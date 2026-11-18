"""Tests for the Antigravity capacity adapter."""

import json
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tiny_capacity_lab.contracts.observation import GroupIdSource, ObservationStatus
from tiny_capacity_lab.providers.antigravity import (
    AntigravityParseError,
    AntigravityResponseError,
    AntigravitySchemaError,
    AntigravityValueError,
    parse_antigravity_response,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture_text(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def load_fixture_dict(name: str) -> dict:
    return json.loads(load_fixture_text(name))


def test_valid_response_multiple_dynamically_discovered_groups_and_windows():
    fixture_text = load_fixture_text("antigravity_valid.json")
    dt = datetime(2026, 11, 17, 21, 0, 0, tzinfo=timezone.utc)
    obs = parse_antigravity_response(fixture_text, collected_at=dt)

    assert obs.schema_version == 1
    assert obs.provider == "antigravity"
    assert obs.status == ObservationStatus.AVAILABLE
    assert obs.collected_at == dt
    assert obs.provider_observed_at is None
    assert obs.reason is None
    assert obs.hint is None

    # Discover groups dynamically: two groups
    assert len(obs.groups) == 2

    # Group 1: explicit provider-reported ID
    g1 = obs.groups[0]
    assert g1.id == "explicit-alpha"
    assert g1.id_source == GroupIdSource.PROVIDER_REPORTED
    assert g1.name == "Synthetic Alpha Models"
    assert g1.description == "Synthetic model group A"
    assert len(g1.windows) == 2

    w1_weekly = g1.windows[0]
    assert w1_weekly.id == "weekly"
    assert w1_weekly.remaining_percent == 75.0
    assert w1_weekly.used_percent == 25.0
    assert w1_weekly.resets_at == datetime(2099, 1, 8, 0, 0, 0, tzinfo=timezone.utc)
    assert w1_weekly.provider_value is not None
    assert w1_weekly.provider_value.remaining_fraction == 0.75
    assert w1_weekly.provider_value.reset_time == "2099-01-08T00:00:00Z"
    assert w1_weekly.provider_value.raw_window == "weekly"
    assert w1_weekly.provider_value.raw_id == "synth-alpha-weekly"

    w1_5h = g1.windows[1]
    assert w1_5h.id == "five_hour"
    assert w1_5h.remaining_percent == 40.0
    assert w1_5h.used_percent == 60.0
    assert w1_5h.resets_at == datetime(2099, 1, 1, 5, 0, 0, tzinfo=timezone.utc)
    assert w1_5h.provider_value is not None
    assert w1_5h.provider_value.remaining_fraction == 0.40
    assert w1_5h.provider_value.reset_time == "2099-01-01T05:00:00Z"
    assert w1_5h.provider_value.raw_window == "5h"
    assert w1_5h.provider_value.raw_id == "synth-alpha-5h"

    # Group 2: derived from name
    g2 = obs.groups[1]
    assert g2.id == "synthetic-beta-models"
    assert g2.id_source == GroupIdSource.DERIVED_FROM_NAME
    assert g2.name == "Synthetic Beta Models"
    assert g2.description == "Synthetic model group B"
    assert len(g2.windows) == 1

    w2_weekly = g2.windows[0]
    assert w2_weekly.id == "weekly"
    assert w2_weekly.remaining_percent == 90.0
    assert w2_weekly.used_percent == 10.0
    assert w2_weekly.resets_at == datetime(2099, 1, 8, 0, 0, 0, tzinfo=timezone.utc)
    assert w2_weekly.provider_value is not None
    assert w2_weekly.provider_value.remaining_fraction == 0.90


def test_boundary_fractions_zero_and_one():
    data = load_fixture_dict("antigravity_boundaries.json")
    obs = parse_antigravity_response(data)

    assert obs.status == ObservationStatus.AVAILABLE
    assert len(obs.groups) == 1
    windows = obs.groups[0].windows
    assert len(windows) == 2

    # Boundary 0.0
    w0 = windows[0]
    assert w0.remaining_percent == 0.0
    assert w0.used_percent == 100.0
    assert w0.provider_value is not None
    assert w0.provider_value.remaining_fraction == 0.0

    # Boundary 1.0
    w1 = windows[1]
    assert w1.remaining_percent == 100.0
    assert w1.used_percent == 0.0
    assert w1.provider_value is not None
    assert w1.provider_value.remaining_fraction == 1.0


def test_numeric_precision_without_rounding():
    payload = {
        "status": "SUCCESS",
        "command": {
            "name": "usage",
            "data": {
                "groups": [
                    {
                        "name": "Precision Test",
                        "buckets": [
                            {
                                "window": "weekly",
                                "remaining_fraction": 0.8782,
                            }
                        ],
                    }
                ]
            },
        },
    }
    obs = parse_antigravity_response(payload)
    window = obs.groups[0].windows[0]
    # Verify exact float calculation without 4-decimal rounding
    expected_remaining = 0.8782 * 100.0
    expected_used = 100.0 - expected_remaining
    assert window.remaining_percent == expected_remaining
    assert window.used_percent == expected_used
    assert window.provider_value.remaining_fraction == 0.8782


def test_empty_groups_as_honest_available_observation():
    data = load_fixture_dict("antigravity_empty_groups.json")
    obs = parse_antigravity_response(data)

    assert obs.status == ObservationStatus.AVAILABLE
    assert obs.groups == ()


def test_malformed_json_raises_error():
    with pytest.raises(AntigravityParseError, match="Malformed JSON payload"):
        parse_antigravity_response("{malformed json:")


def test_unsuccessful_provider_status_always_raises():
    data = load_fixture_dict("antigravity_unsuccessful.json")
    with pytest.raises(AntigravityResponseError, match="status was 'FAILURE'"):
        parse_antigravity_response(data)


def test_command_name_validation():
    # Another command name must be rejected
    payload = {
        "status": "SUCCESS",
        "command": {
            "name": "status",
            "data": {"groups": []},
        },
    }
    with pytest.raises(AntigravitySchemaError, match="Expected command.name to be 'usage'"):
        parse_antigravity_response(payload)


def test_window_identity_preservation():
    payload = {
        "status": "SUCCESS",
        "command": {
            "name": "usage",
            "data": {
                "groups": [
                    {
                        "name": "Window Group",
                        "buckets": [
                            {
                                "window": "CustomWindow_XYZ",
                                "remaining_fraction": 0.5,
                            }
                        ],
                    }
                ]
            },
        },
    }
    obs = parse_antigravity_response(payload)
    w = obs.groups[0].windows[0]
    # Exact case preservation (not lowercased)
    assert w.id == "CustomWindow_XYZ"
    assert w.provider_value.raw_window == "CustomWindow_XYZ"


def test_non_derivable_and_empty_group_name():
    # Empty string
    p1 = {
        "status": "SUCCESS",
        "command": {
            "name": "usage",
            "data": {
                "groups": [{"name": "", "buckets": []}],
            },
        },
    }
    with pytest.raises(AntigravitySchemaError, match="must be a non-empty string"):
        parse_antigravity_response(p1)

    # Non-derivable characters (e.g. symbols only)
    p2 = {
        "status": "SUCCESS",
        "command": {
            "name": "usage",
            "data": {
                "groups": [{"name": "!!!###", "buckets": []}],
            },
        },
    }
    with pytest.raises(AntigravitySchemaError, match="cannot be derived into a valid group id"):
        parse_antigravity_response(p2)


@pytest.mark.parametrize(
    "corrupted_payload,expected_err,err_match",
    [
        ({}, AntigravitySchemaError, "Missing required top-level field: 'status'"),
        ({"status": 123}, AntigravitySchemaError, "Field 'status' must be a string"),
        ({"status": "SUCCESS"}, AntigravitySchemaError, "Missing required field: 'command'"),
        (
            {"status": "SUCCESS", "command": "not-a-dict"},
            AntigravitySchemaError,
            "Field 'command' must be a Mapping",
        ),
        (
            {"status": "SUCCESS", "command": {}},
            AntigravitySchemaError,
            "Missing required field: 'command.name'",
        ),
        (
            {"status": "SUCCESS", "command": {"name": "usage"}},
            AntigravitySchemaError,
            "Missing required field: 'command.data'",
        ),
        (
            {"status": "SUCCESS", "command": {"name": "usage", "data": []}},
            AntigravitySchemaError,
            "Field 'command.data' must be a Mapping",
        ),
        (
            {"status": "SUCCESS", "command": {"name": "usage", "data": {}}},
            AntigravitySchemaError,
            "Missing required field: 'command.data.groups'",
        ),
        (
            {"status": "SUCCESS", "command": {"name": "usage", "data": {"groups": "not-a-list"}}},
            AntigravitySchemaError,
            "Field 'command.data.groups' must be a list",
        ),
        (
            {"status": "SUCCESS", "command": {"name": "usage", "data": {"groups": ["not-a-dict"]}}},
            AntigravitySchemaError,
            "Group at index 0 must be a Mapping",
        ),
        (
            {"status": "SUCCESS", "command": {"name": "usage", "data": {"groups": [{}]}}},
            AntigravitySchemaError,
            "Group at index 0 missing required field 'name'",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {"name": "usage", "data": {"groups": [{"name": 999}]}},
            },
            AntigravitySchemaError,
            "Group at index 0 'name' must be a non-empty string",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {"name": "usage", "data": {"groups": [{"name": "G", "id": ""}]}},
            },
            AntigravitySchemaError,
            "Group at index 0 'id' must be a non-empty string if provided",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {"name": "usage", "data": {"groups": [{"name": "G"}]}},
            },
            AntigravitySchemaError,
            "Group 'G' missing required field 'buckets'",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {
                    "name": "usage",
                    "data": {"groups": [{"name": "G", "buckets": "not-a-list"}]},
                },
            },
            AntigravitySchemaError,
            "Group 'G' 'buckets' must be a list",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {
                    "name": "usage",
                    "data": {"groups": [{"name": "G", "buckets": ["not-a-dict"]}]},
                },
            },
            AntigravitySchemaError,
            "Bucket at index 0 in group 'G' must be a Mapping",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {
                    "name": "usage",
                    "data": {"groups": [{"name": "G", "buckets": [{}]}]},
                },
            },
            AntigravitySchemaError,
            "missing required field 'window'",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {
                    "name": "usage",
                    "data": {"groups": [{"name": "G", "buckets": [{"window": ""}]}]},
                },
            },
            AntigravitySchemaError,
            "'window' must be a non-empty string",
        ),
        (
            {
                "status": "SUCCESS",
                "command": {
                    "name": "usage",
                    "data": {
                        "groups": [{"name": "G", "buckets": [{"window": "weekly"}]}]
                    },
                },
            },
            AntigravitySchemaError,
            "missing required field 'remaining_fraction'",
        ),
    ],
)
def test_missing_and_malformed_structures(corrupted_payload, expected_err, err_match):
    with pytest.raises(expected_err, match=err_match):
        parse_antigravity_response(corrupted_payload)


