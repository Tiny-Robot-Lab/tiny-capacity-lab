# Experiment 0001 Evidence: Muse Code quota schema

## Observation

Tiny Capacity Lab inspected the structured quota output produced by the
locally installed Muse Code CLI on the macOS experiment system.

Command:

```text
muse usage --json
```

Two observations were made around the first Muse activity in a new usage
window.

## Observation 1: Before first use

Before sending a new Muse request, the CLI returned:

```json
{
  "schemaVersion": 1,
  "allowance": null,
  "reason": "server_sent_no_usage",
  "hint": "the server sent no usage data for this subscription; this can happen before your first use in a new window"
}
```

This is a successful structured response, but no current allowance
measurement is present.

Tiny Capacity Lab must not translate this state into either:

```text
0% remaining
```

or:

```text
100% remaining
```

The provider reported no allowance observation.

## Observation 2: After first use

One small real Muse interaction was performed.

A subsequent:

```text
muse usage --json
```

returned an allowance object:

```json
{
  "schemaVersion": 1,
  "allowance": {
    "tier": "Muse Code High Usage",
    "window": {
      "usedPercent": 0,
      "resetsAtMs": 1794810395000
    },
    "weekly": {
      "usedPercent": 0,
      "resetsAtMs": 1795392000000
    },
    "asOfMs": 1794792395910,
    "source": "mint"
  },
  "reason": null,
  "hint": null
}
```

The provider reported `usedPercent` as zero after the small interaction.

Tiny Capacity Lab must preserve that reported value rather than infer that the
interaction consumed exactly zero capacity. The provider may expose capacity
at a coarser precision than an individual small request.

## Relevant structured fields

Top-level fields observed:

```text
schemaVersion
allowance
reason
hint
```

When `allowance` is present, useful fields include:

```text
tier
window
weekly
asOfMs
source
```

Observed five-hour window fields:

```text
allowance.window.usedPercent
allowance.window.resetsAtMs
```

Observed weekly window fields:

```text
allowance.weekly.usedPercent
allowance.weekly.resetsAtMs
```

## Observation-state implications

The Muse adapter must distinguish at least:

```text
AVAILABLE
NO_OBSERVATION
ERROR
```

`AVAILABLE` means a valid allowance object was reported.

`NO_OBSERVATION` means the provider command returned successfully but
`allowance` was null. Provider `reason` and `hint` should be retained.

`ERROR` is reserved for command failure, unavailable CLI, malformed output, or
other conditions where a valid provider response cannot be obtained.

A successful `allowance: null` response is not an error.

## Provenance and freshness

Tiny Capacity Lab should preserve:

```text
allowance.tier
allowance.asOfMs
allowance.source
```

The application should also record its own local collection timestamp.

Provider observation time and Tiny Capacity Lab collection time are different
facts and must remain distinguishable.

## Reset-time normalization

Muse reports reset times as epoch milliseconds:

```text
resetsAtMs
```

Tiny Capacity Lab may derive a normalized absolute reset timestamp while
retaining the original provider value or its provenance.

A derived value must remain distinguishable from a provider-reported value.

## Quota-consumption boundary

Experiment 0001 uses:

```text
muse usage --json
```

as the quota observation interface.

The model-consuming `muse exec` probing approach identified during prior-art
research is deliberately excluded from v0.1.

Tiny Capacity Lab must not make an LLM/model request merely to determine
remaining capacity.

## Authentication boundary

Tiny Capacity Lab did not inspect, copy, store, or refresh Muse credentials.

Authentication remained the responsibility of the installed Muse CLI.

## Privacy

No prompt content, source code, credentials, account identifier, or other
personal provider state is included in this evidence record.

The one Muse interaction used only to establish the post-activity quota state
is not reproduced here.

## Result

The Muse CLI structured quota interface is suitable for continued Experiment
0001 evaluation.

The experiment directly observed both:

```text
successful query with no allowance observation
```

and:

```text
successful query with structured allowance data
```

This demonstrates that missing allowance information is a valid provider state
that Tiny Capacity Lab must represent explicitly rather than convert into an
invented capacity percentage.
