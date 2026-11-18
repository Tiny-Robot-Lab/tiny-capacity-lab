# AI Development Capacity Research Notebook

Working observations correlating AI development tasks, capacity movement, engineering outcomes, review findings, and rework.

These notes are exploratory evidence for a later Tiny Capacity Lab experiment. They are not part of the Capacity Observation v1 contract or Experiment 0001 implementation scope.

Entries are retained in their original working-note form and may contain incomplete or superseded checkpoints.

Capacity before:
- 186.7 / 1,500 credits used

Fusion routing:
- Effort: Standard
- Session: Fresh
- Fusion complexity assessment: Low
- Primary model observed: GPT-6 Luna

Task:
- Draft prospective ADR-0007
- Durable Task Continuations and Platform-Governed Asynchronous Resumption
- Repository-grounded, documentation-only
- Human acceptance: Pending
- Independent Argon review: Required


## Task observation: Prospective ADR-0007 draft

Task:
Draft prospective ADR-0007, Durable Task Continuations and
Platform-Governed Asynchronous Resumption.

Project:
Tiny Agent Lab / autonomous-agent-lab

Tool:
GitHub Copilot Fusion

Effort:
Fusion Standard

Session:
Fresh

Task type:
Repository-grounded, documentation-only architecture drafting

Repository baseline:
- Branch: docs/adr-0007-durable-task-continuations
- Commit: 7e8bfc7
- Initial working tree: clean

Capacity before:
- 186.7 / 1,500 credits used

Capacity after:
- 189.8 / 1,500 credits used
- Reset shown: Nov 30 at 4:00 PM

Observed account-credit movement:
- +3.1 credits

Fusion routing:
- Fusion complexity assessment: Low
- Primary model observed: GPT-6 Luna
- Completion model: GPT-6 Luna
- Task credits shown separately: Not observed

Outcome:
- Completed: Yes
- Files created: 1 prospective ADR
- Implementation files changed: None
- Tests changed: None
- GitHub issues changed: None
- Human accepted: Pending
- Independent Argon review: Required
- Commit/push/PR: No

Draft:
- ADR 0007 status: Proposed
- Filename:
  docs/adr/0007-durable-task-continuations-and-platform-governed-asynchronous-resumption.md
- Size: 542 lines
- New-file diff: 542 insertions
- ADR README changed: No, because no prospective-ADR index exists

Selected direction:
- durable tasks own continuation state
- agents are replaceable executors
- parent yields while child work runs
- continuation targets capability rather than agent identity
- durable completion-command stream
- trusted idempotent platform projector
- canonical child completion and safe failure outcomes
- versioned continuation claims
- narrow initial research -> analysis authority edge
- one child and one delegation wave for issue #33

Validation:
- git diff --check passed
- whitespace and final-newline checks passed
- no Markdown lint configuration found
- no tests run because change is documentation-only

Tool-execution observations:
- One validation command initially failed because `python` was unavailable;
  validation succeeded with `.venv/bin/python`.
- One patch application failed because expected text no longer matched the
  evolving draft; Luna reread the relevant ranges and applied the intended
  changes through a subsequent edit.
- Neither event produced repository drift or an unresolved validation failure.

Capacity assessment:
- Luna produced a comprehensive prospective ADR for an observed +3.1 account
  credits.
- Fusion labeled the documentation action low complexity, despite the
  underlying architectural decision being security- and consistency-sensitive.
- Independent Argon review and human acceptance remain mandatory.


## Revision pass

Capacity before:
- 189.8 / 1,500 credits used

Capacity after:
- 192.0 / 1,500 credits used
- Reset shown: Nov 30 at 4:00 PM

Observed account-credit movement:
- +2.2 credits

Combined ADR-0007 drafting:
- Initial draft: +3.1 credits
- Human-review revision: +2.2 credits
- Combined: +5.3 credits

Revision outcome:
- Completed: Yes
- Model: GPT-6 Luna
- Files changed: Only prospective ADR-0007
- Implementation/test changes: None
- GitHub issue changes: None
- ADR status: Proposed
- Human accepted: No
- Independent Argon review: Still required

Major revisions:
- added immutable, versioned durable task input
- separated bounded continuation control data from task-scoped artifacts
- made the 16 KiB continuation limit a provisional configured default
- introduced a private, versioned TaskAssignment envelope
- selected an authenticated Orchestrator assignment/delegation boundary
- explicitly blocked executable delegation until that boundary is validated
- moved canonical delegated-child result acceptance to platform projection
- bounded Redis durability claims by configured persistence/recovery
- separated pre-acceptance unavailable capability from post-acceptance
  dispatch failure
- retained claims/fencing without silently adding automatic task retry
- added issue #36 tracing boundaries
- decomposed #33 implementation into six bounded increments

Tool-execution notes:
- Seven focused edit operations completed.
- Full-file review was performed in four ranges.
- git diff --check passed.
- whitespace and final-newline checks passed.
- No correction cycle remains open.


Task:
Independent ADR-0007 architecture review

Tool:
Gemini web app

Model:
Gemini 4 Argon

Reasoning:
High

Outcome:
- revise before acceptance
- 7 blocking findings
- 5 high-priority revisions
- 4 non-blocking recommendations
- simpler pull-claim/direct-projection architecture proposed

Human acceptance:
Pending

Live repository validation:
Required


## Live-repository validation of Argon review

Task:
Validate the Gemini 4 Argon High review of prospective ADR-0007 against live
Tiny Agent Lab main at 7e8bfc7.

