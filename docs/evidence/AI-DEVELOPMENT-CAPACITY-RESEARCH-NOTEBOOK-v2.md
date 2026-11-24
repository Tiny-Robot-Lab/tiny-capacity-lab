# Tiny Capacity Lab Research Notebook v2

## Purpose and evidence rules

This notebook (v2) is a consolidated, decision-ready working research notebook synthesized from the raw experimental records of Tiny Capacity Lab. It does not replace the raw historical observations; rather, it distills durable engineering findings, operational policies, consolidated task outcomes, and cross-task analyses into an accessible, working reference.

Evidence rules governing this notebook:

- **Observation vs. cost**: Provider-reported capacity represents observed quota metrics (percentages, fractions, credits), not financial cost or direct compute expenditure.
- **Window independence**: Rolling five-hour allowance windows and fixed weekly quota windows operate independently; consumption in one does not imply proportional consumption in the other.
- **Reset boundaries are hard fences**: Never subtract or calculate net differences across reset boundaries.
- **Workload indicators**: Arithmetic sums across distinct reset segments do not represent continuous window utilization; they may serve only as explicitly labeled accumulated-workload indicators.
- **Non-monotonic readings preserved**: Observations where remaining capacity increases unexpectedly or resets shift are recorded honestly without inventing reconciliation mechanisms or external causes.
- **Missing data remains missing**: Unknown, missing, or unobserved metrics remain unknown; zero usage, full capacity, or arbitrary defaults must never be fabricated.
- **Provenance preservation**: Provider-reported metrics and derived values (such as percentages calculated from fractions) must remain clearly distinguishable.
- **Outcome over quota**: Task value is evaluated using verified engineering outcomes, test suites, and rework evidence, not quota movement alone.
- **Claims require verification**: Agent completion claims are hypotheses until independently verified by automated test suites, static analysis, or human review.
- **Final accepted disposition**: For synthesis purposes, the final accepted human disposition supersedes interim or superseded checkpoints, while the raw interim history remains intact in v1.

## Archive boundary

Detailed observations collected before this notebook are preserved in:

`AI-DEVELOPMENT-CAPACITY-RESEARCH-NOTEBOOK.md`

This v2 notebook carries forward consolidated findings and final dispositions.
The v1 notebook remains authoritative for raw historical checkpoints.

## Durable findings

### Capacity measurement

- **Zero-overhead querying**: Native CLI structured interfaces (`agy -p /usage --output-format json` and `muse usage --json`) reliably report capacity without consuming model tokens or invocation quota.
- **Provider measurement anomalies**: Provider quota systems exhibit non-monotonic behavior. In LANRoster #41, Gemini weekly remaining capacity increased by 0.5262 percentage points between checkpoints without reset; in #224, it increased by 0.3710 percentage points. Preserving raw provider observations without fabricating reconciliation causes is critical for trustworthy measurement.
- **Incommensurability of units**: Antigravity percentages, Muse percentages, and Copilot Fusion credits reflect disparate metering models. Attempting to convert them to equivalent token counts, dollars, or unified units creates false precision.

### Reset-window handling

- **Independent cadence**: Rolling 5-hour windows reset multiple times per day, while weekly windows follow distinct fixed schedules.
- **Cross-reset invalidity**: Calculating quota consumption across a reset boundary produces mathematically invalid results. Multi-session tasks crossing reset boundaries must be segmented into distinct measurement epochs.
- **Accumulated workload accounting**: Adding percentages across reset boundaries is valid only as a rough indicator of total task effort across sessions, never as a measure of peak utilization against a single allowance.

### Tool and model selection

