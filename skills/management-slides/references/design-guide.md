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

## Editable construction

- Use native PowerPoint shapes, live text and connectors, plus native tables/charts when appropriate. Every generated component must remain individually editable and movable. No full-slide screenshots, flattened diagrams, rasterized labels or text converted to outlines. Disclose any unavoidable non-editable source artwork.
- Use native arrowheads or small editable direction markers. Do not let arrows cross text or sit inside a node body.
- Connect actual edges; use equal spacing and consistent line width. Keep simple diagrams free of backward arrows unless a return flow is necessary.
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