Tool:
GitHub Copilot Fusion

Effort:
Fusion Standard

Session:
Continued ADR-0007 session

Model:
GPT-6 Luna

Capacity before:
- 192.0 / 1,500 credits used

Capacity after:
- 196.7 / 1,500 credits used
- Reset shown: Nov 30 at 4:00 PM

Observed account-credit movement:
- +4.7 credits

Combined Fusion usage for ADR-0007:
- initial prospective ADR draft: +3.1
- human-review revision: +2.2
- Argon-finding live validation: +4.7
- total Fusion movement: +10.0 credits

Outcome:
- completed read-only validation
- repository files changed: none
- GitHub issues changed: none
- ADR status remains Proposed
- worktree clean
- review branch HEAD: d394cf3
- main baseline: 7e8bfc7

Argon blocker validation:
- B-1 proposer identity deferred: partially confirmed
- B-2 initial root assignment path missing: partially confirmed and blocking
- B-3 direct result writes bypass fencing: partially confirmed and blocking
- B-4 API plus completion stream contradiction: partially confirmed;
  valid simplification concern, not inherent contradiction
- B-5 pre-bound push can strand pre-delivery work: partially confirmed and
  blocking if push delivery remains
- B-6 child TaskInput/artifact validation omitted: confirmed and blocking
- B-7 recovery workers absent: partially confirmed; missing work ownership is
  real, but four distinct workers are not required

High-priority finding validation:
- H-1 unavailability inconsistency: overstated; lifecycle distinction is
  coherent, but post-acceptance deadline semantics are missing
- H-2 TaskInput immutability contradiction: not supported
- H-3 continuation stage/version ambiguity: partially confirmed
- H-4 root authority grant provisioning missing: partially confirmed and
  blocks executable delegation
- H-5 #36 correlation identifiers must originate in #33 state: confirmed

Recommendation validation:
- 2–4 KiB continuation limit: not supported by repository evidence
- one completion command path: partially confirmed
- TaskInput/artifact retention: confirmed omission
- resumed-turn fallback-history identity: partially confirmed and valid
  forward-compatibility concern

Recommended architecture after validation:
- authenticated pull-claim for initial roots, children, and resumed parents
- non-secret Redis wake-up hints only
- private TaskAssignment returned by authenticated Orchestrator claim
- one assignment/fencing model for every task turn
- authenticated proposal and completion APIs
- direct idempotent atomic Redis projection in the completion handler
- no completion stream/projector unless a distinct reliability benefit is
  later demonstrated
- fenced canonical completion for every execution kind
- explicit child TaskInput/artifact checks during delegation acceptance
- issue #33 authoritative records produce correlation IDs for issue #36

Human acceptance:
- pending ADR revision

## Final ADR-0007 architecture revision

Task:
Revise prospective ADR-0007 after independent Gemini 4 Argon High review and
live-repository validation.

Tool:
GitHub Copilot Fusion

Effort:
Fusion Standard

Session:
Continued ADR-0007 session

Model:
GPT-6 Luna

Capacity before:
- 196.7 / 1,500 credits used

Capacity after:
- 201.8 / 1,500 credits used
- Reset shown: Nov 30 at 4:00 PM

Observed account-credit movement:
- +5.1 credits

Combined Fusion movement for ADR-0007:
- initial draft: +3.1
- human-review revision: +2.2
- Argon live validation: +4.7
- final architecture revision: +5.1
- total: +15.1 credits

Outcome:
- revision completed
- ADR remains Proposed
- only ADR-0007 modified
- implementation files changed: none
- tests changed: none
- GitHub issues changed: none
- commit/push performed in this pass: no
- explicit human acceptance: pending

Major architecture changes:
- replaced pre-bound push assignments with authenticated pull-claim
- unified initial root, delegated child, and resumed-parent assignment
- made Redis queues non-secret wake-up hints only
- selected authenticated Orchestrator claim/proposal/completion boundary
- replaced completion stream/projector with direct idempotent atomic projection
- applied fenced completion to every assignment-backed execution turn
- added root authority grant creation and assignment binding
- added TaskInput and artifact verification to delegation acceptance
- added candidate claim deadlines and canonical dispatch failure
- defined continuation stage and version transitions
- preserved explicit recovery_required for ambiguous acknowledged claims
- added reference-safe TaskInput/artifact retention
- selected one issue-#33 result transport
- added turn identity to fallback telemetry
- made issue #33 authoritative records trace-ready for issue #36
- scoped atomic operations to bundled single-node Redis
- decomposed issue #33 into six bounded implementation increments

Validation:
- full ADR reread completed
- git diff --check passed
- staged diff check passed
- whitespace/EOF checks passed
- only ADR-0007 modified

Capacity assessment:
- Luna successfully incorporated adversarial Argon findings and live-repository
  validation into a materially simpler architecture.
- The final revision cost more than the initial draft because it replaced core
  transport, assignment, completion, and recovery decisions rather than merely
  editing wording.

## Final ADR-0007 consistency correction

Task:
Apply final contract, continuation-stage, and unclaimed-child terminology
corrections to prospective ADR-0007.

Tool:
GitHub Copilot Fusion

Effort:
Fusion Standard

Session:
Continued ADR-0007 session

Model:
GPT-6 Luna

Capacity before:
- 201.8 / 1,500 credits used

Capacity after:
- 203.4 / 1,500 credits used
- Reset shown: Nov 30 at 4:00 PM

