# Security Policy

Tiny Capacity Lab is a non-commercial learning project that explores how to
observe and compare AI development-tool capacity, usage evidence, and cost
signals.

The project may process provider responses, command output, configuration
metadata, and locally collected evidence. It must not intentionally collect,
store, or publish credentials, authentication tokens, private prompts, private
source code, or personal account identifiers.

## Supported Versions

Security fixes are applied to the default `main` branch.

| Version or branch | Supported |
| --- | --- |
| `main` | Yes |
| Historical commits, branches, or tags | No guaranteed security backports |

This learning project does not currently provide long-term support guarantees
for historical snapshots.

## Reporting a Vulnerability

Please do not disclose suspected vulnerabilities, credentials, sensitive
evidence, or exploit details through public GitHub issues, pull requests,
discussions, or repository files.

Use GitHub Private Vulnerability Reporting:

1. Open the repository's **Security** page.
2. Select **Report a vulnerability**.
3. Provide enough information to reproduce and assess the issue safely.

Helpful details include:

- the affected file, component, command, or provider adapter;
- the relevant branch, commit, or version;
- steps to reproduce using synthetic or sanitized evidence;
- the potential security or privacy impact;
- suggested mitigation, if known.

Do not include active credentials, private prompts, private source code,
personal account identifiers, or real provider tokens in a report. Revoke and
rotate any exposed credential before continuing the investigation.

## Security Vulnerabilities

Examples of security issues include:

- exposure or persistence of credentials, tokens, or authentication material;
- unintended publication of private prompts, source code, account identifiers,
  or provider evidence;
- command or argument injection;
- unsafe handling of provider CLI output or configuration files;
- unauthorized modification of evidence records;
- bypass of provenance, redaction, or integrity controls;
- dependency or workflow behavior that exposes secrets or grants unintended
  access.

## Ordinary Bugs and Research Questions

The following are normally appropriate for a public GitHub issue when they do
not expose sensitive information:

- incorrect quota normalization or percentage calculations;
- stale or missing provider observations;
- parsing failures involving synthetic or sanitized examples;
- documentation errors;
- display or formatting problems;
- disagreements about measurement methodology;
- provider behavior that does not create a security or privacy risk.

When uncertain, use Private Vulnerability Reporting rather than disclosing the
details publicly.

## Credential and Evidence Hygiene

If a credential or other sensitive value may have been exposed:

1. Revoke or rotate it immediately with the provider.
2. Treat the original value as compromised.
3. Do not rely on deleting a file or commit as the sole remediation.
4. Report the exposure privately so repository history and downstream effects
   can be assessed.

Tiny Capacity Lab records what was observed. Security-sensitive or private
information must remain outside published evidence.
