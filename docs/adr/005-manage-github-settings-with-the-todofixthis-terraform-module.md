---
status: Accepted
date: 2026-11-20
scope: [.gitignore, infra/]
summary: Manage this repo's GitHub settings through todofixthis/terraform-github-repository from infra/github/, adopted by import ahead of cookiecutter-py shipping it, with local state, plans run by hand and applies from an up-to-date develop after merge; not by hand in the GitHub UI, and not waiting for the template.
revisit-when: cookiecutter-py ships infra files to generated projects; a module bump or a change to infra/github/main.tf merges without a plan having been run; the state is lost, or a second machine or maintainer needs to plan.
---

# 005: Manage GitHub settings with the todofixthis Terraform module

## Context

This repo's GitHub settings were set by hand in the UI: merge methods, features, and two rulesets, `develop` and `main`. Nothing records why they are what they are, and a change made in the UI goes unnoticed.

[todofixthis/terraform-github-repository][module] holds the todofixthis standard for repo settings, and its ADR 001 has every todofixthis repo provisioned through it. Since v1.1.0 it can adopt a repo that already exists, importing its hand-made rulesets in place. cookiecutter-py, which this project follows ([ADR 004][]), doesn't ship the module's infra files yet. No cookiecutter-py ADR decides anything about infra, so adopting the module here adds to the template rather than departing from one of its decisions. This repo is the first library to adopt the module, as a pilot.

The module's own repo gates infra PRs on a plan comment posted from the maintainer's machine (its ADR 003). That needs a plan script, a CI job and path patterns, none of which this repo has.

## Options

### Option 1: Do nothing

**Pros:** No local state to keep.
**Cons:** Settings stay unrecorded, and drift from the standard goes unseen.

### Option 2: Adopt the module now, by hand (Accepted)

`infra/github/` holds a root module calling the module at a pinned tag, with `import` blocks for the existing repo and rulesets. State stays on the maintainer's machine, gitignored. Plans run by hand, and the maintainer applies from an up-to-date `develop` after an infra PR merges, as the module's repo does.

**Cons:** No CI check confirms a plan ran, so a Renovate PR bumping the module tag can be merged without one. Renovate's lock-file maintenance, which automerges, will also refresh `.terraform.lock.hcl` weekly without a plan. That's accepted: a provider lock refresh changes nothing on GitHub, and the next apply shows its plan before acting. Until the template ships these files they're this project's own, so a later template update may conflict on them.
**Risks:** State lives on one machine. Losing it after the `import` blocks are removed makes the next plan propose creating the repo and its rulesets, and the apply fails because the name is taken. Recovery is re-adding the `import` blocks, with one for the `tags-release` ruleset the first apply created, which is safe because the push step only pushes branches the remote lacks. The state holds no secrets (the module's ADR 002).

### Option 3: Wait for cookiecutter-py to ship the infra files

**Pros:** The files arrive through `copier update` like the rest of the template.
**Cons:** Adoption and the module's settings would go untested on a real library first.

## Decision

Option 2. The pilot tests adoption and the module's settings against a real library before any of it goes into the template, where a mistake would reach every generated project. It doesn't test the plan gate the template would also need. That gap is acceptable for a pilot with one maintainer, who runs the plan before every apply. The revisit conditions mark when it stops being acceptable.

## Consequences

- Adopting changes how the maintainer works here:
  - `main` loses its Admin bypass. The release skill's flow still works, since it reaches `main` through a PR, creates tags rather than moving them, and pushes only to `develop`, which keeps its bypass.
  - `tags-release` blocks moving or deleting any tag.
  - Review threads must be resolved before a PR merges.
  - Secret-scanning push protection and Dependabot alerts turn on.
- `.gitignore` ignores Terraform state. It's a template candidate for cookiecutter-py, since any generated project adopting the module needs it.
- A Renovate PR changing `infra/github/main.tf` (a module or provider bump) needs a local plan before it merges.
- The `import` blocks come out in a follow-up PR once applied, as the module's README says.
- When cookiecutter-py ships infra files, this project takes the template's version, and that version's `description` comes from the copier answer, which differs from the repo's live description. The first plan after that update shows the change; keep the live one or accept the new one then.

[ADR 004]: 004-defer-to-cookiecutter-py-s-template-decisions.md
[module]: https://github.com/todofixthis/terraform-github-repository
