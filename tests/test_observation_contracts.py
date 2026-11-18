"""Direct construction tests for Capacity Observation v1 contract invariants."""

from datetime import datetime, timezone
from types import MappingProxyType

import pytest

from tiny_capacity_lab.contracts.observation import (
    CapacityObservation,
    ObservationStatus,
    ProviderWindowValue,
    QuotaWindow,
)


def test_provider_window_value_valid_shapes():
    # Antigravity shape: remaining_fraction + reset_time
    val_ag = ProviderWindowValue(
        remaining_fraction=0.75,
        reset_time="2099-01-08T00:00:00Z",
        raw_window="weekly",
        raw_id="ag-weekly",
    )
    assert val_ag.remaining_fraction == 0.75
    assert val_ag.used_percent is None
    assert val_ag.reset_time == "2099-01-08T00:00:00Z"
    assert val_ag.resets_at_ms is None
    assert val_ag.resets_at_derived is False

    # Muse shape: used_percent + resets_at_ms (derived)
    val_muse = ProviderWindowValue(
        used_percent=10.0,
        resets_at_ms=1794810395000,
        raw_window="window",
        resets_at_derived=True,
    )
    assert val_muse.used_percent == 10.0
    assert val_muse.remaining_fraction is None
    assert val_muse.resets_at_ms == 1794810395000
    assert val_muse.reset_time is None
    assert val_muse.resets_at_derived is True


def test_provider_window_value_invalid_combinations():
    # Neither remaining_fraction nor used_percent
    with pytest.raises(ValueError, match="exactly one of remaining_fraction or used_percent"):
        ProviderWindowValue()

    # Both remaining_fraction and used_percent
    with pytest.raises(ValueError, match="exactly one of remaining_fraction or used_percent"):
        ProviderWindowValue(remaining_fraction=0.5, used_percent=50.0)

    # resets_at_derived=True requires resets_at_ms
    with pytest.raises(ValueError, match="resets_at_derived=True requires resets_at_ms"):
        ProviderWindowValue(used_percent=10.0, resets_at_derived=True)

    # resets_at_ms and reset_time cannot both be present
    with pytest.raises(ValueError, match="resets_at_ms and reset_time cannot both be present"):
        ProviderWindowValue(
            remaining_fraction=0.5,
            reset_time="2099-01-08T00:00:00Z",
            resets_at_ms=1000,
        )


def test_quota_window_timestamp_invariants():
    tz_dt = datetime.now(timezone.utc)
    naive_dt = datetime(2099, 1, 1, 0, 0, 0)
    provider_val = ProviderWindowValue(remaining_fraction=1.0)

    # Valid: timezone-aware datetime
    w_valid = QuotaWindow(
        id="w",
        used_percent=0.0,
        remaining_percent=100.0,
        resets_at=tz_dt,
        provider_value=provider_val,
    )
    assert w_valid.resets_at == tz_dt

    # Valid: None
    w_none = QuotaWindow(
        id="w",
        used_percent=0.0,
        remaining_percent=100.0,
        resets_at=None,
        provider_value=provider_val,
    )
    assert w_none.resets_at is None

    # Invalid: naive datetime rejected
    with pytest.raises(ValueError, match="QuotaWindow.resets_at must be timezone-aware"):
        QuotaWindow(
            id="w",
            used_percent=0.0,
            remaining_percent=100.0,
            resets_at=naive_dt,
            provider_value=provider_val,
        )

    # Invalid: non-datetime
    with pytest.raises(ValueError, match="QuotaWindow.resets_at must be a datetime or None"):
        QuotaWindow(
            id="w",
            used_percent=0.0,
            remaining_percent=100.0,
            resets_at="2099-01-01T00:00:00Z",  # type: ignore[arg-type]
            provider_value=provider_val,
        )


def test_capacity_observation_timestamp_invariants():
    tz_dt = datetime.now(timezone.utc)
    naive_dt = datetime(2099, 1, 1, 0, 0, 0)

    # Valid: timezone-aware collected_at and provider_observed_at
    obs = CapacityObservation(
        schema_version=1,
        provider="test",
        status=ObservationStatus.AVAILABLE,
        collected_at=tz_dt,
        provider_observed_at=tz_dt,
    )
    assert obs.collected_at == tz_dt
    assert obs.provider_observed_at == tz_dt

    # Invalid: naive collected_at
    with pytest.raises(ValueError, match="CapacityObservation.collected_at must be timezone-aware"):
        CapacityObservation(
            schema_version=1,
            provider="test",
            status=ObservationStatus.AVAILABLE,
            collected_at=naive_dt,
        )

    # Invalid: naive provider_observed_at
    with pytest.raises(
        ValueError, match="CapacityObservation.provider_observed_at must be timezone-aware"
    ):
        CapacityObservation(
            schema_version=1,
            provider="test",
            status=ObservationStatus.AVAILABLE,
            collected_at=tz_dt,
            provider_observed_at=naive_dt,
        )


def test_metadata_defensive_copy_and_immutability():
    tz_dt = datetime.now(timezone.utc)
    caller_dict = {"tier": "TierA", "source": "SourceB"}

    obs = CapacityObservation(
        schema_version=1,
        provider="muse",
        status=ObservationStatus.AVAILABLE,
        collected_at=tz_dt,
        metadata=caller_dict,
    )

    assert isinstance(obs.metadata, MappingProxyType)
    assert obs.metadata["tier"] == "TierA"

    # Mutating caller dictionary must not mutate obs.metadata
    caller_dict["tier"] = "MutatedTier"
    assert obs.metadata["tier"] == "TierA"

    # Direct mutation on MappingProxyType must fail
    with pytest.raises(TypeError, match="'mappingproxy' object does not support item assignment"):
        obs.metadata["tier"] = "NewTier"  # type: ignore[index]
