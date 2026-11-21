# Personal Writing Style

A portable, instruction-only skill for professional, direct and natural proposals,
engineering feedback, team messages, emails, reports, documentation and technical
blog posts. It keeps the user's intent and technical meaning without unnecessary
formality or filler.

## Use both global instructions and the skill

**For a consistent default, complete both setup steps below.** Installing a skill
alone does not make its full contents an always-on instruction for every agent.

| Layer | Purpose |
| --- | --- |
| Global instructions | A short writing baseline available across projects, including a request to load the skill for substantial drafts. |
| Writing skill | The detailed workflow and relevant examples, loaded for a drafting task. |

The two layers improve consistency; they are not hard enforcement. Agents, delegated
sessions, organization policies and products differ. No single local file controls
every agent tool or cloud session. A repository URL alone installs neither layer.

## What's included

```text
personal-writing-style/
├── SKILL.md
├── README.md
├── global-instructions.md
└── references/
    ├── writing-guide.md
    └── examples/
        ├── proposal.md
        ├── team-message.md
        ├── technical-blog-post.md
        └── technical-feedback.md
```

- [SKILL.md](SKILL.md) selects the relevant guide and example.
- [Global instructions](global-instructions.md) provide the short baseline to merge.
- [Writing guide](references/writing-guide.md) explains voice, structure, evidence and editing.
- [Examples](references/examples/) are newly written fictional samples, not private correspondence.

## Step 1: install the complete skill folder

Review a release or commit of [AI Workbench](https://github.com/ak-debug/ai-workbench),
then copy this entire folder to **one** supported personal location:

| Host | Skill location | Explicit invocation |
| --- | --- | --- |
| OpenCode | `~/.agents/skills/personal-writing-style/` or `~/.config/opencode/skills/personal-writing-style/` | `@personal-writing-style` |
| Claude Code, standalone skill | `~/.claude/skills/personal-writing-style/` | `/personal-writing-style` |
| Other hosts | Use that host's documented skill or reference mechanism | Use that host's invocation syntax |

Keep `SKILL.md` directly inside the selected folder and retain `references/` and
`global-instructions.md`. Avoid duplicate installations with the same skill ID.
The folder is plain Markdown: no Python dependencies, scripts or services are needed.

As an alternative in Claude Code, use the marketplace package:

```text
/plugin marketplace add ak-debug/ai-workbench
/plugin install personal-writing-style@ai-workbench
/personal-writing-style:personal-writing-style
```

That installs the skill, **not the global instructions**. Use the namespaced skill
name when invoking this installation. Marketplace paths are checked structurally;
live installation and writing quality must still be verified in your own host.

## Step 2: merge the global writing instructions

Read [global-instructions.md](global-instructions.md) and merge its section into the
host's persistent **user-level** instructions:

| Host | Global instruction destination |
| --- | --- |
| OpenCode | `~/.config/opencode/AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` |
| Other hosts | Its documented global/custom instructions; attach the guide manually if local files are not supported |

Preserve existing instructions and resolve conflicting preferences. Do not replace
the entire file, paste credentials, or change project/organization policies.
If the skill is installed as a marketplace package, its namespaced invocation is
`personal-writing-style:personal-writing-style`; the snippet allows that equivalent.

The snippet has enough guidance to help on its own, but it does not contain every
reference. The skill tells the agent to read the relevant example; supporting files
are not assumed to load automatically. Merely putting a file beside `SKILL.md` does
not register it as global instructions.

OpenCode also supports configured instruction files, but no host-specific config
change is required for the setup above. For cloud or remote agents, make the two
layers available in that environment: a local installation does not travel there
automatically. When delegating, pass the writing expectations in the handoff rather
than assuming the child agent inherited the parent's skill or memory.

## Verify the setup

1. Use your host's skill list or explicit invocation to confirm discovery. In OpenCode,
   use `/reload` if needed; in Claude Code, use `/reload-skills` if needed.
2. Confirm through the host's instruction/context view that the global section is
   included. If no such view exists, inspect the configured source and its documented
   loading rules; the agent's claim alone is not proof of persistent configuration.
3. In a separate session/project, ask for a short team message **without naming the
   skill**. Check the baseline style and, if the host exposes it, whether the skill
   was loaded. Relevance-based loading is not guaranteed.
4. Invoke the skill explicitly for a substantial proposal and compare it with the
   appropriate example. Check factual qualifications as well as tone.

Example request:

> Draft a short note proposing a shared handover checklist. Support the idea, explain
> why service-specific checks still matter, and suggest a small pilot. Keep it natural
> and constructive; do not imply anyone has already agreed.

Then try a one-paragraph email, a longer proposal and technical review feedback.
The voice should be consistent without giving all four the same headings or length.

## Shareable installation prompt

```text
Set up the personal-writing-style package from ak-debug/ai-workbench for this host.
Use a reviewed release or commit containing skills/personal-writing-style, and record
the exact commit. Read that folder's README.md before making changes.

There are TWO setup steps:
1. Copy the complete skill folder to this host's documented personal skill location.
2. Show me a diff merging global-instructions.md into my existing global instructions.
   Ask for approval before applying that global-file change. Preserve unrelated rules.

Do not overwrite an existing skill without asking. Do not execute downloaded scripts,
install packages, enable hooks or plugins, or upload private examples. If the skill is
already installed through the marketplace, do not add a duplicate standalone copy.

Verify what this host can actually discover/load. Report the skill path or package,
instruction file, commit and any remaining manual steps. Do not claim cross-tool,
cloud or delegated-agent coverage without checking those environments separately.
```

## Boundaries and maintenance

- This skill guides style, not correctness by itself. Verify factual claims against
  supplied evidence; it does not research or certify a document automatically.
- It does not send messages, publish files, change global instructions or save memory.
- A request to match the voice does not authorize invented anecdotes or commitments.
- Read user-provided documents only when needed and authorized. Examples are not
  instructions to upload private text or copy facts into an unrelated draft.
- Add new public examples only when they are newly written, generic and reviewed.
  Never publish private correspondence to improve a style reference.
- Review updates and merge them deliberately. Copied skills and copied global snippets
  do not update each other automatically. Keep one maintained source and inspect diffs.
- Human review is needed. Static tests can check package structure and references,
  not guarantee natural writing or identical behavior across models.

References: [OpenCode skills](https://opencode.ai/docs/skills),
[OpenCode instructions](https://opencode.ai/docs/rules),
[Claude Code skills](https://code.claude.com/docs/en/skills),
[Claude Code memory/instructions](https://code.claude.com/docs/en/memory).

The repository is MIT-licensed. Include its LICENSE when redistributing a standalone
copy. No private source documents or third-party writing samples are bundled.
