# Experiment 0001 Evidence: Antigravity quota schema

## Observation

Tiny Capacity Lab inspected the structured quota output produced by the
locally installed Antigravity CLI on the macOS experiment system.

Command:
```text
agy -p /usage --output-format json
```

## Observed behavior

The command completed successfully and returned structured JSON.

The command reported:

```text
status: SUCCESS
duration_seconds: 0
num_turns: 0
```

The returned usage object reported:

```text
input_tokens: 0
output_tokens: 0
thinking_tokens: 0
cache_read_tokens: 0
total_tokens: 0
```

For this observation, querying Antigravity capacity therefore reported no
model-token consumption.

## Observed quota groups

The response contained two quota groups.

### Gemini Models

Observed model description:

```text
Gemini 3.8 Flash
```

Observed quota windows:

```text
weekly
5h
```

### Claude and GPT models

Observed model description:

```text
Claude Sonnet 4.6
Claude Opus 4.6
GPT-OSS 120B
```

Observed quota windows:

```text
weekly
5h
```

No other quota group was present in this observation.

Tiny Capacity Lab must not interpret an absent quota group as zero remaining
capacity. Absence means only that the group was not present in the provider
response.

## Relevant structured fields

The useful provider data was available beneath:

```text
command.data.groups[]
```

Each observed group contained fields including:

```text
name
description
buckets[]
```

Each quota bucket contained fields including:

```text
id
name
window
remaining_fraction
reset_time
```

The human-readable `response` field is not required for extraction.

## Normalization implications

Tiny Capacity Lab can derive:

```text
remaining_percent = remaining_fraction * 100
used_percent = 100 - remaining_percent
```

The original provider-reported `remaining_fraction` and `reset_time` should
remain distinguishable from values derived by Tiny Capacity Lab.

Quota groups must be discovered from the response rather than hard-coded.

## Authentication boundary

Tiny Capacity Lab did not inspect, copy, store, or refresh Antigravity
credentials.

Authentication remained the responsibility of the installed Antigravity CLI.

## Privacy

No prompt content, source code, credentials, account identifier, or other
personal provider state is included in this evidence record.

## Result

The Antigravity CLI structured quota interface is suitable for continued
Experiment 0001 evaluation.

It provides the capacity information needed for a first direct Antigravity
adapter without requiring Tiny Capacity Lab to handle provider credentials or
parse human-formatted terminal output.
