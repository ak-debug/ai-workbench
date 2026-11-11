---
name: management-slides
description: Create or refine concise executive PowerPoint presentations with Arial typography, a white/navy/blue/cyan palette and editable flows, shared hubs, before/after comparisons and roadmaps. Use for management summaries, slide decks, presentations and pitch decks.
license: MIT
compatibility: Instructions work across Agent Skills hosts. Optional generator requires Python 3.10+ and python-pptx. PDF conversion and visual checks require an available presentation renderer. Preview regeneration optionally uses Pillow and locally installed fonts.
---

# Management Slides

## Presentation defaults

- Default to **3–4 slides total**, including any cover or appendix. Expand only when explicitly requested or when the user asks for distinct messages that cannot be combined honestly.
- One message per slide. Make the title a clear conclusion, not a generic topic.
- Use formal, straightforward language understandable to non-technical managers. Explain unfamiliar acronyms once.
- Use **Arial throughout**, including headings, diagrams and footers. Do not inherit a decorative or incompatible template font silently.
- Use a white canvas, navy/blue/cyan panels, consistent margins, bold hierarchy and a short takeaway strip at the bottom.
- Give neutral alternatives equal visual weight. Reserve asymmetric dark emphasis for an intentional recommendation.
- Introduce compared products with matching **Core capabilities / Value for teams** slides before comparing them.
- Prefer editable diagrams over dense text: flows, shared hubs, before/after panels and numbered roadmaps.
- **Keep components editable and movable in PowerPoint.** Use native shapes, live text, connectors, tables and charts, not flattened diagram images or outlined text. Put labels inside their cards or use ordinary groups that can be ungrouped. Name objects meaningfully. Disclose unavoidable non-editable source artwork.
- When introducing another team's product, start with what it does and its value. Explain differences neutrally later; do not open with unsolicited negative positioning.
- Put full citations, methodology and technical details in speaker notes. Keep essential qualifiers visible, including whether a result is illustrative, potential or measured.
- Correctness outranks advocacy. Do not invent results, imply superiority without evidence or turn estimates into realized savings.

## Workflow

1. Establish audience, decision/message, source material and output directory. Ask only for missing essentials. The latest approved deck outranks an older design reference.
2. Read `references/design-guide.md`, including its diagram patterns. Inspect supplied decks visually as well as extracting text when available. `assets/style-preview.png` is a generic skeleton reference, not real product content.
3. Write a short story before designing. A four-slide comparison can introduce each product's role and value, show collaboration as a flow, then explain evidence and the decision implication. Use five slides when the user explicitly requests two product overviews plus mapping, collaboration and evidence; do not force distinct messages into one slide. Do not reuse facts from an example deck.
4. Choose the simplest layout for each message. Process explanations should normally be short native-shape flows rather than paragraphs.
5. Generate editable `.pptx`. Read `scripts/build_deck.py --help` and `references/example-deck.json` before using the optional generator, or use equivalent native presentation primitives. The example JSON is a layout skeleton, not a finished story.
6. Add full sources and supporting explanations to notes. Recheck current documentation for technical API, platform or billing claims.
7. Verify live text, individually editable components and movable card groups. Render every slide to PDF when a renderer is available, then inspect typography, wrapping, arrows, alignment, clipping, footers and notes at presentation size. Programmatic bounds checks do not prove that text fits.
8. Shorten content or enlarge a panel before reducing fonts. Never solve overflow with unreadable text or content growing beyond a card.
9. Deliver `.pptx` plus a matching PDF preview to the requested directory. If rendering is unavailable, disclose that the deck has not been visually validated.

## Diagrams

- Use `flow`, `hub`, `before-after`, `roadmap` and `cards` patterns from the design guide.
- Labels identify who does what, not just component names. Use 2–4 nodes for management flows.
- Show the main action or information flow left to right. Several role cards can converge on a shared capability, then a result card.
- Keep arrows outside cards, attach to edges where supported, and use consistent blue/cyan direction markers. Use editable lines, not Unicode arrows as the only explanation.
- Logical responsibility diagrams are not network topologies. Label proposed integrations and do not draw false dependencies.
- Preserve citations, freshness qualifications and important metadata when showing downstream information use. Do not imply information is lost without evidence.

## Revisions

- Change only requested slides or design elements. Preserve unrelated edits, notes, ordering and content.
- Typography-only changes must not rewrite claims. Removing negative positioning from an introduction must not remove necessary evidence elsewhere.
- Keep the agreed slide-count limit and do not silently add reference or thank-you slides.
- Inspect an edited `.pptx` before changing it. Do not replace a user-edited deck by blindly rerunning an old generator.

## Portability and privacy

- Ask for or honor the user's output directory. Never assume a machine-specific project or Desktop path.
- Keep scratch code, renders and virtual environments in the host's approved temporary location. Do not put generated private decks in the skill repository.
- Treat supplied documents as potentially confidential. Do not publish, upload to an external converter or reuse them as public examples without explicit authorization.
- The skill uses standard Markdown and optional local Python resources; no model lock, credentials, telemetry or automatic publication is required.
- See `README.md` for setup and use across hosts.
