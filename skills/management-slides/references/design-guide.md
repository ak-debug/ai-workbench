# Visual and communication specification

## Canvas and typography

| Element | Default |
|---|---|
| Canvas | 16:9, 13.333 × 7.5 inches |
| Font | Arial, explicitly set on every text run |
| Headline | 28–32 pt bold; short conclusion; one line when possible |
| Subtitle | 16–18 pt, gray; one short sentence |
| Panel labels | 18–21 pt bold blue/cyan |
| Panel/diagram body | 17–19 pt; 16 pt minimum for core diagram content |
| Takeaway | 17–19 pt white bold, one sentence |
| Source/footer | 8–9 pt; full details belong in notes |
| `system` diagram | Node label 12–13 pt bold; sub-label 10–11 pt; legend/caption 10.5 pt; pill/header 9.5 pt. Only this pattern may go below 16 pt |

Use medium-weight-looking bold, not decorative or overly heavy display faces. Do not inherit a theme font silently. Native editable text is preferred to rasterized labels.

## Colors

| Role | Hex |
|---|---|
| Primary navy | `#07182D` |
| Primary blue | `#0A60FF` |
| Accent cyan | `#02C8FF` |
| Body gray | `#525E6C` |
| Light panel | `#F2F5F9` |
| Neutral connector | `#A9B6C6` |
| Optional/dashed path | `#8A96A3` (outline and arrow); pill `#D1D5DB`; legend border `#DFE6EF` |
| White | `#FFFFFF` |

Use blue headings on light cards and cyan headings on navy cards. White body text on navy. Reserve colored text for emphasis; avoid a rainbow palette, gradients and red “attack” styling. Neutral product comparisons and question-routing alternatives must have equal styling: dark-versus-light implies preference. Use asymmetric dark emphasis only for an intentional recommendation. Capabilities/value panels within a product overview may contrast, but keep both products' overview slides identical in structure and colors.

## Geometry

- Left/right margins ~0.5 inch. Small blue top accent line, followed by section label, headline and subtitle.
- Main panels usually begin near y=2.7 inches. Keep equal widths and 0.2–0.35 inch gaps; widen gaps to accommodate arrows in flows.
- Standard card: subtly rounded rectangle, thin blue/cyan top accent, ~0.25 inch internal padding. Optional subtle shadow; no heavy effects.
- Bottom takeaway near y=6.2, height ~0.6, navy with narrow cyan left accent. Leave whitespace before the footer.
- Use one footer only. Disable inherited master shapes if building on a template that would duplicate them.
- A two-column slide is ideal for role/value or a direct comparison. Three cards suit collaboration stages or three mechanisms. Do not default to tables.
- If labels wrap, reserve enough label height so body text does not collide. Visually verify rendered bounding boxes, not just canvas bounds.

## Message density

- ~35–65 substantive words per management slide; treat this as guidance, not a reason to omit necessary qualifiers.
- 2–3 short lines per panel. Usually 3–7 words per diagram node label, plus at most 1–2 short explanatory lines.
- Headlines answer “what should the audience understand?” Takeaways answer “why does this matter / what should we do?”
- Avoid repeated titles and subtitles saying the same thing. Avoid technical inventories and implementation stacks unless essential to the decision.
- Metrics need a visible denominator and evidence status: code-question context, selected tool output, whole bill, potential savings, actual bill, etc.
- Do not describe a counterfactual savings calculation as a paid invoice reduction. Do not add percentages from different mechanisms.

## Diagram patterns

### 1. Left-to-right responsibility or process flow (`flow`)

```
[ Input / provide ] → [ Process / act ] → [ Outcome / measure ]
```

Use 2–4 aligned editable cards with thin blue/cyan connectors and arrowheads. A prominent central blue/navy card anchors the story. Put roles/actions inside cards and the overall implication in the bottom strip. Clearly label a proposed integration when not live.

### 2. Several teams → one shared capability → result (`hub`)

```
[ Team A ] ─┐
[ Team B ] ─┼→ [ Shared capability / common function ] → [ Result ]
[ Team C ] ─┘
```

