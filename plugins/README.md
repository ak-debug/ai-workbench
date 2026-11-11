# Plugins

Reserved for host-specific integrations. No standalone plugin implementations are published yet; Management Slides is exposed as a skill-only marketplace package directly from its canonical `skills/` directory.

A future Claude Code plugin can use `plugins/<id>/.claude-plugin/plugin.json` with its components inside `plugins/<id>/`. Other hosts have different APIs and formats: label support accurately and document installation, permissions, hooks and network behavior.
