# Capacity Observation v1

## Purpose

Capacity Observation v1 is the smallest provider-neutral representation needed
for Tiny Capacity Lab Experiment 0001.

It represents what Tiny Capacity Lab actually observed from a provider without
inventing missing capacity, reset times, quota groups, or provider state.

The contract is based on evidence collected from Muse Code and Antigravity on
the macOS experiment system.

## Observation

Each provider query produces one provider observation.

Required fields:

```text
schema_version
provider
status
collected_at
groups
```

Optional fields:

```text
reason
hint
provider_observed_at
metadata
```

`schema_version` is `1` for this contract.

`provider` is a stable Tiny Capacity Lab identifier such as:

```text
muse
antigravity
```

`collected_at` records when Tiny Capacity Lab obtained the provider response.

## Observation status

The initial states are:

```text
available
no_observation
error
```

### available

The provider returned usable quota information.

### no_observation

The provider command completed successfully, but no current quota observation
was present.

This state is required by the observed Muse response:

```text
allowance = null
reason = server_sent_no_usage
```

`no_observation` must not be converted into zero usage, full capacity, or an
error.

### error

Tiny Capacity Lab could not obtain or interpret a valid provider response.

Examples may include an unavailable CLI, failed command, or malformed
structured output.

An error must not be replaced with invented quota information.

## Provider metadata

Provider-specific metadata may be retained when it improves provenance.

Observed Muse metadata includes:

```text
tier
source
provider_observed_at
```

Provider metadata must not contain credentials, authentication tokens, prompts,
source code, or personal account identifiers.

## Quota groups

An observation contains zero or more quota groups.

Each group has:

```text
id
name
windows
```

Groups are discovered from provider output.

Tiny Capacity Lab must not assume that a provider always returns a predefined
set of groups.

An absent group means:

```text
not observed
```

It does not mean:

```text
zero capacity
```

or:

```text
exhausted
```

## Quota windows

Each observed quota window has:

```text
id
used_percent
remaining_percent
```

Optional fields:

```text
resets_at
resets_in_seconds
provider_value
```

Known window identifiers may include:

```text
five_hour
weekly
```

Providers may expose other windows later.

The contract must not require every quota group to expose every known window.

## Percentages

Providers may report used or remaining capacity.

Tiny Capacity Lab normalizes observations so consumers can access both:

```text
used_percent
remaining_percent
```

When one value is derived from the other:

```text
remaining_percent = 100 - used_percent
```

or:

```text
used_percent = 100 - remaining_percent
```

the original provider value must remain identifiable as provider-reported
rather than derived.

The raw provider percentage should not be silently changed merely to make a
display look cleaner.

## Reset information

When a provider reports an absolute reset timestamp, Tiny Capacity Lab may
normalize it to `resets_at`.

When a provider reports only a relative duration, Tiny Capacity Lab may retain
that value as `resets_in_seconds`.

If an absolute timestamp is derived from a relative duration, provenance must
identify the value as derived.

Unknown reset information remains unknown.

Tiny Capacity Lab must not fabricate reset times.

## Provenance

Every observation must identify its collection source.

Experiment 0001 initially supports:

```text
provider_cli
```

The source record should preserve enough information to explain how the
observation was obtained without storing credentials or secret command
arguments.

Examples:

```text
Muse Code:
muse usage --json

Antigravity:
agy -p /usage --output-format json
```

The source record may identify whether the observation method is expected to
consume model quota.

Experiment 0001 requires the preferred provider CLI paths to avoid model calls
for quota measurement.

## Freshness

Provider observation time and Tiny Capacity Lab collection time are separate
facts.

Where a provider supplies its own observation timestamp, preserve it as:

```text
provider_observed_at
```

Tiny Capacity Lab records its own:

```text
collected_at
```

Freshness or age calculations must be derived from those timestamps rather
than replacing them.

## Example: Muse before first use

```json
{
  "schema_version": 1,
  "provider": "muse",
  "status": "no_observation",
  "collected_at": "example timestamp",
  "reason": "server_sent_no_usage",
  "hint": "provider supplied hint",
  "groups": []
}
```

The timestamp above is illustrative, not experimental evidence.

## Example: Muse with allowance

```json
{
  "schema_version": 1,
  "provider": "muse",
  "status": "available",
  "collected_at": "example timestamp",
  "provider_observed_at": "example provider timestamp",
  "metadata": {
    "tier": "Muse Code High Usage",
    "source": "mint"
  },
  "groups": [
    {
      "id": "default",
      "name": "Muse Code",
      "windows": [
        {
          "id": "five_hour",
          "used_percent": 0.0,
          "remaining_percent": 100.0
        }
      ]
    }
  ]
}
```

Values not needed to demonstrate the structure are intentionally omitted from
the example.

## Example: Antigravity group

```json
{
  "id": "gemini",
  "name": "Gemini Models",
  "windows": [
    {
      "id": "weekly",
      "used_percent": 12.18,
      "remaining_percent": 87.82,
      "resets_at": "provider-reported reset timestamp"
    }
  ]
}
```

The percentages above illustrate normalization from the observed provider
fraction and are not a replacement for the committed evidence record.

## Privacy boundary

Capacity Observation v1 must not contain:

```text
provider credentials
OAuth tokens
API keys
prompt content
source code
personal account identifiers
```

Provider authentication remains the responsibility of the provider CLI.

## Non-goals

Capacity Observation v1 does not define:

```text
persistent database storage
background polling
UI layout
model quality scores
engineering outcome evidence
tool recommendations
autonomous routing
```

Those concerns belong to later experiments.

## Guiding invariant

Tiny Capacity Lab records what was observed.

Missing, stale, unavailable, or unknown information must remain distinguishable
from measured capacity.

No observation is better than invented certainty.