Observed account-credit movement:
- +1.6 credits

Combined Fusion movement for ADR-0007:
- initial draft: +3.1
- first human-review revision: +2.2
- Argon review validation: +4.7
- architecture rewrite: +5.1
- final consistency corrections: +1.6
- total: +16.7 credits

Corrections:
- clarified the distinct purposes of TaskRequested, TaskResult,
  TaskAssignment, and trusted canonical completion
- defined incorporate_analysis_child strictly as an application resumption
  entry point rather than a scheduling state
- replaced dispatch_failed with claim_timed_out where no Analysis runtime
  claims an accepted pending child before the deadline
- preserved the distinction among claim timeout, execution failure,
  assignment-delivery failure, and temporary executor unavailability

Validation:
- only ADR-0007 changed
- git diff --check passed
- staged diff check passed
- whitespace and EOF checks passed
- stale wording search passed
- ADR remains Proposed
- no tests run because the change is documentation-only
- no commit or push performed

## ADR-0007 acceptance recording

Task:
Record explicit human acceptance of ADR-0007 after architecture review and
governance completion.

Tool:
GitHub Copilot Fusion

Effort:
Fusion Standard

Model:
GPT-6 Luna

Capacity before:
- 203.4 / 1,500 credits used

Capacity after:
- 204.0 / 1,500 credits used
- Reset shown: Nov 30 at 4:00 PM

Observed account-credit movement:
- +0.6 credits

Combined Fusion movement for ADR-0007:
- initial draft: +3.1
- first revision: +2.2
- Argon validation: +4.7
- architecture rewrite: +5.1
- final consistency pass: +1.6
- acceptance recording: +0.6
- total: +17.3 credits

Outcome:
- ADR status changed from Proposed to Accepted
- explicit human acceptance recorded
- acceptance date recorded as 2026-11-16
- independent Argon review and live validation documented
- accepted architecture summarized
- pre-enablement implementation gates retained
- only ADR-0007 modified
- validation passed



### Antigravity capacity observation after Issue #219

Task:
Implement and harden Issue #219 durable continuation storage foundation.

Tool:
Antigravity

Primary model:
Gemini High

Work performed:
- initial repository-grounded implementation
- multiple human architecture review gates
- five focused commits before squash merge
- durable TaskInput, StageArtifact, TaskContinuation, and root-authority records
- canonical serialization and deep immutability
- atomic Redis Lua persistence
- registration markers and contiguous version streams
- Redis concurrency, corruption, and replay tests
- Pyrefly corrections in touched code
- PR #226 merged after CI and CodeQL passed

Previous Gemini weekly checkpoint:
- remaining_percent: 87.82
- used_percent: 12.18
- source: prior Antigravity CLI observation
- exact collection timestamp: not retained in this note

Current observation:
- provider: antigravity
- source: provider_cli
- command: agy -p /usage --output-format json
- status: available
- measurement consumed model tokens: no

Gemini Models:
- weekly remaining_percent: 70.33663392066956
- weekly used_percent: 29.66336607933044
- weekly reset_at: 2026-11-20T22:52:22Z
- five_hour remaining_percent: 43.831053376197815
- five_hour used_percent: 56.168946623802185
- five_hour reset_at: 2026-11-17T06:44:51Z

Observed movement since previous weekly checkpoint:
- weekly capacity consumed: 17.48336607933044 percentage points

Five-hour starting observation:
- 100% remaining after reset, user-observed

Observed five-hour movement:
- capacity consumed: 56.168946623802185 percentage points

Claude and GPT models:
- weekly remaining_percent: 100.0
- five_hour remaining_percent: 100.0

Interpretation:
- The substantial Issue #219 implementation and repeated correction/review
  cycles consumed approximately 17.48 percentage points of the Gemini weekly
  allowance since the prior recorded checkpoint.
- No intermediate PC checkpoint was collected, so individual AG passes cannot
  be cost-attributed separately.
- Claude and GPT quota remained unused.



#220 Phase 1 starting checkpoint
Gemini weekly remaining: 70.48234939575195%
Gemini five-hour remaining: 100%
Claude/GPT weekly remaining: 100%
Claude/GPT five-hour remaining: 100%
Measurement cost: 0 tokens


### Issue #220 interim Antigravity checkpoint

Task:
Implement the first pass of Issue #220:
authenticated pull-claim, private TaskAssignment, fencing,
detached assignment proof, root delegation grant,
wake-up hints, acknowledgement, and authenticated artifact staging.

Tool:
Antigravity

Model:
Gemini High

Repository baseline:
- main commit: 074fac4
- feature branch: feature/issue-220-authenticated-pull-claim

Status:
- implementation first pass completed
- human review pending
- Pyrefly/security inspection in progress
- no commit or push performed
- real Redis DB 15 validation not yet completed
- executable delegation remains disabled

Scope observed:
- 19 files changed or created
- 12 tracked files modified
- 7 new files
- reported diff: 2,003 insertions, 20 deletions
- runtime authentication, pull-claim, assignment, fencing,
  root grant, hint delivery, acknowledgement, and artifact staging touched

Capacity before Phase 1 inspection:
- Gemini weekly remaining: 70.48234939575195%
- Gemini five-hour remaining: 100%

Capacity after Phase 1 inspection:
- Gemini weekly remaining: 70.0733482837677%
- Gemini five-hour remaining: 98.56851100921631%

