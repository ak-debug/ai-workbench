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
- **One type scale, one grid, nothing below 12 pt.** Use only the sizes in the design guide's type table (title 28, heading 18, body 16, dense 14, label 12, footer 10; cover 44/24). Every slide's content starts at y=2.3 and ends at y=5.95. A deck with a dozen near-identical font sizes and panels that start at different heights looks unprofessional even when each slide is fine. If text does not fit, cut words or enlarge the panel: never shrink type.
- **Text fit is measured, not guessed.** Build with `scripts/deck_kit.py`, which measures text with real Arial metrics and refuses to build when anything overflows. Then run `scripts/lint_deck.py` on the finished file. A clean build is not proof the slide looks right: still render and look at it.
- Use a white canvas, navy/blue/cyan panels, consistent margins, bold hierarchy and a short takeaway strip at the bottom.
- Give neutral alternatives equal visual weight. Reserve asymmetric dark emphasis for an intentional recommendation.
- Introduce compared products with matching **Core capabilities / Value for teams** slides before comparing them.
- Prefer editable diagrams over dense text: flows, shared hubs, before/after panels, numbered roadmaps and system diagrams.
- **Keep components editable and movable in PowerPoint.** Use native shapes, live text, connectors, tables and charts, not flattened diagram images or outlined text. Put labels inside their cards or use ordinary groups that can be ungrouped. Name objects meaningfully. Disclose unavoidable non-editable source artwork.
- When introducing another team's product, start with what it does and its value. Explain differences neutrally later; do not open with unsolicited negative positioning.
- Put full citations, methodology and technical details in speaker notes. Keep essential qualifiers visible, including whether a result is illustrative, potential or measured.
- Correctness outranks advocacy. Do not invent results, imply superiority without evidence or turn estimates into realized savings.

## Workflow

1. Establish audience, decision/message, source material and output directory. Ask only for missing essentials. The latest approved deck outranks an older design reference.
2. Read `references/design-guide.md`, including its diagram patterns. Inspect supplied decks visually as well as extracting text when available. `assets/style-preview.png` is a generic skeleton reference, not real product content.
3. Write a short story before designing. A four-slide comparison can introduce each product's role and value, show collaboration as a flow, then explain evidence and the decision implication. Use five slides when the user explicitly requests two product overviews plus mapping, collaboration and evidence; do not force distinct messages into one slide. Do not reuse facts from an example deck.
4. Choose the simplest layout for each message. Process explanations should normally be short native-shape flows rather than paragraphs.
5. Build the deck as editable `.pptx`.
   - **Default: write a small builder on `scripts/deck_kit.py`** (type scale, grid, `card`, `table`, `node`, `badge`, `link`, `base`, `row_x`, `finish`). One function per layout, content from a JSON spec. Call `deck_kit.finish()` after the last slide: it raises one error listing every overflow, so fix them all in one pass. A worked example is `references/example-builder.py`.
   - `scripts/build_deck.py` is the original generator with six simple layouts (`cards`, `flow`, `hub`, `before-after`, `roadmap`, `system`). Keep using it only for a quick 3–4 slide summary whose text is short; its fixed card heights do not check fit. Read its help and `references/example-deck.json` before use.
6. Add full sources and supporting explanations to speaker notes. Recheck current technical documentation for claims about APIs, caching, clients or platforms. Detail you cut from a slide for fit belongs here, not nowhere.
7. Check that labels are live text and diagram components are individually selectable/movable, with no flattened replacement for editable content. Then **verify in this order**:
   1. `python scripts/lint_deck.py deck.pptx`: must report 0 errors (type below 12 pt, text overflowing its shape, non-Arial runs, off-canvas shapes). Read the warnings: overlaps and very heavy slides usually need a layout fix.
   2. `python scripts/render_preview.py deck.pptx OUTDIR`: render every slide and look at the contact sheets, then zoom on anything doubtful. Programmatic checks, including measured fit, **do not prove** a slide looks right.
8. Shorten content or enlarge a panel before reducing fonts. Never solve overflow with unreadable text or content growing beyond a card.
9. Deliver `.pptx` plus a matching PDF preview to the requested directory. If rendering is unavailable, disclose that the deck has not been visually validated.

## Diagrams

- Use `flow`, `hub`, `before-after`, `roadmap`, `cards` and `system` patterns from the design guide. Use `system` when one slide must show inputs, an engine, a hand-off, stages and an optional alternative path (an architecture-style diagram with a container, role-coded nodes, dashed optional paths and a legend).
- Build diagrams from **native PowerPoint shapes and glued connectors**, never as a placed picture. Sketching in draw.io/Visio with the user is fine, but rebuild the result natively rather than inserting an export. See "How to build a good diagram" in the design guide.
- Labels identify who does what, not just component names. Use 2–4 nodes for management flows; the `system` pattern may use up to 7 columns with a label plus one short sub-label each.
- Show the main action or information flow left to right. Several role cards can converge on a shared capability, then a result card.
- Keep arrows outside cards, attach to edges where supported, and use consistent blue/cyan direction markers. Use editable lines, not Unicode arrows as the only explanation.
- Logical responsibility diagrams are not network topologies. Label proposed integrations and do not draw false dependencies.
- Preserve citations, freshness qualifications and important metadata when showing downstream information use. Do not imply information is lost without evidence.

## Revisions

- Change only requested slides or design elements. Preserve unrelated edits, notes, ordering and content.
- Typography-only changes must not rewrite claims. Removing negative positioning from an introduction must not remove necessary evidence elsewhere.
- Keep the agreed slide-count limit and do not silently add reference or thank-you slides.
- Inspect an edited `.pptx` before changing it. Do not replace a user-edited deck by blindly rerunning an old generator.

## When the user says a deck "looks bad"

Diagnose with numbers before touching anything: run `scripts/lint_deck.py` on the current file and render it. The usual root causes, in order of frequency:

1. **Too many font sizes and sizes below 12 pt.** Fix at the scale, not slide by slide.
2. **Content starting and ending at different heights** from slide to slide. Move everything onto the grid.
3. **Cards sized by hand, not by their text**: half-empty cards next to cramped ones. Size from measured text; share spare height; use the `heading` size for sparse cards.
4. **Tags straddling card edges, navy tags on navy panels, caption lines colliding with the row above.**
5. **Shadows** (`p:style` theme reference) that render differently per application. `deck_kit` shapes are flat.
6. **Copy written for reading, shown at 16 pt.** Cut words and move the detail to notes; keep every number and qualifier on the slide.

Fix the kit or builder once, rebuild, lint, render. If the same defect could appear in the next deck, fix it in `deck_kit.py` or the design guide, not only in this deck.

## Portability and privacy

- Ask for or honor the user's output directory. Never assume a machine-specific project or Desktop path.
- Keep scratch code, renders and virtual environments in the host's approved temporary location. Do not put generated private decks in the skill repository.
- Treat supplied documents as potentially confidential. Do not publish, upload to an external converter or reuse them as public examples without explicit authorization.
- The skill uses standard Markdown and optional local Python resources; no model lock, credentials, telemetry or automatic publication is required.
- See `README.md` for setup and use across hosts.
