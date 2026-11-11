# Third-party notices

No third-party code, images or documentation are vendored. The layout follows common public conventions. The presentation skill and deck builder are the maintainer's own work; the public documentation and examples are newly written and generic.

Design references, not vendored implementations:

- [Agent Skills standard](https://agentskills.io/)
- [Anthropic's public skills repository](https://github.com/anthropics/skills): self-contained `skills/` folders and root-based marketplace entries.
- [Superpowers](https://github.com/obra/superpowers): portable skills with host-specific installation documentation.
- [Claude Code marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces)
- [OpenCode skills documentation](https://opencode.ai/docs/skills)

Optional dependencies are installed separately and retain their upstream licenses:

- [python-pptx](https://github.com/scanny/python-pptx), MIT.
- [Pillow](https://github.com/python-pillow/Pillow), HPND.
- Presentation renderers such as LibreOffice are external applications, not bundled.

Arial is a separately licensed font and is not distributed here. The public preview was drawn using an installed font; regenerating it requires your own suitable font installation. The PowerPoint generator specifies Arial by name. Renderers may substitute a different font if Arial is unavailable.