Capacity after initial implementation pass:
- Gemini weekly remaining: 66.70581102371216%
- Gemini five-hour remaining: 86.28212809562683%

Observed movement, Phase 1 inspection:
- weekly consumed: 0.40900111198425 percentage points
- five-hour consumed: 1.43148899078369 percentage points

Observed movement, implementation pass after inspection:
- weekly consumed: 3.36753726005554 percentage points
- five-hour consumed: 12.28638291358948 percentage points

Observed movement, complete #220 session so far:
- weekly consumed: 3.77653837203979 percentage points
- five-hour consumed: 13.71787190437317 percentage points

Measurement:
- command: agy -p /usage --output-format json
- CLI measurement consumed model tokens: no
- input tokens: 0
- output tokens: 0
- thinking tokens: 0
- total tokens: 0
- turns: 0

Claude and GPT models:
- weekly remaining: 100%
- five-hour remaining: 100%

Validation state at checkpoint:
- focused deterministic tests reported passing
- default suite reported 1,475 passed and 15 deselected
- Ruff passed
- real Redis DB 15 suite not run because Redis was unavailable
- editor exposed Pyrefly diagnostics in branch-changed code
- read-only Pyrefly, security-boundary, scope, and test-command inspection requested

Interpretation:
- This is an interim observation, not evidence that Issue #220 is complete.
- The first implementation pass consumed approximately 3.37 weekly percentage
  points and 12.29 five-hour percentage points after the Phase 1 inspection.
- Final engineering outcome and total capacity movement remain pending review,
  correction, real Redis validation, CI, and merge.

### Issue #220 Pyrefly and security inspection checkpoint

Capacity before inspection:
- Gemini weekly remaining: 66.70581102371216%
- Gemini five-hour remaining: 86.28212809562683%

Capacity after inspection:
- Gemini weekly remaining: 65.41837453842163%
- Gemini five-hour remaining: 83.38279128074646%

Observed inspection movement:
- weekly consumed: 1.28743648529053 percentage points
- five-hour consumed: 2.89933781336975 percentage points

Complete Issue #220 session movement so far:
- starting weekly remaining: 70.48234939575195%
- current weekly remaining: 65.41837453842163%
- weekly consumed: 5.06397485733032 percentage points
- starting five-hour remaining: 100%
- current five-hour remaining: 83.38279128074646%
- five-hour consumed: 16.61720871925354 percentage points

Inspection outcome:
- 7 Pyrefly diagnostics found in branch-touched files
- 6 verified as pre-existing on main
- 1 branch-introduced test-fixture typing issue
- repository-wide baseline contains 310 Pyrefly diagnostics
- security-boundary inspection found no raw credential or assignment-proof
  persistence or logging
- legacy_push remains the default
- authenticated_claim publishes hints only
- executable delegation remains disabled
- real Redis DB 15 verification remains pending

Blocking design issue:
- idempotent claim replay returns the existing assignment without a reusable
  assignment proof
- a lost initial response could leave the runtime unable to acknowledge or
  complete the assignment
- proof replay semantics require an explicit human architecture decision

Repository state:
- branch: feature/issue-220-authenticated-pull-claim
- changes remain unstaged and uncommitted
- no push performed

### Issue #220 cumulative Antigravity capacity observation

Task:
Implement and harden Issue #220:
authenticated pull-claim, RuntimePrincipal authentication,
private TaskAssignment, fencing, detached assignment proofs,
root delegation grants, non-secret wake-up hints,
assignment acknowledgement, delivery-lease handling,
and authenticated artifact staging.

Tool:
Antigravity

Model:
Gemini High

Repository:
Tiny Agent Lab / autonomous-agent-lab

Branch:
feature/issue-220-authenticated-pull-claim

Baseline:
074fac4

Current status:
- Phase 1 architecture inspection completed
- initial implementation completed
- Pyrefly and security inspection completed
- deterministic proof-replay design completed
- proof-replay correction implemented
- grant-lifecycle and secret-configuration inspection completed
- assignment-scoped grant correction approved but not yet implemented
- working tree remains unstaged
- no commit or push performed
- real Redis DB 15 verification remains pending
- executable delegation remains disabled

Measurement source:
- provider: antigravity
- source: provider_cli
- command: agy -p /usage --output-format json
- measurement consumed model tokens: no
- input tokens: 0
- output tokens: 0
- thinking tokens: 0
- total tokens: 0
- turns: 0

#### Gemini weekly window

Issue #220 starting observation:
- remaining_percent: 70.48234939575195
- used_percent: 29.51765060424805
- reset_at: 2026-11-20T22:52:22Z

Latest observation:
- remaining_percent: 62.74850368499756
- used_percent: 37.25149631500244
- reset_at: 2026-11-20T22:52:22Z

Observed weekly movement for Issue #220 so far:
- consumed_percentage_points: 7.73384571075439

#### Gemini five-hour window 1

Starting remaining_percent:
- 100.0

Final observed remaining_percent before reset:
- 83.38279128074646

Observed movement:
- consumed_percentage_points: 16.61720871925354

#### Gemini five-hour window 2

The five-hour quota reset between observations.

Latest remaining_percent:
- 88.54944705963135

Current-window used_percent:
- 11.45055294036865

Observed current-window movement:
- consumed_percentage_points: 11.45055294036865

#### Aggregate five-hour workload indicator

Sum of observed consumption across the two distinct five-hour windows:
- 28.06776165962219 percentage points

This aggregate is not a single-window utilization percentage.
It sums observed consumption across two different reset windows.

