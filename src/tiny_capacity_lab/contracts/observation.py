"""Capacity Observation v1 contract models.

Immutable data structures representing normalized capacity observations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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

    remaining_fraction: float
    reset_time: str | None = None
    raw_window: str | None = None
    raw_id: str | None = None


@dataclass(frozen=True)
class QuotaWindow:
    """Normalized capacity window."""

    id: str
    used_percent: float
    remaining_percent: float
    resets_at: str | None = None
    resets_in_seconds: int | float | None = None
    provider_value: ProviderWindowValue | None = None


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
    provider_observed_at: str | None = None
