# Writing guide

## Voice

Professional, direct, practical and constructive. Sound like an engineer or colleague
who understands the subject and respects the reader's time. Use first person when
writing on the user's behalf and it fits the message, but do not add personal
experience, emotions or commitments that were not supplied.

Improve spelling, grammar and flow without turning plain wording into corporate
language. "I suggest we test this with two teams first" is usually better than
"It is imperative to leverage a comprehensive cross-functional validation strategy."

## Content

- Start with why the text is being sent or what it proposes.
- Give just enough context to make the recommendation understandable.
- Identify concrete problems instead of broad judgments such as "the architecture
  is bad" or "this will never work."
- Link recommendations to practical benefits: clearer ownership, less duplication,
  easier review or more reliable operation. Do not invent percentages or savings.
- Acknowledge useful existing work when relevant; do not manufacture praise as a
  preface to every criticism.
- Include limits and open decisions. "This has not been tested" must not become
  "This works" during editing.
- Make the request clear, but do not force a call to action onto an informational note.

## Structure by task

| Format | Useful starting structure | Avoid |
| --- | --- | --- |
| Team message | Context, main concern, suggestion, next step | A miniature white paper |
| Short email | Purpose, essential detail, request | Unneeded headings and tables |
| Proposal | Purpose, recommendation, practical details, tradeoffs, adoption | A broad architecture redesign unrelated to the ask |
| Technical feedback | Observation, impact, recommendation, verification needed | Treating a suspected risk as a confirmed incident |
| Report | Outcome, evidence, limitations, next decisions | A diary of reads, searches and tool calls |
| Documentation | Purpose, prerequisites, instructions, checks, limitations | Undocumented assumptions or promises of universal compatibility |

These are starting points, not required headings. Use only what the draft needs.

## Sentence and formatting habits

- Prefer direct verbs: "use," "check," "share," "agree," "test" and "review."
- Mix short and medium-length sentences. Use natural contractions when appropriate.
- Keep each paragraph focused. Break dense paragraphs instead of making every
  sentence a bullet.
- Use parallel bullets for related points; do not add numbered lists to imply an
  ordering that does not exist.
- Use tables for real comparisons or mappings, not to make a short note look formal.
- Use bold sparingly. A few useful labels are enough.
- Include code or a folder tree only when it clarifies the proposal. Label illustrative
  APIs or proposed structures rather than presenting them as existing interfaces.
- Do not impose arbitrary word limits when accuracy requires more detail. If the
  user asks for brevity, cut repetition before cutting qualifications.

## Common edits

| Instead of | Prefer |
| --- | --- |
| "In today's rapidly evolving landscape..." | Start with the actual subject |
| "This revolutionary solution will guarantee..." | Describe the specific capability and its limits |
| "We should improve standardization" | Say which inputs, interfaces or checks should be standardized |
| "The team has agreed" when no agreement exists | "I propose" or "We could consider" |
| "Everything passed" after a limited check | Name the check and what it does not establish |
| "Happy to take full ownership" without authorization | Ask for agreement on the next step |

Do not treat this table as a word blacklist. Context and meaning matter more than
removing a particular expression.

## Facts and boundaries

Distinguish these explicitly when relevant:

- **Observed:** supported by the supplied material or actual verification.
- **Proposed:** a recommendation, not an already-adopted decision.
- **Assumed:** necessary context that has not been confirmed.
- **Unverified:** something that still requires evidence.

Use citations where the reader needs traceability; do not overwhelm an ordinary
team message with links. Never invent references to make a draft look researched.
Do not add private names, customer details, internal links or local paths to public
examples. Material supplied for editing is not permission to publish it elsewhere.

## Working with corrections

Apply the user's corrections to the current draft. If they want a preference made
persistent, propose a small update to this guide or the global snippet and preserve
existing instructions. Do not silently add private correspondence to a public
example collection or let one document-specific request become a universal rule.

## Quick quality check

Read the draft once as the intended recipient. Remove filler, unsupported certainty,
unnecessary headings and repeated conclusions. Check the names, claims, status and
request against the supplied facts. The final draft should be usable without an
explanation of the editing process.