#### Observation checkpoints

1. Issue #220 start:
   - weekly remaining: 70.48234939575195%
   - five-hour remaining: 100.0%

2. After Phase 1 architecture inspection:
   - weekly remaining: 70.0733482837677%
   - five-hour remaining: 98.56851100921631%

3. After initial implementation:
   - weekly remaining: 66.70581102371216%
   - five-hour remaining: 86.28212809562683%

4. After Pyrefly and security inspection:
   - weekly remaining: 65.41837453842163%
   - five-hour remaining: 83.38279128074646%

5. After the five-hour reset and deterministic proof-design pass:
   - weekly remaining: 64.875328540802%
   - five-hour remaining: 97.99333214759827%

6. After proof implementation and correction:
   - weekly remaining: 63.14380764961243%
   - five-hour remaining: 90.93301892280579%

7. After grant-lifecycle and configuration inspection:
   - weekly remaining: 62.74850368499756%
   - five-hour remaining: 88.54944705963135%

#### Engineering outcomes observed so far

- authenticated runtime-principal boundary designed and implemented
- private immutable TaskAssignment introduced
- opaque detached assignment proof designed
- deterministic proof recovery added for lost-response idempotent retry
- proof-token and verifier subkeys separated
- only keyed verifier digests persisted
- constant-time proof validation implemented
- active claims and fencing state added
- non-secret wake-up hint delivery added behind legacy-default delivery mode
- delivery-lease expiry and acknowledgement added
- authenticated artifact staging added
- Pyrefly inspection completed
- branch-introduced test-fixture diagnostic corrected
- authority-grant lifecycle defect discovered before commit
- fixed production secret defaults discovered before commit
- assignment-scoped immutable grant correction approved
- authenticated-claim fail-fast configuration correction approved

#### Interpretation

The complete Issue #220 session has consumed approximately
7.73 percentage points of the Gemini weekly allowance so far.

The work has crossed two separate five-hour windows, consuming approximately
16.62 percentage points in the first observed window and 11.45 percentage
points in the current window.

These observations represent unfinished engineering work. Final capacity,
quality, and outcome assessment remain pending:
- assignment-scoped grant correction
- configuration hardening
- real Redis DB 15 tests
- final review
- CI
- merge

#### Assignment-scoped grant correction checkpoint

Latest observation:
- Gemini weekly remaining: 61.42271161079407%
- Gemini five-hour remaining: 84.75317358970642%

Movement since prior checkpoint:
- weekly consumed: 1.32579207420349 percentage points
- five-hour consumed: 3.79627346992493 percentage points

Complete Issue #220 movement so far:
- weekly consumed: 9.05963778495788 percentage points
- first five-hour window consumed: 16.61720871925354 percentage points
- current five-hour window consumed: 15.24682641029358 percentage points
- aggregate across two five-hour windows: 31.86403512954712 percentage points

Engineering outcome:
- authority grants changed from a root-scoped overwrite model to immutable,
  assignment-scoped records
- grants now bind assignment, principal, fencing epoch, and turn identity
- fixed usable cryptographic defaults removed
- authenticated-claim mode now requires explicit secrets and active principals
- safe configuration placeholders added
- real Redis verification and final Lua mutation-order review remain pending


#### Configuration, authority-propagation, and timestamp-safety correction

Capacity before correction:
- Gemini weekly remaining: 60.15726923942566%
- Gemini five-hour remaining: 78.32412719726562%

Capacity after correction:
- Gemini weekly remaining: 56.54190182685852%
- Gemini five-hour remaining: 69.09301877021790%

Observed movement:
- weekly consumed: 3.61536741256714 percentage points
- five-hour consumed: 9.23110842704772 percentage points

Complete Issue #220 movement so far:
- starting weekly remaining: 70.48234939575195%
- current weekly remaining: 56.54190182685852%
- total weekly consumed: 13.94044756889343 percentage points
- first five-hour window consumed: 16.61720871925354 percentage points
- current five-hour window consumed: 30.90698122978210 percentage points
- aggregate across two five-hour windows: 47.52418994903564 percentage points

Measurement:
- command: agy -p /usage --output-format json
- measurement input tokens: 0
- measurement output tokens: 0
- measurement thinking tokens: 0
- measurement total tokens: 0
- measurement turns: 0

Engineering outcomes:
- both runtime-credential and assignment-proof peppers now require at least
  32 bytes of decoded secret material
- runtime-principal configuration standardized on RUNTIME_PRINCIPALS_JSON
- malformed lease and principal configuration now fails startup rather than
  silently falling back
- legacy_push may still start without claim-mode secrets
- authenticated_claim requires explicit valid secrets and active principals
- authenticated principal identity now flows explicitly into the Redis
  acknowledgement operation
- Redis acknowledgement no longer uses the stored claim principal as the
  expected caller identity
- canonical fixed-width UTC timestamp normalization introduced
- ActiveClaim, TaskAssignment, DelegationGrant, and WakeUpHint timestamps are
  normalized before persistence
- Lua timestamp comparisons are now based on one fixed-width UTC representation
- naive or malformed timestamps fail closed
- focused pull-claim suite reported 173 passing tests
- Ruff, Compose, and whitespace checks passed
- working tree remains unstaged, uncommitted, and unpushed

Current status:
- production Redis adapter and persisted timestamp representations changed
  during this pass
