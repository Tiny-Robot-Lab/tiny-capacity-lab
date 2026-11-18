"""Tests for the Muse capacity adapter."""

import json
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType

import pytest

from tiny_capacity_lab.contracts.observation import GroupIdSource, ObservationStatus
from tiny_capacity_lab.providers.muse import (
    MuseParseError,
    MuseSchemaError,
    MuseValueError,
    parse_muse_response,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture_text(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def load_fixture_dict(name: str) -> dict:
    return json.loads(load_fixture_text(name))


def test_valid_no_observation_response():
    data = load_fixture_dict("muse_no_observation.json")
    dt = datetime(2026, 11, 17, 21, 30, 0, tzinfo=timezone.utc)
    obs = parse_muse_response(data, collected_at=dt)

    assert obs.schema_version == 1
    assert obs.provider == "muse"
    assert obs.status == ObservationStatus.NO_OBSERVATION
    assert obs.collected_at == dt
    assert obs.groups == ()
    assert obs.reason == "synthetic_server_sent_no_usage"
    assert obs.hint == "synthetic hint explaining that no usage data was returned"
    assert obs.provider_observed_at is None
    assert obs.metadata is None


def test_valid_available_response():
    data = load_fixture_dict("muse_available.json")
    dt = datetime(2026, 11, 17, 21, 30, 0, tzinfo=timezone.utc)
    obs = parse_muse_response(data, collected_at=dt)

    assert obs.schema_version == 1
    assert obs.provider == "muse"
    assert obs.status == ObservationStatus.AVAILABLE
    assert obs.collected_at == dt

    # Distinction between collected_at and provider_observed_at
    expected_as_of = datetime.fromtimestamp(2000000000, tz=timezone.utc)
    assert obs.provider_observed_at == expected_as_of
    assert obs.collected_at != obs.provider_observed_at

    # Group verification
    assert len(obs.groups) == 1
    group = obs.groups[0]
    assert group.id == "muse-code"
    assert group.name == "Muse Code"
    assert group.id_source == GroupIdSource.DERIVED_FROM_NAME
    assert len(group.windows) == 2

    # Five hour window
    w_five = group.windows[0]
    assert w_five.id == "five_hour"
    assert w_five.used_percent == 25.0
    assert w_five.remaining_percent == 75.0
    expected_reset_five = datetime.fromtimestamp(2000018000, tz=timezone.utc)
    assert w_five.resets_at == expected_reset_five
    assert w_five.provider_value is not None
    assert w_five.provider_value.used_percent == 25.0
    assert w_five.provider_value.remaining_fraction is None
    assert w_five.provider_value.resets_at_ms == 2000018000000
    assert w_five.provider_value.resets_at_derived is True
    assert w_five.provider_value.raw_window == "window"

    # Weekly window
    w_weekly = group.windows[1]
    assert w_weekly.id == "weekly"
    assert w_weekly.used_percent == 10.5
    assert w_weekly.remaining_percent == 89.5
    expected_reset_weekly = datetime.fromtimestamp(2000604800, tz=timezone.utc)
    assert w_weekly.resets_at == expected_reset_weekly
    assert w_weekly.provider_value is not None
    assert w_weekly.provider_value.used_percent == 10.5
    assert w_weekly.provider_value.remaining_fraction is None
    assert w_weekly.provider_value.resets_at_ms == 2000604800000
    assert w_weekly.provider_value.resets_at_derived is True
    assert w_weekly.provider_value.raw_window == "weekly"

    # Metadata verification
    assert obs.metadata is not None
    assert isinstance(obs.metadata, MappingProxyType)
    assert obs.metadata["tier"] == "Synthetic Muse Tier Ultra"
    assert obs.metadata["source"] == "synthetic_source"


def test_boundary_percentages_zero_and_hundred():
    data = load_fixture_dict("muse_boundaries.json")
    obs = parse_muse_response(data)

    assert obs.status == ObservationStatus.AVAILABLE
    windows = obs.groups[0].windows

    # 0% used -> 100% remaining
    assert windows[0].used_percent == 0.0
    assert windows[0].remaining_percent == 100.0

    # 100% used -> 0% remaining
    assert windows[1].used_percent == 100.0
    assert windows[1].remaining_percent == 0.0


def test_unrounded_arithmetic_precision():
    payload = {
        "schemaVersion": 1,
        "allowance": {
            "asOfMs": 1000000,
            "window": {"usedPercent": 12.34567, "resetsAtMs": 2000000},
            "weekly": {"usedPercent": 99.12345, "resetsAtMs": 3000000},
        },
    }
    obs = parse_muse_response(payload)
    w_five = obs.groups[0].windows[0]
    expected_remaining = 100.0 - 12.34567
    assert w_five.remaining_percent == expected_remaining
    assert w_five.used_percent == 12.34567


def test_malformed_json_raises_error():
    with pytest.raises(MuseParseError, match="Malformed JSON payload"):
        parse_muse_response("{invalid json:")


def test_unsupported_schema_version():
    data = load_fixture_dict("muse_unsupported_schema.json")
    with pytest.raises(MuseSchemaError, match="Unsupported schemaVersion: 99"):
        parse_muse_response(data)


@pytest.mark.parametrize(
    "corrupted,expected_err,match_str",
    [
        ({}, MuseSchemaError, "Missing required top-level field: 'schemaVersion'"),
        ({"schemaVersion": True}, MuseSchemaError, "Field 'schemaVersion' must be an integer"),
        ({"schemaVersion": "1"}, MuseSchemaError, "Field 'schemaVersion' must be an integer"),
        ({"schemaVersion": 1.0}, MuseSchemaError, "Field 'schemaVersion' must be an integer"),
        ({"schemaVersion": 1}, MuseSchemaError, "Missing required top-level field: 'allowance'"),
        (
            {"schemaVersion": 1, "allowance": "invalid"},
            MuseSchemaError,
            "Field 'allowance' must be null or a Mapping",
        ),
        (
            {"schemaVersion": 1, "allowance": {}},
            MuseSchemaError,
            "Missing required field 'allowance.window'",
        ),
        (
            {"schemaVersion": 1, "allowance": {"window": "invalid"}},
            MuseSchemaError,
            "Field 'allowance.window' must be a Mapping",
        ),
        (
            {"schemaVersion": 1, "allowance": {"window": {}}},
            MuseSchemaError,
            "Missing required field 'allowance.weekly'",
        ),
        (
            {"schemaVersion": 1, "allowance": {"window": {}, "weekly": "invalid"}},
            MuseSchemaError,
            "Field 'allowance.weekly' must be a Mapping",
        ),
        (
            {"schemaVersion": 1, "allowance": {"window": {}, "weekly": {}}},
            MuseSchemaError,
            "Missing required field 'allowance.asOfMs'",
        ),
        (
            {
                "schemaVersion": 1,
                "allowance": {"window": {}, "weekly": {}, "asOfMs": 1000},
            },
            MuseSchemaError,
            "Missing required field 'allowance.window.usedPercent'",
        ),
        (
            {
                "schemaVersion": 1,
                "allowance": {
                    "window": {"usedPercent": 0},
                    "weekly": {},
                    "asOfMs": 1000,
                },
            },
            MuseSchemaError,
            "Missing required field 'allowance.window.resetsAtMs'",
        ),
        (
            {
                "schemaVersion": 1,
                "allowance": {
                    "window": {"usedPercent": 0, "resetsAtMs": 2000},
                    "weekly": {},
                    "asOfMs": 1000,
                },
            },
            MuseSchemaError,
            "Missing required field 'allowance.weekly.usedPercent'",
        ),
        (
            {
                "schemaVersion": 1,
                "allowance": {
                    "window": {"usedPercent": 0, "resetsAtMs": 2000},
                    "weekly": {"usedPercent": 0},
                    "asOfMs": 1000,
                },
            },
            MuseSchemaError,
            "Missing required field 'allowance.weekly.resetsAtMs'",
        ),
        (
            {"schemaVersion": 1, "allowance": None, "reason": 123},
            MuseSchemaError,
            "Field 'reason' must be a string or null",
        ),
        (
            {"schemaVersion": 1, "allowance": None, "hint": 123},
            MuseSchemaError,
            "Field 'hint' must be a string or null",
        ),
    ],
)
def test_missing_and_malformed_structures(corrupted, expected_err, match_str):
    with pytest.raises(expected_err, match=match_str):
        parse_muse_response(corrupted)


@pytest.mark.parametrize(
    "invalid_val,match_str",
    [
        (True, "must be numeric"),
        (False, "must be numeric"),
        ("10", "must be numeric"),
        (None, "must be numeric"),
        ([], "must be numeric"),
        (float("nan"), "must be finite"),
        (float("inf"), "must be finite"),
        (float("-inf"), "must be finite"),
        (-0.01, "between 0 and 100 inclusive"),
        (-5, "between 0 and 100 inclusive"),
        (100.01, "between 0 and 100 inclusive"),
        (150, "between 0 and 100 inclusive"),
    ],
)
def test_invalid_used_percent(invalid_val, match_str):
    payload = {
        "schemaVersion": 1,
        "allowance": {
            "asOfMs": 1000,
            "window": {"usedPercent": invalid_val, "resetsAtMs": 2000},
            "weekly": {"usedPercent": 0, "resetsAtMs": 3000},
        },
    }
    with pytest.raises(MuseValueError, match=match_str):
        parse_muse_response(payload)


@pytest.mark.parametrize(
    "invalid_epoch_ms,match_str",
    [
        (True, "must be an integer"),
        (False, "must be an integer"),
        (123.456, "must be an integer"),
        ("1000", "must be an integer"),
        (-1, "must be non-negative"),
        (-5000, "must be non-negative"),
    ],
)
def test_invalid_epoch_ms_values(invalid_epoch_ms, match_str):
    # Invalid asOfMs
    p1 = {
        "schemaVersion": 1,
        "allowance": {
            "asOfMs": invalid_epoch_ms,
            "window": {"usedPercent": 0, "resetsAtMs": 2000},
            "weekly": {"usedPercent": 0, "resetsAtMs": 3000},
        },
    }
    with pytest.raises(MuseValueError, match=match_str):
        parse_muse_response(p1)

    # Invalid window.resetsAtMs
    p2 = {
        "schemaVersion": 1,
        "allowance": {
            "asOfMs": 1000,
            "window": {"usedPercent": 0, "resetsAtMs": invalid_epoch_ms},
            "weekly": {"usedPercent": 0, "resetsAtMs": 3000},
        },
    }
    with pytest.raises(MuseValueError, match=match_str):
        parse_muse_response(p2)

    # Invalid weekly.resetsAtMs
    p3 = {
        "schemaVersion": 1,
        "allowance": {
            "asOfMs": 1000,
            "window": {"usedPercent": 0, "resetsAtMs": 2000},
            "weekly": {"usedPercent": 0, "resetsAtMs": invalid_epoch_ms},
        },
    }
    with pytest.raises(MuseValueError, match=match_str):
        parse_muse_response(p3)


@pytest.mark.parametrize(
    "field_target,expected_field_name",
    [
        ("asOfMs", "allowance.asOfMs"),
        ("window", "allowance.window.resetsAtMs"),
        ("weekly", "allowance.weekly.resetsAtMs"),
    ],
)
def test_excessively_large_epoch_ms(field_target, expected_field_name):
    payload = {
        "schemaVersion": 1,
        "allowance": {
            "asOfMs": 1000,
            "window": {"usedPercent": 0, "resetsAtMs": 2000},
            "weekly": {"usedPercent": 0, "resetsAtMs": 3000},
        },
    }
    excessive_val = 10**25
    if field_target == "asOfMs":
        payload["allowance"]["asOfMs"] = excessive_val
    elif field_target == "window":
        payload["allowance"]["window"]["resetsAtMs"] = excessive_val
    elif field_target == "weekly":
        payload["allowance"]["weekly"]["resetsAtMs"] = excessive_val

    with pytest.raises(
        MuseValueError,
        match=f"Malformed or out-of-range epoch millisecond timestamp in '{expected_field_name}'",
    ):
        parse_muse_response(payload)


@pytest.mark.parametrize("invalid_tier", ["", "   ", 123, True, []])
def test_invalid_metadata_tier(invalid_tier):
    payload = {
        "schemaVersion": 1,
        "allowance": {
            "tier": invalid_tier,
            "asOfMs": 1000,
            "window": {"usedPercent": 0, "resetsAtMs": 2000},
            "weekly": {"usedPercent": 0, "resetsAtMs": 3000},
        },
    }
    with pytest.raises(MuseSchemaError, match="Field 'allowance.tier' must be a non-empty string"):
        parse_muse_response(payload)


@pytest.mark.parametrize("invalid_source", ["", "   ", 123, True, []])
def test_invalid_metadata_source(invalid_source):
    payload = {
        "schemaVersion": 1,
        "allowance": {
            "source": invalid_source,
            "asOfMs": 1000,
            "window": {"usedPercent": 0, "resetsAtMs": 2000},
            "weekly": {"usedPercent": 0, "resetsAtMs": 3000},
        },
    }
    with pytest.raises(
        MuseSchemaError, match="Field 'allowance.source' must be a non-empty string"
    ):
        parse_muse_response(payload)


def test_metadata_optional_and_caller_dict_mutation():
    # Neither tier nor source present
    payload = {
        "schemaVersion": 1,
        "allowance": {
            "asOfMs": 1000,
            "window": {"usedPercent": 0, "resetsAtMs": 2000},
            "weekly": {"usedPercent": 0, "resetsAtMs": 3000},
        },
    }
    obs = parse_muse_response(payload)
    assert obs.metadata is None

    # Caller dictionary mutation test
    caller_dict = {"tier": "TierInitial", "source": "SourceInitial"}
    payload["allowance"]["tier"] = caller_dict["tier"]
    payload["allowance"]["source"] = caller_dict["source"]
    obs_meta = parse_muse_response(payload)
    assert obs_meta.metadata is not None
    assert obs_meta.metadata["tier"] == "TierInitial"

    caller_dict["tier"] = "MutatedLater"
    assert obs_meta.metadata["tier"] == "TierInitial"


def test_collected_at_timezone_validation():
    data = load_fixture_dict("muse_no_observation.json")

    # Timezone-aware datetime works
    tz_dt = datetime.now(timezone.utc)
    obs = parse_muse_response(data, collected_at=tz_dt)
    assert obs.collected_at == tz_dt

    # Naive datetime rejected
    naive_dt = datetime.now()  # noqa: DTZ005
    with pytest.raises(MuseValueError, match="must be a timezone-aware datetime"):
        parse_muse_response(data, collected_at=naive_dt)

    # String timestamp rejected
    with pytest.raises(MuseValueError, match="must be a timezone-aware datetime or None"):
        parse_muse_response(data, collected_at="2026-11-17T21:30:00Z")  # type: ignore[arg-type]


def test_immutability_and_no_nested_mutable_state():
    data = load_fixture_dict("muse_available.json")
    obs = parse_muse_response(data)

    # Observation immutability
    with pytest.raises(FrozenInstanceError):
        obs.status = ObservationStatus.ERROR  # type: ignore[misc]

    # Group immutability
    with pytest.raises(FrozenInstanceError):
        obs.groups[0].name = "Mutated"  # type: ignore[misc]

    # Window immutability
    with pytest.raises(FrozenInstanceError):
        obs.groups[0].windows[0].used_percent = 99.9  # type: ignore[misc]

    # ProviderValue immutability
    with pytest.raises(FrozenInstanceError):
        obs.groups[0].windows[0].provider_value.used_percent = 99.9  # type: ignore[misc]

    # MappingProxyType immutability
    assert obs.metadata is not None
    assert isinstance(obs.metadata, MappingProxyType)
    with pytest.raises(TypeError, match="'mappingproxy' object does not support item assignment"):
        obs.metadata["tier"] = "Hacked"  # type: ignore[index]


def test_unrelated_unknown_fields_ignored():
    payload = {
        "schemaVersion": 1,
        "unexpected_extra_field": "ignore_me",
        "human_readable_junk": {"foo": "bar"},
        "allowance": {
            "tier": "Tier",
            "source": "Source",
            "asOfMs": 1000,
            "window": {
                "usedPercent": 10,
                "resetsAtMs": 2000,
                "extra_window_info": "ignored",
            },
            "weekly": {
                "usedPercent": 20,
                "resetsAtMs": 3000,
                "extra_weekly_info": 42,
            },
            "extra_allowance_info": [1, 2, 3],
        },
    }
    obs = parse_muse_response(payload)
    assert obs.status == ObservationStatus.AVAILABLE
    assert len(obs.groups[0].windows) == 2
    assert obs.metadata == {"tier": "Tier", "source": "Source"}
