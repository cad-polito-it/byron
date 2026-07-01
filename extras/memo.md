# MEMO

> ┏━┏━━┓━━━━━━━━━━━━━━━━━━┓  
> ┃━┃┏┓┃━━━━━━━━━━━━━━━━━━┃  
> ┃━┃┗┛┗┓┏┓━┏┓┏━┓┏━━┓┏━┓━━┃  
> ┃━┃┏━┓┃┃┃━┃┃┃┏┛┃┏┓┃┃┏┓┓━┃  
> ┃━┃┗━┛┃┃┗━┛┃┃┃━┃┗┛┃┃┃┃┃━┃  
> ┃━┗━━━┛┗━┓┏┛┗┛━┗━━┛┗┛┗┛━┃  
> ┃━┏━━━━━━┛┃━━━━━━━━━━━━━┃  
> ┗━┗━━━━━━━┛━━━━━━━━━━━━━┛  

## Publish

```shell
bumpver update
poetry build
poetry publish

uvx keyring set https://upload.pypi.org/legacy/ __token__


uvx bumpver update
rm dist/*; uv build
uvx twine upload dist/*
UV_PUBLISH_TOKEN=$(security find-generic-password -s "pypi-token" -w) uv publish 
```

## Coverage

```
coverage run --branch -m pytest
coverage html
```

## Conventional Commits

- Core Types (Trigger Releases): These types usually trigger a version bump in semantic versioning (SemVer) and appear directly in automated changelogs.
  - feat (Feature): A new feature being introduced to the codebase. This corresponds to a MINOR version bump in SemVer. Example: feat(auth): add Google OAuth2 login support 
  - fix (Bug Fix): A bug fix for the user or system. This corresponds to a PATCH version bump in SemVer. Example: fix(api): resolve memory leak on websocket connection
- Structural & Maintenance Types: These types are used for changes that don't directly modify production application logic or add user-facing features. They generally do not trigger a version bump.
  - chore: Routine database maintenance, tool updates, or configuration changes that don't modify source code or tests (e.g., updating .gitignore). Example: chore: bump dependencies in package.json 
  - build: Changes that affect the build system, package management, or external dependencies. Example: build(deps): migrate from poetry to uv
  - ci: Changes to CI/CD configuration files and scripts (e.g., GitHub Actions, GitLab CI, Jenkins). Example: ci: add parallel testing to github workflow 
  - docs: Documentation-only changes (e.g., updating the README.md or inline code comments). Example: docs: update installation instructions
  - style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, linting fixes). Example: style: run prettier formatter across codebase
  - refactor: A code change that neither fixes a bug nor adds a feature. It’s strictly about rewriting code for readability, performance, or technical debt. Example: refactor: simplify user validation logic
  - perf (Performance): A code change that explicitly improves performance (speed, memory usage). Example: perf: optimize SQL queries for dashboard loading 
  - test: Adding missing tests or correcting existing tests. Example: test: add unit tests for payment gateway