@pytest.mark.parametrize(
    "fraction_value,err_match",
    [
        (True, "cannot be a boolean"),
        (False, "cannot be a boolean"),
        ("0.75", "must be numeric"),
        (None, "must be numeric"),
        ([], "must be numeric"),
        ({}, "must be numeric"),
        (float("nan"), "must be a finite number"),
        (float("inf"), "must be a finite number"),
        (float("-inf"), "must be a finite number"),
        (-0.01, "between 0 and 1 inclusive"),
        (-1.0, "between 0 and 1 inclusive"),
        (1.0001, "between 0 and 1 inclusive"),
        (2.5, "between 0 and 1 inclusive"),
    ],
)
def test_invalid_remaining_fraction(fraction_value, err_match):
    payload = {
        "status": "SUCCESS",
        "command": {
            "name": "usage",
            "data": {
                "groups": [
                    {
                        "name": "Synthetic Group",
                        "buckets": [
                            {
                                "id": "synth-bucket",
                                "window": "weekly",
                                "remaining_fraction": fraction_value,
                            }
                        ],
                    }
                ]
            },
        },
    }
    with pytest.raises(AntigravityValueError, match=err_match):
        parse_antigravity_response(payload)


def test_invalid_reset_time():
    base_payload = {
        "status": "SUCCESS",
        "command": {
            "name": "usage",
            "data": {
                "groups": [
                    {
                        "name": "Synthetic Group",
                        "buckets": [
                            {
                                "id": "synth-bucket",
                                "window": "weekly",
                                "remaining_fraction": 0.5,
                                "reset_time": "",
                            }
                        ],
                    }
                ]
            },
        },
    }

    # Empty string
    with pytest.raises(AntigravitySchemaError, match="must be a non-empty string or null"):
        parse_antigravity_response(base_payload)

    # Malformed ISO
    base_payload["command"]["data"]["groups"][0]["buckets"][0]["reset_time"] = "not-a-datetime"
    with pytest.raises(AntigravityValueError, match="Malformed reset_time ISO 8601 string"):
        parse_antigravity_response(base_payload)

    # Naive ISO
    base_payload["command"]["data"]["groups"][0]["buckets"][0]["reset_time"] = "2099-01-08T00:00:00"
    with pytest.raises(AntigravityValueError, match="must be timezone-aware, got naive"):
        parse_antigravity_response(base_payload)

    # Non-string
    base_payload["command"]["data"]["groups"][0]["buckets"][0]["reset_time"] = 123456
    with pytest.raises(AntigravitySchemaError, match="must be a non-empty string or null"):
        parse_antigravity_response(base_payload)


