# Example: engineering proposal

Fictional example. The system, team needs and proposed work below are invented to
illustrate tone and structure, not to report a real implementation or agreement.

---

# Proposal: a common approach to reusable validation scripts

I support the shared validation library. It gives teams a useful starting point
instead of asking everyone to write the same checks again. I suggest we agree on
the script interfaces and contribution expectations before the collection grows.

The aim is not to introduce another framework. It is to make the existing building
blocks easier to combine and maintain.

## Proposed approach

| Area | Proposal |
| --- | --- |
| Inputs | Pass device roles, expected values and thresholds as parameters rather than fixing them in shared code. |
| Reusable behavior | Keep common collection and comparison functions in small, maintained modules. Search those modules before adding another implementation. |
| Validation | Require positive and negative examples so a check demonstrates both when it should pass and when it should fail. |
| Ownership | Give each shared module an owner and document the versions used by its consumers. |

The individual test should describe the procedure and expected outcome. Connection
policy, data interpretation and repeated comparison logic should have one maintained
implementation where they are genuinely shared.

## Adoption

Start with two representative checks. Have another engineer run the same code in a
different environment, changing only the inventory and expected values. Record any
assumptions that still require an implementation change.

Once the reference approach is stable, use it for new contributions and migrate
existing tests when they are next updated. This avoids a large rewrite before we
know which interfaces work well in practice.

The expected benefit is less duplicated logic and a clearer review process. We
should measure the maintenance effort during the pilot rather than assume a saving
in advance.

Could we agree on the reference checks and the owners for that pilot before making
the new contribution rules mandatory?