- real Redis DB 15 verification must be repeated
- direct human default-suite verification must be repeated
- independent architecture and security review remains pending
- executable delegation remains disabled

Local human verification:
- default suite: 1486 passed, 21 deselected
- real Redis 7 / DB 15: 20 passed, 1487 deselected
- Ruff: passed
- Compose validation: passed
- whitespace validation: passed
- executable delegation remains disabled

#### Independent-review live-checkout validation

A Gemini weekly quota reset occurred while waiting for the independent
Hydrogen/Argon reviews.

The weekly and five-hour buckets both showed 100% remaining immediately before
this AG read-only validation task. The screenshot captured the task shortly
after starting at 100% weekly and 99% five-hour remaining.

Model:
- Gemini 3.8 Flash High

Task:
- validate consolidated independent-review findings against live commit 2de7f34
- read-only repository inspection
- no edits, staging, commits, or pushes

New quota-window baseline:
- Gemini weekly remaining: 100%
- Gemini five-hour remaining: 100%

Capacity after validation:
- Gemini weekly remaining: 98.9980936050415%
- Gemini five-hour remaining: 96.98933362960815%

Observed movement:
- weekly consumed: 1.00190639495850 percentage points
- five-hour consumed: 3.01066637039185 percentage points

Reset timestamps reported after the task:
- Gemini weekly reset: 2026-11-24T23:41:47Z
- Gemini five-hour reset: 2026-11-18T04:41:47Z

Measurement:
- command: agy -p /usage --output-format json
- input tokens: 0
- output tokens: 0
- thinking tokens: 0
- total tokens: 0
- turns: 0

Prior weekly-window segment:
- Issue #220 consumed approximately 13.94044756889343 weekly percentage
  points before the reset.

Current weekly-window segment:
- Issue #220 consumed approximately 1.00190639495850 weekly percentage
  points after the reset.

These segments must remain distinct because a weekly reset occurred between
them. Their arithmetic sum may be used only as an accumulated workload
indicator, not as utilization of one continuous quota window.

Engineering outcome:
- live-checkout validation confirmed the independent-review findings for:
  - missing authoritative task-capability binding
  - execution-kind/lifecycle mismatch
  - incorrect restoration of resumable tasks after lease expiry
  - missing continuation and TaskInput binding
  - non-atomic artifact staging
  - incomplete API exception mappings
  - noncanonical custom-target hint routing
  - weak runtime-principal registry validation
  - ActiveClaim state/timestamp invariant
  - stale proof-replay documentation
  - duplicate unreachable test code
  - StageArtifact timestamp normalization
- root grant policy was narrowed:
  - issuance eligibility belongs to Issue #220
  - mutable grant/wave consumption remains in Issue #221
  - replacement grants after unacknowledged expiry remain safe through fencing
- no files were changed

#### Issue #220 consolidated correction pass

Context:
- A weekly quota reset occurred before the independent-review validation.
- This correction pass belongs to the new quota-window segment.
- Model: Gemini 3.8 Flash High
- Elapsed time: approximately 30+ minutes
- Working tree remained unstaged and uncommitted

Capacity before correction pass:
- Gemini weekly remaining: 98.9980936050415%
- Gemini five-hour remaining: 96.98933362960815%

Capacity after correction pass:
- Gemini weekly remaining: 93.09117197990417%
- Gemini five-hour remaining: 77.34510898590088%

Correction-pass movement:
- weekly consumed: 5.90692162513733 percentage points
- five-hour consumed: 19.64422464370727 percentage points

Complete post-reset Issue #220 segment:
- weekly consumed: 6.90882802009583 percentage points
- five-hour consumed: 22.65489101409912 percentage points

Measurement:
- command: agy -p /usage --output-format json
- weekly reset: 2026-11-24T23:41:47Z
- five-hour reset: 2026-11-18T04:41:47Z
- input tokens: 0
- output tokens: 0
- thinking tokens: 0
- total tokens: 0
- turns: 0

Engineering outcomes:
- added immutable RequiredCapabilityRecord
- authoritative task capability is stored separately from mutable status
- claim capability and execution-kind compatibility are checked atomically
- prior claimable status is preserved across unacknowledged lease expiry
- TaskInput and continuation state are bound into claims
- continuation-version validation added
- artifact staging now validates claim and fence atomically
- canonical hint routing no longer derives capability from arbitrary queue names
- runtime-principal registry validation strengthened
- API domain-error mappings expanded
- ActiveClaim state/acknowledgement invariants strengthened
- StageArtifact timestamps normalized
- full default suite reported 1493 passed, 23 deselected
- live Redis 7 suite reported 22 passed
- Ruff and whitespace checks passed
- working tree remains unstaged and uncommitted


#### Issue #220 Pyrefly and correction-safety review

Capacity before review:
- Gemini weekly remaining: 93.09117197990417%
- Gemini five-hour remaining: 77.34510898590088%

Capacity after review:
- Gemini weekly remaining: 90.72467088699341%
- Gemini five-hour remaining: 68.06234717369080%

Observed movement:
- weekly consumed: 2.36650109291076 percentage points
- five-hour consumed: 9.28276181221008 percentage points

Complete post-reset Issue #220 segment:
- weekly consumed: 9.27532911300659 percentage points
- five-hour consumed: 31.93765282630920 percentage points

Measurement:
- command: agy -p /usage --output-format json
- input tokens: 0
- output tokens: 0
- thinking tokens: 0
- total tokens: 0
- turns: 0