- **Risk-aligned routing**: Tool and model choices should match the architectural and security risk of the task, rather than developer familiarity or transient promotional quotas.
- **High-reasoning leverage**: High-reasoning modes (Gemini 3.8 Flash High, Muse Spark 1.3 High, Muse Neon 1.0 High) proved essential for intricate architectural and security tasks (such as atomic Redis Lua scripting and network boundary design).
- **Read-only architecture inspections**: Read-only architectural and test-gap inspections (such as #224) consume minimal quota (<1% 5-hour window) while yielding comprehensive acceptance matrices and gap identification that prevent expensive implementation rework.

### Human verification

- **Agent completion reports are claims**: Agents frequently report tasks as complete while omitting critical edge cases, grant-scoping invariants, or infrastructure seams.
- **Targeted human review**: Direct human inspection consistently identified critical architectural defects before commit, including assignment-scoped grant leakage in #220, public IPv4 risks in #13, and raw delimiter misinterpretation in #41.
- **Bounded correction passes**: Providing focused, bounded human steering on uncommitted branches produced high-quality code and robust test coverage without open-ended agent churn.

### Independent review

- **Cross-model review efficacy**: Independent adversarial reviews conducted by a different model family (e.g. Gemini 4 Argon reviewing Copilot Fusion on ADR-0007; Muse Neon reviewing Antigravity on #13; Muse and Fusion reviewing Gemini on #221; Fusion reviewing Muse on #222) consistently surfaced critical failure modes that the implementing agent rationalized or missed.
- **Adversarial framing**: Review prompts instructed to find omissions or adopt an adversarial posture ("Reject with prejudice" in #13, concurrency edge probing in #221 and #222). Independent reviewers using distinct tools and roles reduced single-reviewer confirmation risk and repeatedly identified non-overlapping defects.

### Real infrastructure validation

- **In-memory fakes conceal atomicity defects**: In-memory mocks and fake Redis implementations repeatedly passed tests despite underlying Lua syntax and type mismatches.
- **Real Redis 7 enforcement**: Running tests against live Redis 7 (DB 15) exposed critical Lua integer-vs-string type coercion errors (#221) and race conditions in child completion notification (#222). Real infrastructure validation is required where acceptance depends on infrastructure-specific semantics not faithfully exercised by deterministic doubles.

### Session/context quality

- **Context contamination**: Extended interactive sessions spanning multiple iterations accumulate stale assumptions and instruction drift.
- **Fresh-session boundary benefits**: Starting fresh sessions for major task phases or independent review rounds cleared context clutter, eliminated hallucinations of superseded contracts, and improved model adherence to rigid constraints.

### Documentation and visual workflows

- **Terminal and visual deception**: Terminal rendering and markdown viewers can visually distort source characters (e.g., ASCII backticks U+0060 appearing as backslashes in #41). Rigorous byte-level inspection and character-code regression tests are necessary when diagnosing syntax issues.
- **Privacy hazards in documentation**: Documentation tasks carry a high risk of leaking private environment details, local IP addresses, and subnets (#10) unless explicit privacy constraints and automated review are enforced.

## Accepted operating policies

1. **Risk-based tool selection**: Choose tools, models, and reasoning tiers based on verified task risk and empirical evidence, not recent habit or quota availability.
2. **Mandatory independent review**: High-risk architectural, protocol, or security designs require adversarial review by an independent model or tool family before acceptance.
3. **Real infrastructure acceptance**: Real infrastructure validation is required where acceptance depends on infrastructure-specific semantics not faithfully exercised by deterministic doubles.
4. **Separation of review and implementation roles**: Avoid having the same agent session implement code and evaluate its own readiness; keep reviewer and implementer roles distinct.
5. **Frozen acceptance boundaries**: Define explicit acceptance criteria, file boundaries, and non-goals prior to task execution; reject unprompted scope creep or opportunistic refactoring.
6. **Bounded correction and stopping rules**: Limit agent correction passes to bounded, single-turn prompts with explicit stopping rules; halt immediately upon unexpected failure or contract ambiguity.
7. **Human maintainer authority**: The human maintainer retains sole authority for architecture decisions, security tradeoffs, and final merge approval. Agent completion claims are never accepted without verification.
8. **Verification preceding staging**: Code and documentation must pass automated tests, linting, and working-tree clean checks before staging; no file is staged or committed on unverified agent self-reports.
9. **Fresh-session preference**: Prefer fresh, clean sessions when initiating new tasks, major phases, or independent reviews to prevent context degradation.
10. **Pre- and post-task capacity logging**: Record structured quota readings immediately before and after meaningful engineering tasks where practical.
11. **No frivolous consumption**: Never consume provider capacity merely to use up expiring quota or idle windows; preserve capacity for grounded engineering work.

## Consolidated historical task index

| Task | Primary tools | Work type | Final disposition | Durable lesson |
| :--- | :--- | :--- | :--- | :--- |
| ADR-0007 | Copilot Fusion (GPT-6 Luna); Reviewer: Antigravity (Gemini 4 Argon High) | Architecture documentation | Accepted & merged | Independent adversarial review prevents drafting architectural abstractions detached from live repository code. |
| Tiny Agent Lab #219 | Antigravity (Gemini High) | Storage foundation & persistence | Accepted & merged (PR #226) | Foundational persistence requires rigid immutability and atomic storage contracts before implementing orchestration. |
| Tiny Agent Lab #220 | Antigravity (Gemini High); Pyrefly inspection | Protocol runtime & authentication | Accepted & merged | Complex security protocols require multi-pass human review; agents consistently miss grant-scoping and credential defaults on initial passes. |
| Tiny Agent Lab #221 | Antigravity (Gemini 3.8 Flash High); Reviewers: Muse Code (Spark 1.3 High), Copilot Fusion | Distributed coordination & delegation | Accepted & merged | In-memory fakes hide Redis Lua type-coercion bugs; real infrastructure validation and multi-model review are essential. |
| Tiny Agent Lab #222 | Muse Code (Spark 1.3 High); Reviewer: Copilot Fusion | Authenticated child completion & execution runtime | Accepted & merged | Adversarial review and real-Redis validation ensure authenticated completion fencing and replay safety. |
| Tiny Agent Lab #223 | Antigravity (Gemini 3.8 Flash Medium); Reviewer: Copilot Fusion | Continuation resumption & wiring | Accepted & merged | Resumption paths require explicit fail-closed timeout and expiration recovery; PR-readiness review catches omitted operational edges. |
| Tiny Agent Lab #224 | Antigravity (Gemini 3.8 Flash High); Reviewer: Muse Code (Spark 1.3 High) | Architecture & test-gap inspection | Inspection and review recorded in v1; final merge pending post-archive recording | Read-only architecture inspection consumes minimal quota (<1% 5h) while identifying structural gaps before costly coding. |
| Tiny Capacity Lab Antigravity adapter | Antigravity (Gemini Medium); Human review | Normalization adapter & contracts | Accepted & merged (PR #2) | Provider formatting quirks (e.g. bucket prefixes) must not be treated as authoritative; preserve exact provider arithmetic and fail closed. |
| Tiny Capacity Lab Muse adapter | Antigravity (Gemini Medium); Human review | Normalization adapter & contracts | Accepted & validated | Shared contracts must remain provider-neutral and honest; never coerce one provider's native metrics into another's schema. |
| LANRoster #10 | Muse Code (Medium effort); Human review | Documentation alignment | Accepted & merged | Documentation tasks require strict privacy boundaries to prevent accidental leakage of local network and environment details. |
| LANRoster #11 | Muse Code (Spark 1.3 Medium) | Packaging & rootless CI | Accepted & merged | Tooling and packaging infrastructure changes must be strictly isolated from application runtime logic. |
| LANRoster #12 | Antigravity (Gemini 3.8 Flash High) | Security binding configuration | Accepted & merged | Network-facing applications must default to localhost-first bindings and be tested without live network side effects. |
| LANRoster #13 | Antigravity (Gemini 3.8 Flash High); Reviewer: Muse Code (Neon 1.0 High) | Security architecture (ADR 0001) | Accepted & merged | Adversarial review ("Reject with prejudice") is critical for security architecture; caught public-IP scanning risks before implementation. |
| LANRoster #41 | Antigravity (Gemini 3.8 Flash Medium) | Bug diagnosis & markup repair | Accepted & merged | Inspect raw code points and UTF-8 bytes directly; terminal rendering can deceive both human and automated inspectors. |
| Cross-repository GitHub governance audit | Antigravity (Gemini 3.8 Flash High); Human maintainer | Security & governance audit | Accepted (Audit matrix delivered) | Governance audits must be grounded in verified repository API evidence rather than generic boilerplate checklists. |

## Consolidated task observations

### ADR-0007: Durable Task Continuations

- **Task objective**: Draft prospective ADR-0007 (Durable Task Continuations and Platform-Governed Asynchronous Resumption) for Tiny Agent Lab.
- **Primary tools / roles**: GitHub Copilot Fusion (GPT-6 Luna, Fusion Standard) for drafting and revisions; Google Antigravity (Gemini 4 Argon High) for independent adversarial review; Human maintainer for live repository grounding.
- **Reset boundary**: Tracked across Copilot monthly credit ledger (186.7 $\rightarrow$ 204.0 / 1,500 credits; monthly reset Nov 30 at 4:00 PM).
- **Significant measured capacity**: Incremental credit usage: initial draft 10.0 credits (186.7 $\rightarrow$ 196.7), revision 5.1 credits (196.7 $\rightarrow$ 201.8), consistency correction 1.6 credits (201.8 $\rightarrow$ 203.4), acceptance recording 0.6 credits (203.4 $\rightarrow$ 204.0). Total consumption: 17.3 credits.
- **Most important review finding**: Independent Argon review revealed that the initial Fusion draft drifted from repository reality, assuming an in-memory orchestrator, missing active Redis Lua persistence, and ignoring existing `TaskInput`/`StageArtifact` contracts. Human maintainer enforced line-by-line reconciliation against live code.
- **Final verified outcome**: ADR-0007 accepted and recorded in the repository with complete architectural alignment to durable Redis Lua storage.
- **Durable lesson**: Architecture decisions must be grounded in live repository state; independent cross-model review prevents formalizing non-existent abstractions.
- **Raw evidence pointers**:
  - `## Task observation: Prospective ADR-0007 draft`
  - `## Revision pass`
  - `## Live-repository validation of Argon review`
  - `## Final ADR-0007 architecture revision`
  - `## Final ADR-0007 consistency correction`
  - `## ADR-0007 acceptance recording`

### Tiny Agent Lab #219: Durable Continuation Storage Foundation

- **Task objective**: Implement durable continuation storage foundation, including `TaskInput`, `StageArtifact`, `TaskContinuation`, root-authority records, canonical serialization, and atomic Redis Lua scripts.
- **Primary tools / roles**: Google Antigravity (Gemini High); Human maintainer review gates.
- **Reset boundary**: Measured within weekly quota window (reset Nov 20 at 22:52:22Z).
- **Significant measured capacity**: Gemini weekly moved from 87.82% remaining (12.18% used) to 70.34% remaining (29.66% used), consuming 17.48 percentage points. Provider query cost was 0 model tokens.
- **Most important review finding**: Multiple human review gates rejected initial mutable collections and partial writes, mandating deep immutability, canonical serialization, and atomic Lua execution with contiguous version streams.
- **Final verified outcome**: PR #226 squashed and merged after passing CI, CodeQL, and Redis concurrency/replay test suites.
- **Durable lesson**: Foundational storage and state models require strict immutability and atomic persistence contracts before higher-level workflow orchestration is introduced.
- **Raw evidence pointer**:
  - `### Antigravity capacity observation after Issue #219`

### Tiny Agent Lab #220: Authenticated Pull-Claim and Assignment

- **Task objective**: Implement authenticated pull-claim, private `TaskAssignment`, detached assignment proof, fencing, root delegation grant, wake-up hints, acknowledgement, and authenticated artifact staging.
- **Primary tools / roles**: Google Antigravity (Gemini High); Pyrefly static analysis; Human maintainer architecture review.
- **Reset boundary**: Work spanned multiple five-hour windows. Window 1 consumed 16.62 percentage points; Window 2 consumed 11.45 percentage points; subsequent post-reset hardening consumed 46.36 percentage points of a fresh 5-hour window.
- **Significant measured capacity**: Initial pass consumed 7.73 percentage points weekly; complete post-reset hardening segment consumed 13.96 percentage points weekly and 46.36 percentage points in the active 5-hour window.
- **Most important review finding**: Human inspection detected critical security and lifecycle defects before commit: authority grants were incorrectly scoped to the root session rather than the individual assignment, fixed production secret defaults were present, and continuation versions lacked integer-only type contracts.
- **Final verified outcome**: Feature branch hardened through focused correction passes, achieving assignment-scoped immutable grants, constant-time proof verification, and strict type safety before merge.
- **Durable lesson**: Broad runtime security PRs cannot be validated in a single pass; human review of grant lifecycles and secret handling catches critical vulnerabilities that agent self-validation overlooks.
- **Raw evidence pointers**:
  - `#220 Phase 1 starting checkpoint`
  - `### Issue #220 interim Antigravity checkpoint`
  - `### Issue #220 Pyrefly and security inspection checkpoint`
  - `### Issue #220 cumulative Antigravity capacity observation`
  - `#### Issue #220 consolidated correction pass`
  - `#### Issue #220 Pyrefly and correction-safety review`
  - `#### Issue #220 continuation-version numeric hardening`
  - `#### Issue #220 continuation-version type-contract correction`
  - `#### Issue #220 final capability-boundary corrections`
  - `#### Issue #220 RequiredCapabilityRecord contract hardening`

### Tiny Agent Lab #221: Atomic Delegation and Pending Child Claimability

- **Task objective**: Implement atomic Research $\rightarrow$ Analysis delegation acceptance, claimable pending child generation, parent checkpointing and yielding, single-wave delegation grant consumption, and deterministic replay.
- **Primary tools / roles**: Google Antigravity (Gemini 3.8 Flash High); independent reviewers: Muse Code (Spark 1.3 High) and Copilot Fusion (GPT-6 Luna Standard).
- **Reset boundary**: Spanned pre-reset and post-reset 5-hour segments. Weekly capacity moved from 78.50% to 67.57% remaining (10.93 percentage points consumed).
- **Significant measured capacity**: Antigravity Gemini weekly: 10.93 percentage points consumed across 7 phases; 5-hour window 1: 26.41 percentage points; 5-hour window 2: 23.36 percentage points. Muse review: 19% 5h used, 4% weekly used. Fusion review: 2 review attempts (~20 credits).
- **Most important review finding**: Human maintainer mandated testing against real Redis 7 (DB 15), exposing Lua string-vs-int parsing errors that in-memory fakes passed. Muse review exposed duplicate-request idempotency gaps and unhandled resume timeouts; Fusion review identified race conditions in grant verification.
- **Final verified outcome**: PR accepted and merged after 7 phases, real-Redis test execution, and full multi-reviewer remediation.
- **Durable lesson**: In-memory test fakes mask Redis Lua type-coercion bugs; real infrastructure validation is required where acceptance depends on infrastructure-specific semantics not faithfully exercised by deterministic doubles.
- **Raw evidence pointers**:
  - `## Task observation: Tiny Agent Lab issue #221`
  - `### Baseline before issue #221 work`
  - `## Phase 1: Repository-grounded implementation planning` through `## Phase 6: Redis-specific validation correction`
  - `## Aggregate capacity accounting`
  - `### Independent Muse Code review`
  - `### Phase 7: Muse-findings correction`
  - `### Initial Copilot Fusion review attempt`
  - `### Copilot Fusion final review`
  - `### Post-reset Fusion-findings correction`

### Tiny Agent Lab #222: Child Claim and Execution Runtime

- **Task objective**: Implement Analysis child task claim, authenticated and fenced completion, canonical TaskResult / TerminalOutcome consistency, Analysis runtime migration, replay safety, and real-Redis completion validation.
- **Primary tools / roles**: Muse Code (muse-spark-1.3 High reasoning) for implementation; Copilot Fusion for independent adversarial review.
- **Reset boundary**: Tracked across two Muse 5-hour windows. Initial implementation consumed 16 percentage points (0% $\rightarrow$ 16%) 5h and 6 percentage points weekly (15% $\rightarrow$ 21%); correction pass consumed 20 percentage points in a fresh 5h window.
- **Significant measured capacity**: Muse: 16% + 20% across two 5-hour windows; Copilot Fusion: 2 adversarial review sessions.
- **Most important review finding**: Fusion adversarial review identified race conditions in child completion notification and missing replay safety protections. Human review enforced authenticated completion fencing, canonical TaskResult / TerminalOutcome consistency, and real-Redis completion validation.
- **Final verified outcome**: Implementation accepted after Muse completed Fusion-directed corrections and verified real-Redis integration.
- **Durable lesson**: Independent reviewers using distinct tools and roles reduced single-reviewer confirmation risk and repeatedly identified non-overlapping defects in child completion and replay safety.
- **Raw evidence pointers**:
  - `### Issue #222 Muse implementation`
  - `### Issue #222 Muse real-Redis migration correction`
  - `### Issue #222 Fusion adversarial review`
  - `### Issue #222 Muse correction of Fusion findings`
  - `### Issue #222 focused Fusion follow-up review`
  - `### Issue #222 final Muse correction`

### Tiny Agent Lab #223: Resumed Research Continuation and Production Wiring

- **Task objective**: Close resumed Research continuation production-wiring gaps, implement governed continuation-context retrieval, add dedicated real-Redis tests, and validate timeout recovery.
- **Primary tools / roles**: Google Antigravity (Gemini 3.8 Flash Medium); Copilot Fusion for PR-readiness review.
- **Reset boundary**: Measured within single Antigravity Gemini window.
- **Significant measured capacity**: Antigravity Gemini 5-hour consumption moderate (~8-12%); Fusion consumed 1 PR-readiness review run.
- **Most important review finding**: Fusion review caught missing recovery logic for expired continuations and omitted telemetry attributes; Gemini implemented targeted corrections prior to staging.
- **Final verified outcome**: Resumed Research continuation wiring verified fail-closed, real-Redis tests passed, and PR finalized.
- **Durable lesson**: Resumption and continuation mechanisms must explicitly handle expiration and timeout recovery paths before production wiring is considered complete.
- **Raw evidence pointers**:
  - `### Issue #223 Gemini continuation and production-wiring pass`
  - `### Issue #223 Fusion PR-readiness review`
  - `### Issue #223 Gemini correction of Fusion findings`

### Tiny Agent Lab #224: Research-to-Analysis Architecture and Gap Inspection

- **Task objective**: Perform read-only inspection of Research $\rightarrow$ Analysis $\rightarrow$ Research lifecycle, establish acceptance matrix, and identify missing seams without mutating the repository.
- **Primary tools / roles**: Google Antigravity (Gemini 3.8 Flash High) for inspection; Muse Code (muse-spark-1.3 High) for independent review.
- **Reset boundary**: Observed non-monotonic provider measurement: Gemini weekly remaining increased by +0.37 percentage points (69.60% $\rightarrow$ 69.97%), while five-hour capacity consumed 0.64 percentage points (76.55% $\rightarrow$ 75.91%).
- **Significant measured capacity**: Gemini 5-hour consumed 0.64 percentage points; Muse review consumed 5% of 5-hour window and 1% of weekly allowance.
- **Most important review finding**: Gemini identified missing pull-claim and delegation seams and absent 3-outcome orchestration tests. Muse issued "Accept with changes", establishing mandatory prerequisites for proposal replay and leakage scans.
- **Final verified outcome**: v1 contains inspection and independent-review evidence for #224, but ends before the final merged #224 disposition. The final #224 outcome is post-archive evidence to be recorded later in v2 New chronological observations.
- **Durable lesson**: Read-only inspection passes consume minimal quota (<1% 5h) while providing high-leverage architectural clarity that prevents implementation waste.
- **Raw evidence pointers**:
  - `### Issue #224 read-only architecture and test-gap inspection`
  - `### Issue #224 independent Muse review`

### Tiny Capacity Lab Antigravity Adapter

- **Task objective**: Implement bounded Experiment 0001 vertical slice: normalize structured Antigravity quota responses (`agy -p /usage --output-format json`) into Capacity Observation v1 immutable models.
- **Primary tools / roles**: Google Antigravity (Gemini Medium); Human maintainer review.
- **Reset boundary**: Gemini 5-hour reset occurred between initial pass and correction pass; initial pass consumed 1.72% in fresh 5h window, weekly remaining 86.53%.
- **Significant measured capacity**: Gemini weekly consumed ~1.7 to 2.5 percentage points across initial pass and correction pass; query cost was 0 model tokens.
- **Most important review finding**: Human review rejected bucket-prefix group ID inference, removed 4-decimal rounding (enforced exact floating-point arithmetic), eliminated dual return/raise error behavior (enforced fail-fast `AntigravityResponseError`), rejected naive datetimes, and eliminated speculative extraction of undocumented timestamps.
- **Final verified outcome**: Adapter accepted and merged (PR #2); verified with 45 unit tests, ruff clean, and zero staged changes.
- **Durable lesson**: Do not infer architectural semantics from provider formatting quirks (bucket prefixes); preserve exact provider arithmetic and fail closed on invalid provider output.
- **Raw evidence pointers**:
  - `## Tiny Capacity Lab Antigravity adapter: first implementation pass`
  - `### Antigravity adapter focused correction pass`

### Tiny Capacity Lab Muse Adapter

- **Task objective**: Implement second bounded Experiment 0001 vertical slice: normalize structured Muse Code responses (`muse usage --json`) into shared Capacity Observation v1 models.
- **Primary tools / roles**: Google Antigravity (Gemini Medium); Human maintainer review.
- **Reset boundary**: Gemini weekly remaining moved from ~85.68% to ~84.2%.
- **Significant measured capacity**: Moderate Antigravity quota consumed across initial pass and correction pass; zero model tokens consumed by CLI queries.
- **Most important review finding**: Human maintainer required generalizing `ProviderWindowValue` provenance (`used_percent` and `resets_at_ms` without fabricating `remaining_fraction`), normalizing reset timestamps to timezone-aware UTC datetimes across both adapters, field-aware epoch conversion error handling, and immutable defensive `MappingProxyType` metadata.
- **Final verified outcome**: Muse adapter accepted; verified with 108 tests passing across Antigravity, Muse, and shared contract models.
- **Durable lesson**: Shared contracts must remain provider-neutral and honest; never coerce one provider's native metrics into another's schema.
- **Raw evidence pointers**:
  - `## Tiny Capacity Lab Muse adapter: first implementation pass`
  - `### Muse adapter and shared-contract correction pass`

### LANRoster #10: Documentation Alignment

- **Task objective**: Align LANRoster documentation with released v0.2.0 implementation without altering `ROADMAP.md` or application code.
- **Primary tools / roles**: Muse Code (Medium effort); Human maintainer review.
- **Reset boundary**: Measured within Muse 5-hour window.
- **Significant measured capacity**: Initial pass consumed 12% 5-hour used, 1% weekly used; correction pass consumed 10% 5-hour used, 1% weekly used.
- **Most important review finding**: Human maintainer rejected unauthorized `ROADMAP.md` edits, caught accidental leakage of private local subnet/IP addresses in example markdown, and enforced strict localhost-only documentation.
- **Final verified outcome**: Documentation aligned, privacy leaks remediated, and branch merged.
- **Durable lesson**: Documentation tasks require strict privacy boundaries; language models readily leak real local environment details unless explicitly constrained.
- **Raw evidence pointers**:
  - `## Task observation: LANRoster issue #10 documentation alignment`
  - `### Human-directed privacy correction pass`

### LANRoster #11: Packaging and CI Tooling

- **Task objective**: Add standard Python packaging (`pyproject.toml`, build tooling), reproducible development environment, rootless CI matrix, and distributable artifact validation.
- **Primary tools / roles**: Muse Code (muse-spark-1.3 Medium effort).
- **Reset boundary**: Measured within single Muse 5-hour window.
- **Significant measured capacity**: 5-hour window used: 11%; weekly window used: 2%.
- **Most important review finding**: Human maintainer required pure tooling configuration without touching application scanning code, ensuring all tests run rootless in containerized CI.
- **Final verified outcome**: Packaging and CI infrastructure accepted and merged; passing clean on GitHub Actions.
- **Durable lesson**: Packaging and CI modernizations should be decoupled from application runtime changes to maintain clean auditability.
- **Raw evidence pointer**:
  - `## Task observation: LANRoster issue #11 packaging and CI`

### LANRoster #12: Localhost-First Binding

- **Task objective**: Change LANRoster web server default binding to localhost (127.0.0.1) and require explicit `--lan` flag for 0.0.0.0 network exposure.
- **Primary tools / roles**: Google Antigravity (Gemini 3.8 Flash High reasoning).
- **Reset boundary**: Single Gemini 5-hour window.
- **Significant measured capacity**: Gemini 5-hour consumed 3.29 percentage points; weekly consumed 1.13 percentage points.
- **Most important review finding**: Verified localhost-first binding and CLI options through unit tests without spawning live network-scanning processes.
- **Final verified outcome**: Feature accepted and merged; verified secure default configuration.
- **Durable lesson**: Security defaults must be fail-safe (localhost-first) and validated through automated unit tests without live network probing.
- **Raw evidence pointer**:
  - `## Task observation: LANRoster issue #12 localhost-first binding`

### LANRoster #13: Allowed Subnet and Scan-Target Security Architecture

- **Task objective**: Define allowed subnet and scan-target policy (ADR 0001); obtain independent adversarial review and reconcile findings.
- **Primary tools / roles**: Google Antigravity (Gemini 3.8 Flash High) for drafting and refinement; Muse Code (muse-neon-1.0 High) for independent review.
- **Reset boundary**: Antigravity Gemini weekly moved from 81.06% to 79.52% (~1.53 percentage points consumed across 4 phases).
- **Significant measured capacity**: Antigravity: 1.53 percentage points weekly; Muse Neon: 2 review passes.
- **Most important review finding**: Independent Neon review issued "Reject with prejudice" on the initial ADR draft for failing to forbid public IPv4, allowing arbitrary subnet sizes (/8), and omitting carrier-grade NAT restrictions. Human maintainer directed full reconciliation: constrained subnets to RFC 1918 private /24-/16, banned public IPs, and required explicit interface binding. Neon review approved revised ADR.
- **Final verified outcome**: ADR 0001 accepted and merged; established strict security envelope before scanning implementation.
- **Durable lesson**: Adversarial security reviews with strict rejection criteria are invaluable for network tools; caught dangerous public-IP scanning vectors before code was written.
- **Raw evidence pointers**:
  - `### LANRoster issue #13 ADR refinement`
  - `## Task observation: LANRoster issue #13 architecture decision`
  - `### Tool roles` through `### Final Neon verification and human decision`

### LANRoster #41: Malformed-Markup Diagnosis and Repair

- **Task objective**: Investigate and repair suspected malformed source markup (delimiters appearing corrupted in terminal displays) in LANRoster.
- **Primary tools / roles**: Google Antigravity (Gemini 3.8 Flash Medium reasoning).
- **Reset boundary**: Crossed 5-hour reset boundary; observed provider reconciliation anomaly where Gemini weekly remaining increased by +0.5262 percentage points (82.15% $\rightarrow$ 82.68%).
- **Significant measured capacity**: Gemini 5-hour consumed 3.77 percentage points; weekly consumed 1.67 percentage points.
- **Most important review finding**: Initial diagnosis suspected corrupted backslash escaping. Raw byte-level inspection revealed characters were standard ASCII backticks (U+0060, byte 0x60) rendered strangely by terminal styling, but root cause was unescaped template interpolation causing malformed DOM markup. Added byte-level regression tests.
- **Final verified outcome**: Focused bugfix accepted and merged without modifying network scanning logic.
- **Durable lesson**: Inspect raw code points and bytes directly when diagnosing syntax anomalies; terminal presentation can deceive both human developers and language models.
- **Raw evidence pointers**:
  - `## Capacity checkpoint: LANRoster issue #41 malformed-markup repair` (both entries)
  - `## Task observation: LANRoster issue #41 malformed-markup repair`
  - `## Task observation: LANRoster issue #41 malformed-markup investigation`

### Cross-Repository GitHub Governance Audit

- **Task objective**: Conduct read-only audit of GitHub security, branch protection, CodeQL, and merge governance across 4 repositories (autonomous-agent-lab, tiny-capacity-lab, tinyrobotlab-site, LANRoster).
- **Primary tools / roles**: Google Antigravity (Gemini 3.8 Flash High reasoning); Human maintainer.
- **Reset boundary**: Single Gemini 5-hour window.
- **Significant measured capacity**: Gemini 5-hour consumed ~8.4 percentage points; weekly consumed ~2.4 percentage points across initial and correction passes.
- **Most important review finding**: Initial pass generated generic recommendations based on unwarranted assumptions about deployment pipelines. Human correction pass grounded recommendations strictly in actual repository risk profiles and verified GitHub API configuration evidence.
- **Final verified outcome**: Cross-repository governance audit matrix completed; established baseline policies without mutating remote configurations.
- **Durable lesson**: Multi-repository governance audits must ground findings in repository-specific configuration evidence rather than generic boilerplate checklists.
- **Raw evidence pointers**:
  - `## Task observation: cross-repository GitHub governance audit, initial pass`
  - `### Human-directed governance-audit correction pass`

## Cross-task observations

*Note: The following observations represent comparative qualitative patterns synthesized across engineering tasks. They are observational comparisons from working developer sessions, not controlled model benchmarks.*

### Documentation versus implementation work

- Documentation and architecture tasks (such as ADR-0007, #10, and #13) consume less overall quota than deep implementation tasks, but carry high risk of subtle conceptual drift or environment leakage.
- When drafting documentation, models tend to invent idealized interfaces or formalize unverified abstractions unless explicitly grounded in live source code.
- In implementation tasks (such as #219, #220, #221, #222), quota consumption is dominated by iterative test execution, static analysis remediation, and multi-turn refactoring.

### Initial passes versus correction passes

- Initial implementation passes consistently exhibit broad structural competence but miss fine-grained boundary conditions, lifecycle invariants, and error contracts.
- Targeted, human-guided correction passes consume significantly less quota than initial passes while accounting for the majority of verified security and correctness improvements.
- Attempting to have an agent perform self-directed open-ended correction often results in churn; human maintainer steering is required to freeze boundaries and focus the edit.

### Independent-review value

- Independent reviewers using distinct tools and roles reduced single-reviewer confirmation risk and repeatedly identified non-overlapping defects.
- Reviewers from independent model families reliably identified severe flaws—such as missing Redis atomicity (#221), child completion notification race conditions and replay safety gaps (#222), and dangerous public-IP scanning allowances (#13)—that the implementing agent failed to detect during self-reflection.
- The highest-leverage reviews utilized explicit adversarial framing ("find unhandled edge cases" or "evaluate with strict rejection criteria").

### Context-confusion and fresh-session effects

- Long, multi-turn sessions (e.g. #220 and multi-phase #221) exhibited context degradation, where agents reintroduced superseded terminology or attempted to satisfy obsolete constraints.
- Initiating fresh sessions with clean working-tree baselines consistently restored strict instruction adherence and eliminated hallucinated contracts.
- Preserving an explicit boundary between implementation sessions and review sessions proved critical for objective analysis.

### Real infrastructure versus fake/in-memory validation

- In-memory test doubles and mock objects provided a false sense of security, readily passing tests that failed immediately upon execution against live infrastructure.
- In #221 and #222, live Redis 7 testing uncovered critical Lua script parsing errors, type mismatches (string vs integer in Redis keys), and timing race conditions.
- Real infrastructure validation is required where acceptance depends on infrastructure-specific semantics not faithfully exercised by deterministic doubles.

### Capacity movement versus validated outcome

- Quota consumption does not correlate with engineering value. A task consuming substantial quota (e.g., iterative refactoring during #220) may represent extensive rework of basic invariants, whereas a low-quota task (e.g., read-only inspection #224 consuming <1% 5h) can produce crucial architectural breakthroughs.
- Evaluating agent productivity by token volume or quota movement is fundamentally misleading; progress can only be measured by validated, tested engineering outcomes and low rework rates.

## Operational experiments

### Layered monitoring

Controlled failure testing was conducted against the configured external monitoring path for Tiny Agent Lab services:

- **Application-down test**: The Tiny Agent Lab Orchestrator was stopped while Cloudflare Tunnel remained active. Layer 2 external monitoring correctly detected the service failure, UptimeRobot dispatched down notifications via email, and recovery was confirmed upon Orchestrator restart.
- **Tunnel-down test**: Cloudflare Tunnel was halted while the local application remained running. Cloudflare issued tunnel-down alerts, external monitoring reported public path unavailability, and UptimeRobot dispatched alerts. Following restart, transient DNS recovery was observed before full recovery.
- **Independent notification paths**: The experiment verified that Cloudflare Tunnel and external health monitors provide independent, non-correlated failure detection boundaries.
- **Polling interval**: Monitors operated on a 5-minute polling interval; exact detection latency was treated as uninformative because events can happen at any offset in the polling cycle.
- **Final service state**: Final verification confirmed full recovery at `2026-11-24T06:38:49+00:00`, with all Compose services healthy and `https://agents.tinyrobotlab.com/health` returning `{"status":"ok"}`.

### Markdown/source fidelity

A future controlled experiment is planned to evaluate character fidelity and delimiter parsing in language model pipelines, specifically addressing edge cases where visual styling or terminal presentation diverges from underlying UTF-8 byte representations (as observed in LANRoster #41).

## Open questions and planned experiments

1. **Cross-provider capacity normalization**: Can provider quota metrics (percentages, fractions, credits) be correlated with objective engineering effort or task complexity without introducing invalid cost models?
2. **Reconciliation frequency**: What causes provider-side non-monotonic quota adjustments (such as observed capacity increases in LANRoster #41 and #224)? How frequently do providers reconcile usage ledgers?
3. **Independent review capacity justification**: When does an additional independent model review provide enough incremental evidence to justify its capacity cost?
4. **Context degradation metrics**: At what turn count or token threshold does multi-turn context degradation begin to degrade code correctness in complex architectural tasks?
5. **Infrastructure validation boundaries**: Determine which behaviors require real infrastructure validation and which remain efficiently covered by deterministic in-memory tests.

## New chronological observations

New detailed observations after the v1 archive boundary are recorded here.

## Archive and provenance

- **Authoritative archive**: `AI-DEVELOPMENT-CAPACITY-RESEARCH-NOTEBOOK.md` (v1) remains the permanent, immutable, byte-for-byte authoritative chronological ledger of raw capacity measurements and task notes.
- **Working synthesis**: `AI-DEVELOPMENT-CAPACITY-RESEARCH-NOTEBOOK-v2.md` (v2) provides a consolidated synthesis of completed tasks, durable findings, and forward-looking observations.
- **Contract separation**: Capacity Observation v1 (`docs/contracts/CAPACITY-OBSERVATION-v1.md`) is a formal software data contract and remains completely separate from this research notebook.
- **Conflict resolution**: If any statement or summary in v2 appears to conflict with raw historical checkpoints, inspect v1 before altering any conclusion.
- **No historical rewriting**: Historical observations and raw provider metrics must never be rewritten or retroactively adjusted.