def test_collected_at_timezone_validation():
    data = load_fixture_dict("antigravity_empty_groups.json")

    # Timezone-aware datetime works
    tz_dt = datetime.now(timezone.utc)
    obs = parse_antigravity_response(data, collected_at=tz_dt)
    assert obs.collected_at == tz_dt

    # Naive datetime rejected
    naive_dt = datetime.now()  # noqa: DTZ005
    with pytest.raises(AntigravityValueError, match="must be a timezone-aware datetime"):
        parse_antigravity_response(data, collected_at=naive_dt)

    # String timestamp rejected
    with pytest.raises(AntigravityValueError, match="must be a timezone-aware datetime or None"):
        parse_antigravity_response(data, collected_at="2026-11-17T21:00:00Z")  # type: ignore[arg-type]


def test_immutability_and_no_nested_mutable_state():
    data = load_fixture_dict("antigravity_boundaries.json")
    obs = parse_antigravity_response(data)

    # Top-level model immutability
    with pytest.raises(FrozenInstanceError):
        obs.status = ObservationStatus.ERROR  # type: ignore[misc]

    # Group model immutability
    with pytest.raises(FrozenInstanceError):
        obs.groups[0].name = "Mutated"  # type: ignore[misc]

    # Window model immutability
    with pytest.raises(FrozenInstanceError):
        obs.groups[0].windows[0].remaining_percent = 99.9  # type: ignore[misc]

    # ProviderValue immutability
    with pytest.raises(FrozenInstanceError):
        obs.groups[0].windows[0].provider_value.remaining_fraction = 0.5  # type: ignore[misc]

    # Tuples used instead of mutable lists
    assert isinstance(obs.groups, tuple)
    assert isinstance(obs.groups[0].windows, tuple)

    # Ensure no mutable mapping attribute is exposed
    assert obs.metadata is None


def test_does_not_parse_or_require_response_text():
    payload = {
        "status": "SUCCESS",
        "response": "HUMAN_READABLE_TEXT_SHOULD_BE_IGNORED",
        "command": {
            "name": "usage",
            "data": {
                "groups": [
                    {
                        "name": "Synthetic Group",
                        "buckets": [
                            {
                                "id": "test-b1",
                                "window": "weekly",
                                "remaining_fraction": 0.5,
                            }
                        ],
                    }
                ]
            },
        },
    }
    obs = parse_antigravity_response(payload)
    assert obs.status == ObservationStatus.AVAILABLE
    assert obs.reason is None
    assert obs.hint is None
    assert obs.provider_observed_at is None
