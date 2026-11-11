# Release process

`main` is protected and always releasable. Changes arrive by pull request; releases are explicit tags, never automatic.

1. Update `CHANGELOG.md` and bump `version` in `.claude-plugin/marketplace.json` for any package whose files changed.
2. Confirm CI is green on `main`, and that `python scripts/validate_repo.py` passes locally.
3. Run `claude plugin validate .` and smoke-test the package in a live Claude Code session when the CLI is available.
4. Tag and publish: `git tag -a vX.Y.Z -m "vX.Y.Z"`, push the tag, then create a GitHub release with notes from the change log.
5. Check the rendered README and the install instructions against the new tag.

## Public-data policy for every release

Review each change, including image pixels and metadata, for private screenshots, workplace identifiers, personal paths and credentials. The validator catches selected patterns only; human review is required. Commit using the maintainer's public-safe identity, not a workplace email.
