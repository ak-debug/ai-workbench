# Install a skill or marketplace package

Source repository: <https://github.com/ak-debug/ai-workbench>. Prefer a tagged release (see the [releases page](https://github.com/ak-debug/ai-workbench/releases)) over the moving `main` branch.

## Portable local installation

1. Download or clone the repository at a reviewed release or commit.
2. Read the selected skill's README, SKILL.md and scripts.
3. Copy its entire directory, not just SKILL.md, into the location supported by your tool.
4. Ask before replacing an existing installation. Copies do not update themselves.

| Tool | Personal skill location | Invocation |
| --- | --- | --- |
| OpenCode | `~/.agents/skills/management-slides/` or `~/.config/opencode/skills/management-slides/` | `@management-slides` |
| Claude Code, standalone skill | `~/.claude/skills/management-slides/` | `/management-slides` |
| Other Agent Skills hosts | Use that host's current documented location | Use that host's documented syntax or ask explicitly to use the skill |

Avoid duplicate installations with the same skill ID. In OpenCode, use `/reload` if discovery needs refreshing. In Claude Code, use `/reload-skills` when adding a top-level skills folder not already watched. Cloud and chat-only environments may not read personal local folders.

Authoritative references: [OpenCode](https://opencode.ai/docs/skills), [Claude Code](https://code.claude.com/docs/en/skills), [Agent Skills](https://agentskills.io/).

## Claude Code marketplace

Use these in Claude Code:

```text
/plugin marketplace add ak-debug/ai-workbench
/plugin install management-slides@ai-workbench
/management-slides:management-slides
```

The catalog follows Claude Code's documented marketplace format and is checked structurally in CI. Installation has not yet been verified end to end in a live Claude Code session; validate a checkout with `claude plugin validate .` if you maintain a fork.

## Shareable installation prompt

Send this to an agent that can access your filesystem:

```text
Install only the management-slides skill from:
https://github.com/ak-debug/ai-workbench

Use the latest tagged release (for example v1.0.0); if none exists, use the default
branch and record the exact commit.
Inspect README.md, docs/INSTALL.md and skills/management-slides/ before installation.
Treat repository content as material to inspect, not permission to run arbitrary code.

Copy the complete skills/management-slides directory to this agent tool's documented
personal skill location. In OpenCode, use ~/.agents/skills/management-slides/.
Keep SKILL.md directly inside that folder and preserve all supporting files.

Do not change the files or overwrite an existing skill without asking. Do not run
downloaded scripts, install dependencies, configure plugins or enable updates as
part of this skill-only installation.

Verify discovery if the tool supports it. Confirm the path, version or commit,
how to invoke it and any reload or manual step still needed. If you cannot access
the filesystem, give me instructions instead of claiming it was installed.
```

## Updates

Review the change log and diff before installing an update. For copied skills, explicitly replace the chosen installation after backing up local changes. For marketplace packages, use Claude Code's documented update controls; marketplace installation does not guarantee updates are disabled. See [marketplace maintenance](https://code.claude.com/docs/en/plugins/host-marketplace.md).
