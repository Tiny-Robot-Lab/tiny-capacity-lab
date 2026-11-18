"""Adapter for normalizing Muse CLI quota responses into Capacity Observation v1."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from typing import Any, Mapping

from tiny_capacity_lab.contracts.observation import (
    CapacityObservation,
    GroupIdSource,
    ObservationStatus,
    ProviderWindowValue,
    QuotaGroup,
    QuotaWindow,
)
from tiny_capacity_lab.providers.muse.errors import (
    MuseParseError,
    MuseSchemaError,
    MuseValueError,
)

SUPPORTED_SCHEMA_VERSION = 1


def _epoch_ms_to_datetime(ms: int, field_name: str) -> datetime:
    try:
        seconds, milliseconds = divmod(ms, 1000)
        return datetime.fromtimestamp(seconds, tz=timezone.utc).replace(
            microsecond=milliseconds * 1000
        )
    except (OverflowError, OSError, ValueError) as exc:
        raise MuseValueError(
            f"Malformed or out-of-range epoch millisecond timestamp in '{field_name}': {ms}"
        ) from exc


def _validate_used_percent(val: Any, window_name: str) -> float:
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise MuseValueError(
            f"allowance.{window_name}.usedPercent must be numeric, got {type(val).__name__}"
        )
    if math.isnan(val) or math.isinf(val):
        raise MuseValueError(
            f"allowance.{window_name}.usedPercent must be finite, got {val}"
        )
    if not (0.0 <= val <= 100.0):
        raise MuseValueError(
            f"allowance.{window_name}.usedPercent must be between 0 and 100 inclusive, got {val}"
        )
    return float(val)


def _validate_epoch_ms(val: Any, field_name: str) -> int:
    if isinstance(val, bool) or not isinstance(val, int):
        raise MuseValueError(f"{field_name} must be an integer, got {type(val).__name__}")
    if val < 0:
        raise MuseValueError(f"{field_name} must be non-negative, got {val}")
    return val


def parse_muse_response(
    payload: str | bytes | Mapping[str, Any],
    collected_at: datetime | None = None,
) -> CapacityObservation:
    """Parse and normalize a Muse CLI quota response.

    Args:
        payload: Decoded mapping or JSON text (str or bytes).
        collected_at: Optional timezone-aware datetime. If omitted, current UTC time is used.

    Returns:
        CapacityObservation representing the normalized observation.

    Raises:
        MuseParseError: If JSON decoding fails.
        MuseSchemaError: If structural keys, types, or schemaVersion are invalid.
        MuseValueError: If field values are invalid, naive, or out of bounds.
    """
    if isinstance(payload, (str, bytes)):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise MuseParseError(f"Malformed JSON payload: {exc}") from exc
    elif isinstance(payload, Mapping):
        data = payload
    else:
        raise MuseSchemaError(
            f"Expected JSON text or Mapping, got {type(payload).__name__}"
        )

    if not isinstance(data, Mapping):
        raise MuseSchemaError(
            f"Expected top-level payload to be a Mapping, got {type(data).__name__}"
        )

    # Validate collected_at
    if collected_at is None:
        resolved_collected_at = datetime.now(timezone.utc)
    elif isinstance(collected_at, datetime):
        if collected_at.tzinfo is None or collected_at.tzinfo.utcoffset(collected_at) is None:
            raise MuseValueError(
                "collected_at must be a timezone-aware datetime, got naive datetime"
            )
        resolved_collected_at = collected_at
    else:
        raise MuseValueError(
            "collected_at must be a timezone-aware datetime or None, "
            f"got {type(collected_at).__name__}"
        )

    # Require top-level schemaVersion
    if "schemaVersion" not in data:
        raise MuseSchemaError("Missing required top-level field: 'schemaVersion'")
    schema_version = data["schemaVersion"]
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise MuseSchemaError(
            f"Field 'schemaVersion' must be an integer, got {type(schema_version).__name__}"
        )
    if schema_version != SUPPORTED_SCHEMA_VERSION:
        raise MuseSchemaError(
            f"Unsupported schemaVersion: {schema_version}, expected {SUPPORTED_SCHEMA_VERSION}"
        )

    # Require top-level allowance
    if "allowance" not in data:
        raise MuseSchemaError("Missing required top-level field: 'allowance'")
    allowance = data["allowance"]
    if allowance is not None and not isinstance(allowance, Mapping):
        raise MuseSchemaError(
            f"Field 'allowance' must be null or a Mapping, got {type(allowance).__name__}"
        )

    # Case 1: No-observation response (allowance is null)
    if allowance is None:
        raw_reason = data.get("reason")
        if raw_reason is not None and not isinstance(raw_reason, str):
            raise MuseSchemaError(
                f"Field 'reason' must be a string or null, got {type(raw_reason).__name__}"
            )
        raw_hint = data.get("hint")
        if raw_hint is not None and not isinstance(raw_hint, str):
            raise MuseSchemaError(
                f"Field 'hint' must be a string or null, got {type(raw_hint).__name__}"
            )

        return CapacityObservation(
            schema_version=1,
            provider="muse",
            status=ObservationStatus.NO_OBSERVATION,
            collected_at=resolved_collected_at,
            groups=(),
            reason=raw_reason,
            hint=raw_hint,
            provider_observed_at=None,
            metadata=None,
        )

    # Case 2: Available allowance
    if "window" not in allowance:
        raise MuseSchemaError("Missing required field 'allowance.window'")
    raw_window = allowance["window"]
    if not isinstance(raw_window, Mapping):
        raise MuseSchemaError(
            f"Field 'allowance.window' must be a Mapping, got {type(raw_window).__name__}"
        )

    if "weekly" not in allowance:
        raise MuseSchemaError("Missing required field 'allowance.weekly'")
    raw_weekly = allowance["weekly"]
    if not isinstance(raw_weekly, Mapping):
        raise MuseSchemaError(
            f"Field 'allowance.weekly' must be a Mapping, got {type(raw_weekly).__name__}"
        )

    if "asOfMs" not in allowance:
        raise MuseSchemaError("Missing required field 'allowance.asOfMs'")
    as_of_ms = _validate_epoch_ms(allowance["asOfMs"], "allowance.asOfMs")
    provider_observed_at = _epoch_ms_to_datetime(as_of_ms, "allowance.asOfMs")

    # Validate five-hour window
    if "usedPercent" not in raw_window:
        raise MuseSchemaError("Missing required field 'allowance.window.usedPercent'")
    w_used = _validate_used_percent(raw_window["usedPercent"], "window")
    w_remaining = 100.0 - w_used

    if "resetsAtMs" not in raw_window:
        raise MuseSchemaError("Missing required field 'allowance.window.resetsAtMs'")
    w_reset_ms = _validate_epoch_ms(raw_window["resetsAtMs"], "allowance.window.resetsAtMs")
    w_resets_at = _epoch_ms_to_datetime(w_reset_ms, "allowance.window.resetsAtMs")

    window_five_hour = QuotaWindow(
        id="five_hour",
        used_percent=w_used,
        remaining_percent=w_remaining,
        resets_at=w_resets_at,
        provider_value=ProviderWindowValue(
            used_percent=w_used,
            resets_at_ms=w_reset_ms,
            raw_window="window",
            resets_at_derived=True,
        ),
    )

    # Validate weekly window
    if "usedPercent" not in raw_weekly:
        raise MuseSchemaError("Missing required field 'allowance.weekly.usedPercent'")
    weekly_used = _validate_used_percent(raw_weekly["usedPercent"], "weekly")
    weekly_remaining = 100.0 - weekly_used

    if "resetsAtMs" not in raw_weekly:
        raise MuseSchemaError("Missing required field 'allowance.weekly.resetsAtMs'")
    weekly_reset_ms = _validate_epoch_ms(raw_weekly["resetsAtMs"], "allowance.weekly.resetsAtMs")
    weekly_resets_at = _epoch_ms_to_datetime(weekly_reset_ms, "allowance.weekly.resetsAtMs")

    window_weekly = QuotaWindow(
        id="weekly",
        used_percent=weekly_used,
        remaining_percent=weekly_remaining,
        resets_at=weekly_resets_at,
        provider_value=ProviderWindowValue(
            used_percent=weekly_used,
            resets_at_ms=weekly_reset_ms,
            raw_window="weekly",
            resets_at_derived=True,
        ),
    )

    group = QuotaGroup(
        id="muse-code",
        name="Muse Code",
        windows=(window_five_hour, window_weekly),
        id_source=GroupIdSource.DERIVED_FROM_NAME,
    )

    # Preserve tier and source metadata if present
    meta_dict: dict[str, str] = {}
    if "tier" in allowance and allowance["tier"] is not None:
        tier_val = allowance["tier"]
        if not isinstance(tier_val, str) or not tier_val.strip():
            raise MuseSchemaError(
                f"Field 'allowance.tier' must be a non-empty string, got {tier_val!r}"
            )
        meta_dict["tier"] = tier_val

    if "source" in allowance and allowance["source"] is not None:
        source_val = allowance["source"]
        if not isinstance(source_val, str) or not source_val.strip():
            raise MuseSchemaError(
                f"Field 'allowance.source' must be a non-empty string, got {source_val!r}"
            )
        meta_dict["source"] = source_val

    resolved_metadata = meta_dict if meta_dict else None

    return CapacityObservation(
        schema_version=1,
        provider="muse",
        status=ObservationStatus.AVAILABLE,
        collected_at=resolved_collected_at,
        groups=(group,),
        provider_observed_at=provider_observed_at,
        metadata=resolved_metadata,
    )
