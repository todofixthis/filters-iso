## Getting Started

Before writing code, check:

- `docs/plans/` — current implementation plan
- `docs/adr/INDEX.md` — prior decisions (don't re-litigate)
- `docs/future/` — deferred features (don't re-discuss)

## Architecture Decision Records

When making significant decisions — choosing between libraries, patterns, tools, or conventions — you **must** write an ADR before implementing the decision. Use the `phx:writing-adrs` skill (from the phx plugin, which `.claude/settings.json` enables) for the format, conventions and tooling: its `adr.py` allocates the number, generates `docs/adr/INDEX.md` and validates the corpus. Outside Claude Code, read the skill at [`SKILL.md`](https://github.com/todofixthis/phx-claude-siat/blob/0725567cec6bab6a227c2a3d569e64c226c33a4e/skills/writing-adrs/SKILL.md) and run its `python3 …/adr.py` commands as `phx-adr` (see Commands). Don't hand-edit the index or add a repo-local ADR script (ADR 003). ADRs live in `docs/adr/`.

If you find yourself about to establish a new cross-cutting pattern (something that will affect multiple domains or files, e.g. a testing convention, a shared utility, an error-handling approach), stop and write an ADR first even if the immediate task feels local. A pattern adopted once becomes the template for everything that follows.

## Commands

```bash
uv run autohooks activate --mode=pythonpath # install pre-commit hook (once per clone)
uv run git commit                           # always use instead of git commit (runs autohooks)
uv add --bounds major <package>             # add a runtime dependency at latest version
uv add --bounds major --group dev <package> # add a dev dependency at latest version
uv run pytest                               # run all tests
uv run pytest test/test_country.py          # run one test module
uv run tox -p                               # test across all supported Python versions
```

The phx plugin's ADR tool, for use outside Claude Code (Renovate bumps these refs with the `adrs` CI job's; don't bump them by hand):

```bash
# Scaffold the next ADR
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr new "Title" --summary "…" --scope path/
# List the decisions binding a path, before changing it
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr for path/to/file
# Mark ADR OLD superseded by NEW
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr supersede OLD --by NEW
# Regenerate docs/adr/INDEX.md
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr index
# Validate, as CI does
uvx --from 'git+https://github.com/todofixthis/phx-claude-siat@0725567cec6bab6a227c2a3d569e64c226c33a4e#subdirectory=skills/writing-adrs' phx-adr check
```

`phx-adr --help`, with the same `uvx --from` prefix, lists the rest.

## Architecture

This is a `phx-filters` extension package. All filters live in `filters_iso/__init__.py` and are registered as `filters.extensions` entry points. Each filter follows the same pattern — read any existing filter to understand it before adding a new one.

Tests are flat pytest functions using the `assert_filter_passes` and
`assert_filter_errors` fixtures injected by the `filters.pytest` plugin. One test
module per filter: `test/test_country.py`, `test/test_currency.py`,
`test/test_locale.py`.

## Docstrings

Google/Napoleon format (`Args:`, `Returns:`, `Note:`) — not Sphinx `:param:` style. Max 80 chars per line. Escape backslashes (e.g. `'\\n'` not `'\n'`). Blank line before lists inside `Args:` sections to avoid Sphinx indentation warnings. ReadTheDocs treats all Sphinx warnings as errors — resolve them before pushing.

## Code Comments

Place comments on the line preceding the code they document, not as trailing comments.

## Language and Style

- NZ English; incorporate Te Reo Māori where natural (e.g. "mahi", "kaupapa")
- Use "Initialises" not "Initializes"

### Writing for coding agents

- Do not document information that already exists in the coding agent's training data or could be easily discovered by reading the code.
- Do not list individual files; list high-level directories so the agent knows where to look.
- Aim for concise style that optimises token count without sacrificing clarity.

## Branches

- `main` — releases only; merge from `develop` via PR
- `develop` — main development branch
- Feature branches off `develop` for all new work

## Agent Config Layout

`.claude/` and `.agents/` are standalone directories, not a whole-directory symlink. They share only `skills`: `.claude/skills` is a symlink into `.agents/skills` (the canonical copy). Keep `.claude/` a real directory — if it becomes a symlink again, the native worktree tool refuses to run and `git add .claude/...` fails with "beyond a symbolic link".

## Git Worktrees

Use `.worktrees/` for isolated workspaces (project-local, gitignored).

After switching to a worktree, run the autohooks activate command (see Commands) to install the pre-commit hook for that worktree.