Pyrefly environment:
- extension: meta.pyrefly 1.4.1
- Python: 3.12.16 from repository virtual environment
- type-checking mode: auto
- baseline 074fac4: 22 diagnostics, including 6 errors
- checkpoint 2de7f34: 52 diagnostics, including 10 errors
- corrected tree: 60 diagnostics, including 6 errors
- zero Issue #220-introduced Pyrefly errors remain
- all 6 remaining errors were present at 074fac4 on unchanged lines

Corrections:
- removed broad TypeError-based TaskDispatcher compatibility fallback
- updated every TaskDispatcher implementation and test double
- removed empty-assignment artifact-security bypass
- artifact persistence now always requires assignment, principal, claim state,
  fencing epoch, and capability-policy validation
- fixed Redis test type-narrowing errors
- removed redundant exception branches identified by Pyrefly

Verification reported:
- focused Issue #220 tests: 136 passed
- full default suite: 1493 passed, 23 deselected
- real Redis 7 / DB 15: 22 passed
- Ruff: passed
- Compose validation: passed
- whitespace and EOF checks: passed
- working tree remains unstaged and uncommitted

#### Issue #220 continuation-version numeric hardening

Capacity before:
- Gemini weekly remaining: 90.72467088699341%
- Gemini five-hour remaining: 68.06234717369080%

Capacity after:
- Gemini weekly remaining: 90.07492661476135%
- Gemini five-hour remaining: 64.78822827339172%

Observed movement:
- weekly consumed: 0.64974427223206 percentage points
- five-hour consumed: 3.27411890029908 percentage points

Complete post-reset Issue #220 segment:
- weekly consumed: 9.92507338523865 percentage points
- five-hour consumed: 35.21177172660828 percentage points

Engineering outcome:
- expected continuation version must be a positive integer
- authoritative continuation-latest pointer must be a positive integer
- malformed authoritative pointers map to fail-closed corruption errors
- continuation validation remains before the first Redis mutation
- focused Issue #220 suite: 137 passed
- real Redis 7 / DB 15 suite: 23 passed
- Ruff passed
- git diff checks passed
- zero Issue #220 Pyrefly errors on changed lines
- no staging, commit, or push

#### Issue #220 continuation-version type-contract correction

Capacity before:
- Gemini weekly remaining: 90.07492661476135%
- Gemini five-hour remaining: 64.78822827339172%

Capacity after:
- Gemini weekly remaining: 89.71341848373413%
- Gemini five-hour remaining: 63.52294683456421%

Observed movement:
- weekly consumed: 0.36150813102722 percentage points
- five-hour consumed: 1.26528143882751 percentage points

Complete post-reset Issue #220 segment:
- weekly consumed: 10.28658151626587 percentage points
- five-hour consumed: 36.47705316543579 percentage points

Engineering outcome:
- application port restored to integer continuation-version semantics
- fractional expected-version corruption is tested directly at the Redis Lua
  boundary
- focused in-memory numeric-hardening test passed
- focused real-Redis numeric-hardening test passed
- Ruff passed
- zero Issue #220 Pyrefly errors on changed lines
- no staging, commit, or push

#### Issue #220 final capability-boundary corrections

Capacity before:
- Gemini weekly remaining: 89.71341848373413%
- Gemini five-hour remaining: 63.52294683456421%

Capacity after:
- Gemini weekly remaining: 87.36956119537354%
- Gemini five-hour remaining: 58.76213908195496%

Observed movement:
- weekly consumed: 2.34385728836059 percentage points
- five-hour consumed: 4.76080775260925 percentage points

Complete post-reset Issue #220 segment:
- weekly consumed: 12.63043880462646 percentage points
- five-hour consumed: 41.23786091804504 percentage points

Engineering outcome:
- removed arbitrary queue-name parsing from authenticated hint routing
- explicit canonical capability is accepted and validated
- exact canonical queue-map inversion is the only no-argument fallback
- arbitrary custom targets without explicit capability fail closed
- authenticated mode publishes no legacy TaskRequested payload
- child task status, lineage, required capability, and parent membership now
  register atomically
- identical child registration is idempotent
- partial or conflicting child registration fails without mutation
- RequiredCapabilityRecord cannot be overwritten by child replay
- focused registration and dispatch suite: 138 passed
- real Redis 7 / DB 15 suite: 25 passed
- Ruff passed
- zero Issue #220 Pyrefly errors on changed lines
- six pre-existing full-scope Pyrefly errors remain on unchanged legacy lines
- no staging, commit, or push

#### Issue #220 RequiredCapabilityRecord contract hardening

Capacity before:
- Gemini weekly remaining: 87.36956119537354%
- Gemini five-hour remaining: 58.76213908195496%

Capacity after:
- Gemini weekly remaining: 86.03911399841309%
- Gemini five-hour remaining: 53.63691449165344%

Observed movement:
- weekly consumed: 1.33044719696045 percentage points
- five-hour consumed: 5.12522459030151 percentage points

Complete post-reset Issue #220 segment:
- weekly consumed: 13.96088600158691 percentage points
- five-hour consumed: 46.36308550834656 percentage points

Engineering outcome:
- RequiredCapabilityRecord now accepts only general, research, or analysis
- explicit empty, whitespace-only, and unknown capabilities fail closed
- registration no longer silently substitutes default capabilities for
  explicitly invalid inputs
- root and child registration validation occurs before Redis mutation
- RequiredCapabilityRecord parsing rejects missing required fields,
  unsupported versions, unexpected fields, and credential-bearing keys
