---
status: Accepted
date: 2026-11-17
scope: [.agents/rules/template-owned.md, .claude/settings.json, .github/workflows/build.yml, AGENTS.md, docs/adr/, pyproject.toml, renovate.json]
summary: This project follows the copier template todofixthis/cookiecutter-py, which writes and owns the files that .agents/rules/template-owned.md lists, and defers to its decisions in them; restating ADR 003, ADR tooling relies on the phx plugin (its hooks in sessions, phx-adr in CI), not a repo-local generator, pre-commit hook or vendored copy, with the CI pin a phx-claude-siat release tag bumped by Renovate as cookiecutter-py ADR 009 decides, not a digest tracking phx's main; diverging from a template decision on purpose needs an ADR here naming the cookiecutter-py ADR it departs from.
revisit-when: This project stops taking template updates; a cookiecutter-py ADR decides reliance on the phx plugin; the template supersedes or renumbers one of the ADRs named here; a phx plugin release imposes an ADR convention the maintainer rejects; ADRs here are routinely authored outside Claude Code, so CI is the first check most ADR commits meet; the phx plugin drops its ADR tooling.
---

# 004: Defer to cookiecutter-py's Template Decisions

## Context

This project now takes its tooling from [cookiecutter-py's copier template][],
recorded in `.copier-answers.yml`; each template release arrives as a Renovate
PR running `copier update` ([cookiecutter-py ADR 015][]). The files copier
writes are template-owned: `.agents/rules/template-owned.md` lists them and
says how to change one, and is itself written by the template.

[003-rely-on-the-phx-plugin-for-adr-tooling.md][] decided to rely on the phx
plugin for ADR tooling, and pinned CI's `phx-adr` to a commit on phx's
releases-only `main`, which a Renovate `git-refs` manager moved to each new
tip. The template's CI job, AGENTS.md and Renovate config, all template-owned,
pin a release tag's commit instead, bumped by a `github-tags` manager that
matches a trailing `# X.Y.Z` ([cookiecutter-py ADR 009][]). ADR 009 rules out
tracking `main`, which 003 chose, so the two ADRs disagree about files the
template now owns. No template ADR decides 003's core: relying on the phx
plugin rather than a repo-local or vendored tool.

[001-migrate-tests-to-pytest.md][] is this project's own and overlaps nothing
the template decides.

## Options

### Option 1: Do nothing

**Pros:** No change to the record.
**Cons:** ADR 003 describes a pin the files no longer use, and a reader acting
on it would restore the `git-refs` manager, which the next template update
reverts.

### Option 2: Defer to the template, restating 003's core here (Accepted)

Supersede 003 with this ADR, which keeps its reliance on the phx plugin and
hands the pin to cookiecutter-py ADR 009.

**Cons:** A reader follows a link to another repository for the pin's
reasoning. This ADR names template ADRs by number, which goes stale if the
template supersedes or renumbers one; the links pin the 1.3.0 tag, so they
still lead to the decision this project adopted.

### Option 3: Keep 003's pin and diverge from the template

Keep the `git-refs` manager tracking `main`, with an ADR naming cookiecutter-py
ADR 009 as the decision it departs from.

**Pros:** The pin follows what the plugin's marketplace serves.
**Cons:** Every template update touching `renovate.json`, `build.yml` or
AGENTS.md conflicts; nothing about this project needs a different pin from
the template's other libraries.

## Decision

Option 2. The template owns these files, so it owns the decisions about them;
a second copy here can only fall behind. 003's reason for tracking `main`
(that the pin matches what sessions install) is a trade-off ADR 009 already
weighed for every library, and nothing specific to filters-iso changes it.

003's core stands, restated in this ADR's summary: ADR tooling is the phx
plugin's, through its hooks in sessions and `phx-adr` in CI, never a
repo-local generator, pre-commit hook or vendored copy. 003's triggers that
watched phx's `main` don't carry over, since nothing here tracks `main` now.

## Consequences

- `.agents/rules/template-owned.md` decides whether a change to a
  template-owned file is made here or proposed to cookiecutter-py.
- Diverging from a template decision on purpose needs its own ADR here,
  naming the template ADR it departs from.
- Between a plugin release and Renovate's bump, sessions run a newer
  `phx-adr` than CI; the template AGENTS.md says how to reconcile them.

[001-migrate-tests-to-pytest.md]: 001-migrate-tests-to-pytest.md
[003-rely-on-the-phx-plugin-for-adr-tooling.md]: 003-rely-on-the-phx-plugin-for-adr-tooling.md
[cookiecutter-py ADR 009]: https://github.com/todofixthis/cookiecutter-py/blob/1.3.0/docs/adr/009-gate-adr-ci-and-the-phx-pin.md
[cookiecutter-py ADR 015]: https://github.com/todofixthis/cookiecutter-py/blob/1.3.0/docs/adr/015-propagate-template-changes-with-copier-and-rotate-python-from-agent-sessions.md
[cookiecutter-py's copier template]: https://github.com/todofixthis/cookiecutter-py
