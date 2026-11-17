# Changelog

## 0.2.0 — 2026-11-17

### Added

- Bundled thai-docx 0.3.4 with MIT and CommonMark BSD notices; no separate skill installation.
- First-use company interview with eight instructor questions and generalized feedback already included.
- Standalone HTML reports plus evidence, coverage and feedback pages; optional DOCX generation and checks.
- Coverage validation and output-chain commands and tests.

### Changed

- HTML replaces Markdown as the user-facing default. Markdown remains an internal source.
- HTML conversion uses an installed Pandoc; agents may select an alternative if unavailable.
- Agents may recover Word generation using other available converters, with content checks and explicit verification limits.

### Verification boundary

- 19 focused tests passed in development. Bundled DOCX build/check passed and HTML was inspected in a browser.
- Coverage checks validate supplied records, not answer quality or omitted instructor requirements. Agents must compare the original requirements.
- Full multi-industry conversations and Word pagination across office applications remain unverified.

## 0.1.0 — 2026-11-13

### Added

- Adaptive company interviews and problem discovery before strategy drafting.
- Explicit readiness and confirmation gates, including accepted data-collection plans.
- Framework guidance, evidence boundaries, and Thai executive writing standards.
- Word export instructions through the separately installed thai-docx skill.
- Readiness gate tests and conversation acceptance scenarios.

### Verification boundary

The readiness gate has 12 passing tests. Live multi-turn interviews and end-to-end Word export through an installed copy of this skill have not been tested.
