# Filters ISO v3.2.0
Drops legacy Python versions, adds 3.13 and 3.14, and brings tooling in sync with phx-filters.

> [!WARNING]
> **Breaking changes**
> - Python 3.10 and 3.11 are no longer supported
>   - Upgrade to Python 3.12 or later
>   - You'll know you need to migrate if you see version-incompatibility errors at install time

## Enhancements
- Added support for Python 3.13 and 3.14
- Migrated build toolchain and test runner to match phx-filters (uv, pytest)
