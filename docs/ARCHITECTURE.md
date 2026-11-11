# Architecture

## One repository, independent capabilities

`skills/` holds portable instructions and their supporting resources. `tools/` holds standalone executables or integrations. `plugins/` holds host-specific packages. A skill's helper script can stay inside its folder; not every script needs a second copy in `tools/`.

The README is the human-readable catalog. `.claude-plugin/marketplace.json` is the Claude Code installation catalog, not a universal plugin format.

## Initial marketplace package

Management Slides has one canonical copy at `skills/management-slides/`. Its marketplace entry uses `source: "./"`, `strict: false` and an explicit `skills` path, following the public Anthropic skills repository pattern. There is no root `plugin.json` and no duplicated skill directory.

For a future plugin with startup hooks, remote servers or native host APIs, place all of its resources inside `plugins/<id>/` and list `source: "./plugins/<id>"`. Do not make plugin paths reach outside that package. Document any permissions, data access and network behavior.

## Portability boundaries

The skill instructions are ordinary Markdown with Agent Skills frontmatter. The deck generator uses local Python and native PowerPoint shapes. Host discovery, invocation syntax, filesystem access, execution permissions and rendering differ by tool.

OpenCode discovers skills in documented local locations; it does not consume a Claude Code marketplace as a native plugin. Copy the selected skill folder or use OpenCode's documented skill source configuration. Do not claim a Claude Code plugin is also an OpenCode plugin.

## What is intentionally absent

No private repository code, company configuration, remote hooks, telemetry, automatic updates, install-time shell execution or generated user presentations. Public examples communicate layout rather than real organizational architecture.
