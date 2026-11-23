# Changelog

## 1.8.0 (unreleased)

- Management Slides 1.2.0: add a design kit (`deck_kit.py`) with one type scale, one grid and
  measured text fit, plus `lint_deck.py` and `render_preview.py` for checking finished decks.
- Fix `build_deck.py` setting fonts on the paragraph instead of the run: PowerPoint ignores
  paragraph defaults, so headlines and footers could render in the theme font and size.
- Bring the `system` layout and slide chrome onto the 12 pt minimum (footer 10 pt) and name
  slide-chrome shapes. Document the type scale, grid and a "deck looks bad" diagnosis in the
  skill and design guide.

## 1.7.0 (unreleased)

- Management Slides 1.1.0: add a `system` diagram pattern (container, role-coded nodes,
  nested stages, dashed optional path and legend), a generator layout that glues
  connectors to shapes, and guidance on building diagrams natively rather than placing
  draw.io or other exported images.

## 1.6.0 (unreleased)

- Include social posts in the writing skill and global guidance, with audience-aware tone.

## 1.5.0 (unreleased)

- Update the LinkedIn example and guidance to reflect the author’s approved tone.

## 1.4.0 (unreleased)

- Improve the technical blog and LinkedIn examples with concrete reasoning and a more natural voice.

## 1.3.0 (unreleased)

- Add LinkedIn post guidance and a fictional technical achievement example to
  Personal Writing Style.

## 1.2.0 (unreleased)

- Add technical blog writing guidance informed by the author's public forensics
  posts, with a fictional file-integrity investigation as an example.

## 1.1.0 (unreleased)

- Add the instruction-only Personal Writing Style skill, a detailed writing guide
  and newly written fictional proposal, team-message and technical-feedback examples.
- Include a separate global-instruction snippet and explain why consistent defaults
  need both global guidance and the on-demand skill.
- Document OpenCode and Claude Code setup, delegated-agent handoffs, verification,
  privacy boundaries and a review-first installation prompt.
- Add a Claude Code marketplace entry for the new skill and package regression tests.
- Existing Management Slides package remains at version 1.0.0.

## 1.0.0

- Initial multi-purpose AI Workbench structure for skills, tools and plugins.
- Portable Management Slides skill and optional editable PowerPoint generator.
- New generic skeleton preview with a reproducible drawing script.
- Claude Code marketplace entry with a single canonical skill copy.
- Installation documentation, structural tests and publication guardrails.
