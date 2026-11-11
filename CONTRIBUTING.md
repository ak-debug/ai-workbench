# Contributing

Add focused capabilities with a clear purpose, installation instructions, examples, permission requirements and checks. Describe limitations instead of promising universal agent compatibility.

## Workflow

This project follows GitHub flow:

1. Branch from an up-to-date `main` using a short, descriptive name such as `feat/new-layout` or `fix/preview-font`.
2. Make small, focused commits using [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `ci:`).
3. Run the checks listed in the README, then open a pull request using the template.
4. Merge after CI passes, using squash and merge. `main` always stays releasable.

## Add a skill

1. Create `skills/<lowercase-kebab-case-id>/SKILL.md` with `name` and `description` frontmatter. Keep the name aligned with the directory.
2. Keep references, scripts, dependencies and assets inside that folder. Use relative paths and user-provided output directories.
3. Add a README with a small generic example and verification instructions.
4. Add tests where executable code is supplied.
5. Update the root README catalog. To expose it in Claude Code, add an explicit entry to `.claude-plugin/marketplace.json`.

For instruction-only skill packages, a root-based marketplace entry can select `./skills/<id>` without duplicating the skill. Use an actual `plugins/<id>/` directory for hooks, MCP servers and other host-specific behavior. Do not add a root `plugin.json` that conflicts with root-based marketplace entries.

## Public-data policy

- Use newly created synthetic examples. Do not blur a private screenshot and call it public-safe.
- Do not include workplace repositories, internal domains, project identifiers, local usernames, personal paths, tokens, customer data or unapproved branding.
- Review image pixels and metadata as well as text files.
- Never commit private source material even temporarily. Removing it in a later commit does not remove it from history.
- Keep generated user decks, ZIPs, PDFs and scratch environments out of the repository.

Run the checks in the README before proposing a change. The pattern scanner is a guardrail, not a complete confidentiality audit.

## Versioning

Record changes in `CHANGELOG.md`. Bump a package's marketplace version when its files change and update the marketplace version when the catalog changes. Create release tags only after reviewing the exact files to publish.

Check that you have the right to contribute and license each file under the repository's MIT license.
