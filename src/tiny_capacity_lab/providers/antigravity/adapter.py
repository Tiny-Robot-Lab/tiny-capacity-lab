"""Adapter for normalizing Antigravity CLI quota responses into Capacity Observation v1."""

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
from tiny_capacity_lab.providers.antigravity.errors import (
    AntigravityParseError,
    AntigravityResponseError,
    AntigravitySchemaError,
    AntigravityValueError,
)

EXPECTED_COMMAND_NAME = "usage"


def _derive_group_id_from_name(name: str) -> str:
    cleaned = "".join(c.lower() if c.isalnum() else "-" for c in name)
    parts = [p for p in cleaned.split("-") if p]
    derived = "-".join(parts)
    if not derived:
        raise AntigravitySchemaError(
            f"Group name {name!r} cannot be derived into a valid group id"
        )
    return derived


def parse_antigravity_response(
    payload: str | bytes | Mapping[str, Any],
    collected_at: datetime | None = None,
) -> CapacityObservation:
    """Parse and normalize an Antigravity CLI quota response.

    Args:
        payload: Decoded mapping or JSON text (str or bytes).
        collected_at: Optional timezone-aware datetime. If omitted, current UTC time is used.

    Returns:
        CapacityObservation representing the normalized observation.

    Raises:
        AntigravityParseError: If JSON decoding fails.
        AntigravitySchemaError: If structural keys or types are invalid.
        AntigravityValueError: If field values are invalid, naive, or out of bounds.
        AntigravityResponseError: If the provider reported an unsuccessful status.
    """
    if isinstance(payload, (str, bytes)):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise AntigravityParseError(f"Malformed JSON payload: {exc}") from exc
    elif isinstance(payload, Mapping):
        data = payload
    else:
        raise AntigravitySchemaError(
            f"Expected JSON text or Mapping, got {type(payload).__name__}"
        )

    if not isinstance(data, Mapping):
        raise AntigravitySchemaError(
            f"Expected top-level payload to be a Mapping, got {type(data).__name__}"
        )

    # Validate collected_at
    if collected_at is None:
        resolved_collected_at = datetime.now(timezone.utc)
    elif isinstance(collected_at, datetime):
        if collected_at.tzinfo is None or collected_at.tzinfo.utcoffset(collected_at) is None:
            raise AntigravityValueError(
                "collected_at must be a timezone-aware datetime, got naive datetime"
            )
        resolved_collected_at = collected_at
    else:
        raise AntigravityValueError(
            "collected_at must be a timezone-aware datetime or None, "
            f"got {type(collected_at).__name__}"
        )

    # Check top-level status: unsuccessful status always raises
    if "status" not in data:
        raise AntigravitySchemaError("Missing required top-level field: 'status'")
    status = data["status"]
    if not isinstance(status, str):
        raise AntigravitySchemaError(
            f"Field 'status' must be a string, got {type(status).__name__}"
        )

    if status != "SUCCESS":
        raise AntigravityResponseError(
            f"Antigravity response status was '{status}', expected 'SUCCESS'"
        )

    # Validate command structure
    if "command" not in data:
        raise AntigravitySchemaError("Missing required field: 'command'")
    command = data["command"]
    if not isinstance(command, Mapping):
        raise AntigravitySchemaError(
            f"Field 'command' must be a Mapping, got {type(command).__name__}"
        )

    if "name" not in command:
        raise AntigravitySchemaError("Missing required field: 'command.name'")
    cmd_name = command["name"]
    if not isinstance(cmd_name, str):
        raise AntigravitySchemaError(
            f"Field 'command.name' must be a string, got {type(cmd_name).__name__}"
        )
    if cmd_name != EXPECTED_COMMAND_NAME:
        raise AntigravitySchemaError(
            f"Expected command.name to be {EXPECTED_COMMAND_NAME!r}, got {cmd_name!r}"
        )

    if "data" not in command:
        raise AntigravitySchemaError("Missing required field: 'command.data'")
    cmd_data = command["data"]
    if not isinstance(cmd_data, Mapping):
        raise AntigravitySchemaError(
            f"Field 'command.data' must be a Mapping, got {type(cmd_data).__name__}"
        )

    if "groups" not in cmd_data:
        raise AntigravitySchemaError("Missing required field: 'command.data.groups'")
    raw_groups = cmd_data["groups"]
    if not isinstance(raw_groups, list):
        raise AntigravitySchemaError(
            f"Field 'command.data.groups' must be a list, got {type(raw_groups).__name__}"
        )

    # Antigravity does not report a provider observation timestamp in recorded evidence
    provider_observed_at = None

    # Discover groups and buckets dynamically
    normalized_groups: list[QuotaGroup] = []

    for group_idx, raw_group in enumerate(raw_groups):
        if not isinstance(raw_group, Mapping):
            raise AntigravitySchemaError(
                f"Group at index {group_idx} must be a Mapping, got {type(raw_group).__name__}"
            )

        if "name" not in raw_group:
            raise AntigravitySchemaError(
                f"Group at index {group_idx} missing required field 'name'"
            )
        group_name = raw_group["name"]
        if not isinstance(group_name, str) or not group_name.strip():
            raise AntigravitySchemaError(
                f"Group at index {group_idx} 'name' must be a non-empty string"
            )

        # Determine group id and provenance
        raw_group_id = raw_group.get("id")
        if raw_group_id is not None:
            if not isinstance(raw_group_id, str) or not raw_group_id.strip():
                raise AntigravitySchemaError(
                    f"Group at index {group_idx} 'id' must be a non-empty string if provided"
                )
            group_id = raw_group_id.strip()
            id_source = GroupIdSource.PROVIDER_REPORTED
        else:
            group_id = _derive_group_id_from_name(group_name)
            id_source = GroupIdSource.DERIVED_FROM_NAME

        if "buckets" not in raw_group:
            raise AntigravitySchemaError(
                f"Group '{group_name}' missing required field 'buckets'"
            )
        raw_buckets = raw_group["buckets"]
        if not isinstance(raw_buckets, list):
            raise AntigravitySchemaError(
                f"Group '{group_name}' 'buckets' must be a list, got {type(raw_buckets).__name__}"
            )

        normalized_windows: list[QuotaWindow] = []

        for bucket_idx, raw_bucket in enumerate(raw_buckets):
            if not isinstance(raw_bucket, Mapping):
                raise AntigravitySchemaError(
                    f"Bucket at index {bucket_idx} in group '{group_name}' must be a Mapping, "
                    f"got {type(raw_bucket).__name__}"
                )

            # Window validation: required non-empty string
            if "window" not in raw_bucket:
                raise AntigravitySchemaError(
                    f"Bucket at index {bucket_idx} in group '{group_name}' "
                    "missing required field 'window'"
                )
            raw_window = raw_bucket["window"]
            if not isinstance(raw_window, str) or not raw_window.strip():
                raise AntigravitySchemaError(
                    f"Bucket at index {bucket_idx} in group '{group_name}' "
                    "'window' must be a non-empty string"
                )

            # Normalize recognized window identifiers; preserve any other non-empty window exactly
            if raw_window == "5h":
                norm_window_id = "five_hour"
            elif raw_window == "weekly":
                norm_window_id = "weekly"
            else:
                norm_window_id = raw_window

            if "remaining_fraction" not in raw_bucket:
                raise AntigravitySchemaError(
                    f"Bucket at index {bucket_idx} in group '{group_name}' "
                    "missing required field 'remaining_fraction'"
                )

            rem_frac = raw_bucket["remaining_fraction"]

            # Booleans are subclasses of int in Python; explicitly reject them
            if isinstance(rem_frac, bool):
                raise AntigravityValueError(
                    f"Bucket 'remaining_fraction' cannot be a boolean in group '{group_name}'"
                )
            if not isinstance(rem_frac, (int, float)):
                raise AntigravityValueError(
                    f"Bucket 'remaining_fraction' must be numeric, got {type(rem_frac).__name__} "
                    f"in group '{group_name}'"
                )
            if math.isnan(rem_frac) or math.isinf(rem_frac):
                raise AntigravityValueError(
                    f"Bucket 'remaining_fraction' must be a finite number, got {rem_frac} "
                    f"in group '{group_name}'"
                )
            if not (0.0 <= rem_frac <= 1.0):
                raise AntigravityValueError(
                    f"Bucket 'remaining_fraction' must be between 0 and 1 inclusive, "
                    f"got {rem_frac} in group '{group_name}'"
                )

            rem_float = float(rem_frac)
            # Exact formula without rounding
            remaining_percent = rem_float * 100.0
            used_percent = 100.0 - remaining_percent

            raw_reset_time = raw_bucket.get("reset_time")
            norm_resets_at: datetime | None = None
            if raw_reset_time is not None:
                if not isinstance(raw_reset_time, str) or not raw_reset_time.strip():
                    raise AntigravitySchemaError(
                        "Bucket 'reset_time' must be a non-empty string or null"
                    )
                try:
                    parsed_reset = datetime.fromisoformat(raw_reset_time)
                except ValueError as exc:
                    raise AntigravityValueError(
                        f"Malformed reset_time ISO 8601 string: {raw_reset_time!r}"
                    ) from exc
                if (
                    parsed_reset.tzinfo is None
                    or parsed_reset.tzinfo.utcoffset(parsed_reset) is None
                ):
                    raise AntigravityValueError(
                        f"reset_time must be timezone-aware, got naive: {raw_reset_time!r}"
                    )
                norm_resets_at = parsed_reset.astimezone(timezone.utc)

            raw_id = raw_bucket.get("id")
            if raw_id is not None and (not isinstance(raw_id, str) or not raw_id.strip()):
                raise AntigravitySchemaError(
                    f"Bucket 'id' must be a non-empty string or null, got {raw_id!r}"
                )

            provider_value = ProviderWindowValue(
                remaining_fraction=rem_float,
                reset_time=raw_reset_time,
                raw_window=raw_window,
                raw_id=raw_id,
            )

            normalized_windows.append(
                QuotaWindow(
                    id=norm_window_id,
                    used_percent=used_percent,
                    remaining_percent=remaining_percent,
                    resets_at=norm_resets_at,
                    provider_value=provider_value,
                )
            )

        group_desc = raw_group.get("description")
        if group_desc is not None and not isinstance(group_desc, str):
            raise AntigravitySchemaError(
                f"Group 'description' must be a string or null, got {type(group_desc).__name__}"
            )

        normalized_groups.append(
            QuotaGroup(
                id=group_id,
                name=group_name,
                windows=tuple(normalized_windows),
                description=group_desc,
                id_source=id_source,
            )
        )

    return CapacityObservation(
        schema_version=1,
        provider="antigravity",
        status=ObservationStatus.AVAILABLE,
        collected_at=resolved_collected_at,
        groups=tuple(normalized_groups),
        provider_observed_at=provider_observed_at,
    )
