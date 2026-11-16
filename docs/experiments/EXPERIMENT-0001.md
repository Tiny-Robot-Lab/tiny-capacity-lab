# Experiment 0001: Observe AI Development Capacity

## Question

Can Tiny Capacity Lab obtain trustworthy, current capacity information from
the AI development tools I actually use through their existing local CLI
interfaces, without handling provider credentials directly and without
consuming model quota merely to measure quota?

## Initial scope

Experiment with two providers:

- Muse Code
- Antigravity

Tiny Capacity Lab is a separate Tiny Robot Lab project. It is not part of
Tiny Agent Lab.

## Platform scope

Experiment 0001 is intentionally macOS-only.

The initial development and validation platform is Tom's Mac.

This keeps the experiment focused on provider capacity extraction and
normalization rather than cross-platform packaging.

Windows and Linux support are explicitly out of scope for v0.1.

## Prior art

Before implementation, the public `aqua5230/usage` project was studied as
prior art at commit `1eea055`.

The purpose of that review was to understand existing data-extraction
approaches and provider behavior, not to copy the application.

The research identified two promising structured CLI interfaces:

```text
muse usage --json

agy -p /usage --output-format json
```

For this experiment, Tiny Capacity Lab will independently validate and use
provider CLI behavior rather than copy upstream provider implementation code.

## v0.1 principles

Keep it tiny.

- Use structured provider CLI output where available.
- Reuse the user's existing provider authentication through the provider CLI.
- Do not read, copy, store, or refresh provider credentials.
- Do not call undocumented provider APIs.
- Do not scrape human-formatted terminal output when structured output exists.
- Do not make an LLM/model call merely to discover remaining quota.
- Do not fabricate missing reset times or capacity values.
- Preserve provenance and freshness.
- Keep providers isolated so one failure does not hide other observations.
- Local only.
- No autonomous tool routing.

## Muse observation

Preferred source:

```text
muse usage --json
```

Prior-art research indicates that current Muse CLI output can provide
structured allowance data for:

- five-hour usage
- weekly usage
- reset timestamps
- subscription tier
- provider observation metadata

Experiment 0001 will validate the actual output produced on this Mac before
fixing an application contract around it.

The older model-consuming `muse exec` probing approach is explicitly out of
scope for v0.1.

## Antigravity observation

Preferred source:

```text
agy -p /usage --output-format json
```

Prior-art research indicates that this can expose separate capacity groups,
including:

- Gemini models
- Claude and GPT models
- Gemini 4 Argon

Different groups may expose different quota windows. Tiny Capacity Lab must
preserve what the provider reports rather than assume every group has both a
five-hour and weekly window.

Direct Google quota APIs and OAuth credential handling are out of scope for
v0.1.

## Proposed normalized observation

The internal representation should preserve at least:

```text
schema_version
provider
quota_group
window
used_percent
remaining_percent
resets_at
resets_in_seconds
provider_observed_at
collected_at
source
freshness
```

Unknown information remains unknown.

Provider-reported values must be distinguishable from values derived by Tiny
Capacity Lab.

## First prototype

The first prototype does only this:

```text
Muse CLI -----------+
                    +--> parse structured JSON
Antigravity CLI ----+
                          |
                          v
                    normalize observations
                          |
                          v
                      local display
```

Manual refresh is sufficient.

No daemon.
No background polling.
No hosted service.
No accounts.
No cloud infrastructure.
No routing advisor.
No permanent provider-specific credential storage.

## Evidence to collect

For each provider:

- exact CLI version
- sanitized example output/schema
- whether invocation changes measured quota
- execution duration
- successful and unsuccessful parse cases
- behavior while signed out or unavailable
- provider observation time, where available
- Tiny Capacity Lab collection time
- reset-window semantics observed in practice

Raw evidence must not include credentials, prompts, source code, personal
information, or other sensitive provider state.

## Success criteria

Experiment 0001 succeeds when:

1. Muse capacity can be queried through its structured CLI interface.
2. Antigravity capacity can be queried through its structured CLI interface.
3. Both can be represented through one small normalized observation model.
4. Neither adapter handles provider credentials directly.
5. Merely viewing previously collected Tiny Capacity Lab data consumes no
   model quota.
6. Provider failures are represented honestly rather than replaced by
   invented data.
7. The experiment is reproducible and documented.

## Explicit non-goals

Experiment 0001 does not:

- recommend which model or coding agent to use
- score model quality
- correlate quota with engineering outcomes
- autonomously route development work
- monitor providers continuously
- support every AI development tool
- reproduce the full feature set of existing quota-monitoring applications

Those capabilities require evidence from later experiments.

## Longer-term hypothesis

Capacity alone is not the interesting problem.

A later Tiny Capacity Lab experiment may investigate whether local evidence
about:

- task type
- tool/model used
- capacity consumed
- elapsed time
- independent review findings
- rework required
- test/CI outcome
- human acceptance

can support useful advisory recommendations about which development tool is a
good fit for the next task.

Any recommendation remains advisory to the human.

## Reproducibility

Tiny Capacity Lab follows the Tiny Robot Lab experiment model:

- working code and configuration
- reproducible instructions
- actual evidence
- known limitations
- expected outputs
- troubleshooting guidance
- teardown/cleanup where applicable
- lessons learned

A permanent hosted service is not required for this experiment.