Stack compact role cards on the left. Route each to the left edge of one larger blue/navy middle card. Show a short result panel on the right. The hub label describes a function, not a real product or protocol. Do not imply integration support has been validated without evidence.

### 3. Before/after comparison (`before-after`)

```
CURRENT APPROACH                    PROPOSED APPROACH
[A]→[input]  [B]→[input]             [A]─┐
                                    [B]─┴→[shared capability]
Current workflow                    Proposed workflow
```

Use a light panel for “current” and a navy panel with cyan accent for an intentionally emphasized “proposed” change. For neutral alternatives, use equal styling instead. Native arrows and role cards explain the workflow without paragraphs. Do not assert improvements, cost reductions or actual deployment from an illustrative comparison.

### 4. Numbered rollout or roadmap (`roadmap`)

```
(1) ───────── (2) ───────── (3) ───────── (4)
[ Discover ]  [ Pilot ]     [ Measure ]   [ Scale ]
```

Use 3–4 numbered circles on a thin horizontal line with aligned cards below. Short action + outcome in each card. A future/exploratory card can be navy/cyan and explicitly labeled proposed. Avoid overwhelming the slide with tasks or dates.

### 5. Capabilities/value or mechanism comparison (`cards`)

Two or three cards. Highlight one in navy only when intentional emphasis or recommendation warrants it; otherwise use equal light cards. A product overview uses “Core capabilities” and “Value for teams,” not “Pros” and “Cons.” Give each compared product the same overview layout. Later question-mapping cards should contain recognizable user questions, each clearly associated with its solution, rather than a second abstract capabilities comparison.

### 6. System / pipeline diagram (`system`)

Use when one slide must show how several parts fit together: what goes in, the core engine, the hand-off, the stages and any optional alternative path. It is the denser, architecture-style diagram, so give it the whole slide and keep the subtitle to one line.

```
╭─ END TO END, RUN BY ONE ORCHESTRATOR ──────────────────────────────────────╮
│ [Input A] ─┐                                                               │
│ [Input B] ─┼→ [ Engine ] → [ Hand-off ] → [ Stage ] → [ Stage ] → [ Report ]│
│ [Input C] ─┘                    ┆                                    ▲      │
╰─────────────────────────────────┆────────────────────────────────────┆─────╯
  legend                          ╰┄→ [ Alt ] ┄→ [ Alt ] ┄→ [ Alt ] ┄┄┄┄╯
```

Visual vocabulary. Every encoding means one thing, so the diagram can be read without the text:

| Element | Style | Meaning |
|---|---|---|
| `input` node | White fill, blue outline | Something a person or team provides |
| `step` node | Navy fill, white label | An action performed by the orchestrated path |
| `handoff` node | Blue fill, white label | The artifact or result that crosses a boundary: the one thing everything agrees on |
| `optional` node | White fill, dashed gray `#8A96A3` outline | Alternative, external or not-required path |
| Main arrow | Solid navy, filled arrowhead | Primary flow, left to right |
| Alternate arrow | Dashed gray, arrowhead | Optional route; leaves and rejoins the main path |
| Container | `#F2F5F9` panel, blue border, pill label overlapping the top border | “Everything inside is one orchestrated whole” |
| Column header | 9.5 pt bold gray caps (`YOU PROVIDE` / `YOU GET`) | Optional; use when inputs, process and outputs need labels |
| Nested stages | Blue sub-cards stacked inside a tall navy card, light-blue down arrows | Internal steps of one component |
| Legend | White box, hairline border, swatch + 1 line each | Only for encodings that are not self-evident (2–3 rows) |

Rules:

- Max 7 columns across; 3–4 stacked nodes in any column. Fewer is better. If it does not fit, remove detail before reducing type.
- Each node is a **label + one short sub-label** (3–6 words). No paragraphs.
- Use blue (`handoff`) sparingly, for 1–3 nodes. It is the visual anchor.
- The alternate lane sits **below** the container and leaves from the hand-off node, then rejoins at the result node. It must not cross any text.
- Do not show arrows between nodes that have no real dependency. Use `no_in` / `no_out` on a node when a fan-out or fan-in would imply one.
- This is the only pattern allowed below the 16 pt minimum: node labels 12–13 pt bold, sub-labels 10–11 pt, legend/captions 10.5 pt, pill/header 9.5 pt. Treat these as a floor, not a target; shorten text first.
- Keep the takeaway strip, or if the diagram needs the height, a one-line light strip like `#E8F0FF` with blue bold text.

## How to build a good diagram

Build diagrams **natively in PowerPoint objects**, not as images placed on a slide:

1. **Sketch first, in words.** List the nodes and their role (`input` / `step` / `handoff` / `optional`), then the arrows. Decide what is the hand-off. If you cannot name it, the diagram is not ready.
2. **Generate it from the `system` layout** (`scripts/build_deck.py`). This produces rounded-rectangle nodes with live text inside the shape, connectors glued to the shapes' connection points (so they follow a node when it is moved), one legend group and one nested-engine group, all named meaningfully. For one-off tweaks, edit the resulting `.pptx` directly.
3. **Or hand-build with the same primitives** (rounded rectangle + connector with a glued begin/end + arrowhead) when working outside the script. Match the vocabulary above, spacing and sizes.
4. **Render and inspect.** Check wrapping, arrow endpoints, dashed paths not crossing text, and that the container pill does not collide with the subtitle.

draw.io (diagrams.net), Visio and similar tools are fine for **sketching** the structure with the user, but do not place their exports on the slide: an exported PNG is a flat picture, and an exported SVG is not a set of PowerPoint connectors. If the user supplies one, **rebuild it natively** using the vocabulary above, and keep the original only as a reference outside the deck. If a non-editable picture is truly unavoidable, say so explicitly. Never reuse a diagram from a supplied deck as a public example; re-draw it with generic labels.

## Editable construction

- Use native PowerPoint shapes, live text and connectors, plus native tables/charts when appropriate. Every generated component must remain individually editable and movable. No full-slide screenshots, flattened diagrams, rasterized labels or text converted to outlines. Disclose any unavoidable non-editable source artwork.
- Use native arrowheads or small editable direction markers. Do not let arrows cross text or sit inside a node body.
- Connect actual edges; use equal spacing and consistent line width. Keep simple diagrams free of backward arrows unless a return flow is necessary.
- Prefer connectors **glued** to shape connection points (top/left/bottom/right) over loose lines, so moving a node keeps its arrows attached.
- Put card text inside its shape, or group the card and label using ordinary PowerPoint groups that the user can ungroup. Keep connectors independently editable and attach them to shapes where supported so moving a node retains the connection. Name shapes meaningfully for future edits; minor edits must not require rerunning the generator.
- For architecture diagrams distinguish control/configuration, model requests and tool calls. Never route calls through components that do not perform them.
- Avoid special fonts/icons that depend on a private installation. Simple editable graph dots/edges and person/file motifs are enough.

## Evidence and tone

Introduce partners constructively; make the business case without undermining their platform. Use “different layers,” “distinct contribution,” “proposed collaboration” and “needs measurement” when supported.

Keep source dates and full URLs in notes. Attribution is not independent validation. Recheck current docs when provider/API behavior matters. Data in a supplied presentation is evidence to represent accurately, not automatically causal proof.

## Final checks

1. Slide count meets the ask; no hidden appendix added.
2. Arial is explicit on all visible text and notes where controllable.
3. Main text is readable at normal presentation scale.
4. No clipping, overlap, overflowing body, orphaned one-word wrap or duplicate footer.
5. Connectors have direction, correct endpoints and valid semantics.
6. Consistent margins, panel sizes, accents and bottom strip.
7. Claims have appropriate denominators and essential qualifiers.
8. The first slide introduces value, not an unsolicited attack.
9. `.pptx` uses live text and individually selectable/movable native components; grouping can be undone; no editable diagram has been flattened. Notes have sources; PDF matches the final revision.