- focused contract and registration tests: 73 passed
- complete Redis 7 / DB 15 suite: 26 passed
- Ruff passed
- zero new Pyrefly errors on changed lines
- no staging, commit, or push



## Tiny Capacity Lab Antigravity adapter: first implementation pass

Task:
Implement the first bounded Experiment 0001 Antigravity normalization adapter,
immutable observation types, deterministic fixtures, and tests.

Tool:
Antigravity

Model:
Gemini Medium

Status at checkpoint:
- first implementation prompt completed
- direct human review completed
- correction prompt prepared but not yet run
- no files staged, committed, or pushed

Engineering outcome:
- Python 3.12+ package scaffold created
- project-specific AGENTS.md created
- immutable normalized observation contracts created
- Antigravity structured-response parser created
- deterministic synthetic fixtures created
- 37 tests passed
- Ruff passed
- whitespace validation passed
- live provider observation remains ignored

Human-review findings before correction:
- group identity derivation must not infer authority from bucket prefixes
- normalized percentages must retain full arithmetic precision
- parser should have one unsuccessful-response behavior
- collection timestamps require stronger semantics
- undocumented provider observation timestamps must not be inferred
- unknown window identities must not be silently rewritten
- command.name must be validated
- frozen models must not expose mutable nested state
- fixtures should contain only fields needed by deterministic tests

Quota-window boundary:
- the Gemini five-hour quota reset between the preceding observation and this
  checkpoint
- this checkpoint begins a new five-hour quota-window segment
- pre-reset and post-reset consumption must remain separate
- any sum across reset segments is only an accumulated workload indicator, not
  utilization of one continuous five-hour window

Observation after first implementation prompt and before correction prompt:
- Gemini weekly remaining: 86.53494715690613%
- Gemini weekly used: 13.46505284309387%
- Gemini five-hour remaining: 98.27970266342163%
- Gemini five-hour used in this new window: 1.72029733657837%
- Claude/GPT weekly remaining: 100%
- Claude/GPT five-hour remaining: 100%

Reset timestamps:
- Gemini weekly: 2026-11-24T23:41:47Z
- Gemini five-hour: 2026-11-18T09:41:47Z
- Claude/GPT weekly: 2026-11-25T05:12:59Z
- Claude/GPT five-hour: 2026-11-18T10:12:59Z

Measurement:
- command: `agy -p /usage --output-format json`
- duration_seconds: 0
- num_turns: 0
- input_tokens: 0
- output_tokens: 0
- thinking_tokens: 0
- cache_read_tokens: 0
- total_tokens: 0

Interpretation:
- this checkpoint measures the first implementation prompt only
- it is the before-reading for the pending focused correction pass
- final adapter quality, test count, and total capacity movement remain pending

### Antigravity adapter focused correction pass

Task:
Apply the human-reviewed provenance, precision, timestamp, validation,
immutability, and error-contract corrections to the first Experiment 0001
Antigravity adapter implementation.

Tool:
Antigravity

Model:
Gemini Medium

Capacity before correction pass:
- Gemini weekly remaining: 86.53494715690613%
- Gemini five-hour remaining: 98.27970266342163%

Capacity after correction pass:
- Gemini weekly remaining: 85.68367958068848%
- Gemini five-hour remaining: 96.69291377067566%
- Claude/GPT weekly remaining: 100%
- Claude/GPT five-hour remaining: 100%

Observed correction-pass movement:
- Gemini weekly consumed: 0.85126757621765 percentage points
- Gemini five-hour consumed: 1.58678889274597 percentage points

Current post-reset five-hour segment:
- segment starting remaining: 100%
- current remaining: 96.69291377067566%
- total consumed in this window so far: 3.30708622932434 percentage points
- first implementation pass consumed: 1.72029733657837 percentage points
- focused correction pass consumed: 1.58678889274597 percentage points

Reset timestamps:
- Gemini weekly: 2026-11-24T23:41:47Z
- Gemini five-hour: 2026-11-18T09:41:47Z
- Claude/GPT weekly: 2026-11-25T05:22:24Z
- Claude/GPT five-hour: 2026-11-18T10:22:24Z

Measurement:
- command: `agy -p /usage --output-format json`
- duration_seconds: 0
- num_turns: 0
- input_tokens: 0
- output_tokens: 0
- thinking tokens: 0
- cache_read_tokens: 0
- total_tokens: 0

Corrections completed:
- removed bucket-prefix inference for group identity
- distinguished provider-reported group IDs from IDs derived from group names
- removed normalization-time percentage rounding
- retained full arithmetic precision and provider-reported remaining fractions
- selected one unsuccessful-provider-response behavior
- made collection timestamps timezone-aware
- removed undocumented provider-observation timestamp extraction
- preserved unknown provider window identifiers without silent rewriting
- required the observed `usage` command identity
- removed mutable metadata from the first normalized contract
- minimized the deterministic fixture

Validation:
- 44 tests passed in 0.05 seconds
- Ruff passed
- `git diff --check` passed
- live provider data remains ignored
- `.venv` remains ignored
- nothing is staged, committed, or pushed

Interpretation:
- the correction pass consumed approximately 0.85 weekly percentage points
  and 1.59 five-hour percentage points
- the complete adapter session has consumed approximately 3.31 percentage
  points in the current post-reset five-hour window
- pre-reset five-hour observations remain a separate quota-window segment
- the implementation remains uncommitted pending direct human diff review
