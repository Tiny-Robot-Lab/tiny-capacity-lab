"""Capacity Observation v1 contract models.

Immutable data structures representing normalized capacity observations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class ObservationStatus(str, Enum):
    """Observation status defined by Capacity Observation v1."""

    AVAILABLE = "available"
    NO_OBSERVATION = "no_observation"
    ERROR = "error"


class GroupIdSource(str, Enum):
    """Source of a normalized QuotaGroup identifier."""

    PROVIDER_REPORTED = "provider_reported"
    DERIVED_FROM_NAME = "derived_from_name"


@dataclass(frozen=True)
class ProviderWindowValue:
    """Preserves raw provider-reported values for provenance."""

    remaining_fraction: float | None = None
    used_percent: float | None = None
    reset_time: str | None = None
    resets_at_ms: int | None = None
    raw_window: str | None = None
    raw_id: str | None = None
    resets_at_derived: bool = False

    def __post_init__(self) -> None:
        has_rem_frac = self.remaining_fraction is not None
        has_used_pct = self.used_percent is not None
        if has_rem_frac == has_used_pct:
            raise ValueError(
                "ProviderWindowValue requires exactly one of remaining_fraction or used_percent"
            )
        if self.resets_at_derived and self.resets_at_ms is None:
            raise ValueError("resets_at_derived=True requires resets_at_ms")
        if self.resets_at_ms is not None and self.reset_time is not None:
            raise ValueError("resets_at_ms and reset_time cannot both be present")


@dataclass(frozen=True)
class QuotaWindow:
    """Normalized capacity window."""

    id: str
    used_percent: float
    remaining_percent: float
    resets_at: datetime | None = None
    resets_in_seconds: int | float | None = None
    provider_value: ProviderWindowValue | None = None

    def __post_init__(self) -> None:
        if self.resets_at is not None:
            if not isinstance(self.resets_at, datetime):
                raise ValueError("QuotaWindow.resets_at must be a datetime or None")
            if (
                self.resets_at.tzinfo is None
                or self.resets_at.tzinfo.utcoffset(self.resets_at) is None
            ):
                raise ValueError("QuotaWindow.resets_at must be timezone-aware")


@dataclass(frozen=True)
class QuotaGroup:
    """Normalized quota group containing one or more quota windows."""

    id: str
    name: str
    windows: tuple[QuotaWindow, ...] = field(default_factory=tuple)
    description: str | None = None
    id_source: GroupIdSource = GroupIdSource.DERIVED_FROM_NAME


@dataclass(frozen=True)
class CapacityObservation:
    """Normalized provider observation conforming to Capacity Observation v1."""

    schema_version: int
    provider: str
    status: ObservationStatus
    collected_at: datetime
    groups: tuple[QuotaGroup, ...] = field(default_factory=tuple)
    reason: str | None = None
    hint: str | None = None
    provider_observed_at: datetime | None = None
    metadata: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.collected_at, datetime):
            raise ValueError("CapacityObservation.collected_at must be a datetime")
        if (
            self.collected_at.tzinfo is None
            or self.collected_at.tzinfo.utcoffset(self.collected_at) is None
        ):
            raise ValueError("CapacityObservation.collected_at must be timezone-aware")

        if self.provider_observed_at is not None:
            if not isinstance(self.provider_observed_at, datetime):
                raise ValueError(
                    "CapacityObservation.provider_observed_at must be a datetime or None"
                )
            if (
                self.provider_observed_at.tzinfo is None
                or self.provider_observed_at.tzinfo.utcoffset(self.provider_observed_at) is None
            ):
                raise ValueError("CapacityObservation.provider_observed_at must be timezone-aware")

        if self.metadata is not None and not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
