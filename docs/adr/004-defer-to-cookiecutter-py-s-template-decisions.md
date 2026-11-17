---
status: Accepted
date: 2026-11-17
scope: [.agents/rules/template-owned.md, .claude/settings.json, .github/workflows/build.yml, AGENTS.md, docs/adr/, pyproject.toml, renovate.json]
summary: This project follows the copier template todofixthis/cookiecutter-py, which writes and owns the files that .agents/rules/template-owned.md lists, and defers to its decisions in them; restating ADR 003, ADR tooling relies on the phx plugin (its hooks in sessions, phx-adr in CI), not a repo-local generator, pre-commit hook or vendored copy, with frontmatter following phx writing-adrs conventions (scope, not tags), and CI pins a phx-claude-siat release's commit SHA with a trailing `# X.Y.Z`, bumped by Renovate as cookiecutter-py ADR 009 decides, not the tip of phx's main; diverging from a template decision on purpose needs an ADR here naming the cookiecutter-py ADR it departs from.
revisit-when: This project stops taking template updates; a cookiecutter-py ADR decides reliance on the phx plugin; a template release changes AGENTS.md's ADR-tooling instruction or the adrs job without an ADR; the template supersedes or renumbers one of the ADRs named here; a phx plugin release imposes an ADR convention the maintainer rejects; ADRs here are routinely authored outside Claude Code, so CI is the first check most ADR commits meet; the phx plugin drops its ADR tooling; phx's `main` stops carrying only releases.
---

# 004: Defer to cookiecutter-py's Template Decisions

## Context

This project now takes its tooling from [cookiecutter-py's copier template][],
recorded in `.copier-answers.yml`; each template release arrives as a Renovate
PR running `copier update` ([cookiecutter-py ADR 015][]). The files copier
writes are template-owned: `.agents/rules/template-owned.md` lists them and
says how to change one, and is itself written by the template.

[003-rely-on-the-phx-plugin-for-adr-tooling.md][] decided to rely on the phx
plugin for ADR tooling, and pinned CI's `phx-adr` to the tip of phx's
releases-only `main`, which a Renovate `git-refs` manager moved. The
template's CI job, AGENTS.md and Renovate config, all template-owned, pin a
release's commit SHA with a trailing `# X.Y.Z` instead, bumped by a
`github-tags` manager ([cookiecutter-py ADR 009][]). ADR 009 rejects tracking
`main` and names filters-iso as the library that did, so 003 contradicts a
template decision on the point it decided, not only on mechanism.

No template ADR decides 003's core, relying on the phx plugin rather than a
repo-local or vendored tool, though the template's AGENTS.md carries it as an
instruction. Sessions still install the plugin from phx's `main`; only CI's
pin moves to release tags.

[001-migrate-tests-to-pytest.md][] is this project's own and overlaps nothing
the template decides.

## Options

### Option 1: Do nothing

**Pros:** No change to the record.
**Cons:** ADR 003 describes a pin the files no longer use. A reader restoring
the `git-refs` manager conflicts with the next template update touching those
lines, where the template-owned rule takes the template's side.

### Option 2: One ADR deferring to the template and restating 003's core (Accepted)

Supersede 003 with this ADR, which keeps its reliance on the phx plugin and
hands the pin to cookiecutter-py ADR 009.

**Cons:** A reader follows a link to another repository for the pin's
reasoning. This ADR names template ADRs by number, which goes stale if the
template supersedes or renumbers one; the links pin the 1.3.0 tag, so they
still lead to the decision this project adopted. When a template ADR decides
plugin reliance, half of this ADR gives way while the deferral stands.

### Option 3: Two ADRs, as class-registry has

Supersede 003 with a narrow ADR on plugin reliance and the pin, and record the
deferral in a separate ADR, as todofixthis/class-registry's ADRs 007 and 008
do.

**Pros:** A template ADR on plugin reliance would supersede one ADR cleanly.
**Cons:** Two ADRs for one adoption, where filters-iso has no other ADRs for a
deferral to supersede.

### Option 4: Keep 003's pin and diverge from the template

Keep the `git-refs` manager tracking `main`, with an ADR naming cookiecutter-py
ADR 009 as the decision it departs from.

**Pros:** CI's pin follows what sessions install.
**Cons:** Every template change to the pin lines or the Renovate manager
conflicts here, for a trade-off ADR 009 weighed for every library.

## Decision

Option 2. The template owns these files, so it owns the decisions about them;
a second copy here can only fall behind. 003's reason for tracking `main`,
that CI's pin matches what sessions install, is a trade-off ADR 009 already
weighed, singling out filters-iso, and nothing specific to filters-iso changes
it. A single ADR suits a project whose only overlap with the template is 003.

Unlike class-registry's ADR 007, which stayed in force beside its deferral,
003 committed to the option ADR 009 rejects, so it is restated and
superseded rather than kept.

003's core stands, in this ADR's summary: ADR tooling is the phx plugin's,
never a repo-local generator, pre-commit hook or vendored copy, and ADR
frontmatter follows the skill's conventions, `scope` rather than `tags`. The
template implements that core in AGENTS.md without an ADR recording it, so
this ADR holds the record until a template ADR does.

## Consequences

- `.agents/rules/template-owned.md` decides whether a change to a
  template-owned file is made here or proposed to cookiecutter-py; that rule,
  not this ADR's `scope`, lists the files.
- Diverging from a template decision on purpose needs its own ADR here,
  naming the template ADR it departs from.
- Between a plugin release and Renovate's bump, sessions run a newer
  `phx-adr` than CI; AGENTS.md says how to reconcile them. That gap stays
  small only while phx's `main` carries only releases.

[001-migrate-tests-to-pytest.md]: 001-migrate-tests-to-pytest.md
[003-rely-on-the-phx-plugin-for-adr-tooling.md]: 003-rely-on-the-phx-plugin-for-adr-tooling.md
[cookiecutter-py ADR 009]: https://github.com/todofixthis/cookiecutter-py/blob/1.3.0/docs/adr/009-gate-adr-ci-and-the-phx-pin.md
[cookiecutter-py ADR 015]: https://github.com/todofixthis/cookiecutter-py/blob/1.3.0/docs/adr/015-propagate-template-changes-with-copier-and-rotate-python-from-agent-sessions.md
[cookiecutter-py's copier template]: https://github.com/todofixthis/cookiecutter-py
