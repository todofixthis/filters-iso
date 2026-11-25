---
status: Accepted
date: 2026-11-25
scope: [.agents/rules/template-owned.md, .claude/settings.json, .copier-answers.yml, .github/workflows/build.yml, AGENTS.md, docs/adr/, pyproject.toml, renovate.json]
summary: "This project follows the copier template todofixthis/cookiecutter-py, which writes and owns the files that .agents/rules/template-owned.md lists, and defers to its decisions in them, ADR tooling included: reliance on the phx plugin (its hooks in sessions, phx-adr in CI and AGENTS.md, never a repo-local generator, pre-commit hook or vendored copy, with frontmatter following the skill's conventions) as cookiecutter-py ADR 019 decides, and the release-pinned phx-adr commit bumped by Renovate, not the tip of phx's main, as cookiecutter-py ADR 018 decides; diverging from a template decision on purpose needs an ADR here naming the cookiecutter-py ADR it departs from."
revisit-when: This project stops taking template updates; the template supersedes or renumbers one of the ADRs named here; a condition in cookiecutter-py ADR 018's or 019's revisit-when arises in this project.
---

# 006: Defer to cookiecutter-py's Template Decisions, ADR Tooling Included

## Context

[004-defer-to-cookiecutter-py-s-template-decisions.md][] made this project
defer to [cookiecutter-py's copier template][] in the files copier writes, and
handed the `phx-adr` pin to cookiecutter-py ADR 009. It also restated the
core of [003-rely-on-the-phx-plugin-for-adr-tooling.md][], relying on the phx
plugin rather than a repo-local or vendored tool, because no template ADR
decided it. It named the condition under which that restatement gives way: "a
cookiecutter-py ADR decides reliance on the phx plugin".

That has happened. [cookiecutter-py ADR 019][], first released in 1.3.2,
decides plugin reliance for the template and every generated project, and its
Consequences name 004 as able to drop its restatement. ADR 009 was superseded
in 1.3.1 by [cookiecutter-py ADR 018][], which carries its pin decision over
unchanged. This project records template 1.4.0 in `.copier-answers.yml`, and
its template-owned AGENTS.md and `adrs` job comment already cite 019 and
018, and `renovate.json` cites 018. 004's summary still restates 003, so it
duplicates what the template decides, and cites 009, which fires 004's other
condition: "the template supersedes or renumbers one of the ADRs named
here".

## Options

### Option 1: Do nothing

**Pros:** No change to the record.
**Cons:** Two records of plugin reliance, this project's and the template's,
that can only drift; 004 cites a superseded template ADR.

### Option 2: Restate 004 without its copy of 003, and supersede 004 (Accepted)

Keep the deferral, and cite 019 and 018 for the ADR-tooling decisions.

**Cons:** A reader follows links to another repository for all of the
ADR-tooling reasoning. This ADR still names template ADRs by number.

### Option 3: Discharge 004's trigger and keep 004 in force

**Cons:** 004's summary itself restates 003, so it would stay in force while
holding the duplicate the trigger existed to remove.

## Decision

Option 2. The template owns these files and now records every decision about
ADR tooling in them, so a second copy here can only fall behind. Superseding,
not discharging, because the restatement sits in 004's summary, the decision
itself, and because only a restatement can replace 004's citation of the
superseded 009.

003's and 004's ADR-tooling revisit conditions (a phx release imposing a
rejected convention, ADRs routinely authored outside Claude Code, the plugin
dropping its ADR tooling, phx's `main` taking commits that aren't releases)
are watched by 019 and 018 in their own revisit conditions, so this ADR
drops them, keeping one pointer to them: some, such as ADRs authored outside
Claude Code, are seen only from inside a project, whose index never shows the
template's. It keeps the conditions that are this project's own: whether it
takes template updates at all, and whether a cited template ADR moves. 004's
watch for a template change to its ADR tooling arriving without an ADR goes
with the restatement it guarded.

## Consequences

- `.agents/rules/template-owned.md` decides whether a change to a
  template-owned file is made here or proposed to cookiecutter-py; that rule,
  not this ADR's `scope`, lists the files.
- Diverging from a template decision on purpose needs its own ADR here,
  naming the template ADR it departs from.
- The links below pin the 1.4.0 tag, the release this project recorded
  when this ADR was written, so they lead to the decisions it adopted even
  if the template later moves them.

[003-rely-on-the-phx-plugin-for-adr-tooling.md]: 003-rely-on-the-phx-plugin-for-adr-tooling.md
[004-defer-to-cookiecutter-py-s-template-decisions.md]: 004-defer-to-cookiecutter-py-s-template-decisions.md
[cookiecutter-py ADR 018]: https://github.com/todofixthis/cookiecutter-py/blob/1.4.0/docs/adr/018-require-gate-everywhere-and-the-release-check-on-main.md
[cookiecutter-py ADR 019]: https://github.com/todofixthis/cookiecutter-py/blob/1.4.0/docs/adr/019-rely-on-the-phx-plugin-for-adr-tooling.md
[cookiecutter-py's copier template]: https://github.com/todofixthis/cookiecutter-py
