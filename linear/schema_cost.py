# /// script
# requires-python = ">=3.10"
# dependencies = ["charter-ai>=0.5.1,<0.6"]
# ///
"""Find the field that makes a tool expensive.

linear.issues_list_full declares Linear's issue query word for word, and its
schema goes to the model on every turn. paths(by_cost=True) prunes each branch
for real and regenerates the schema, so each number is what cutting that
field saves. No credentials, no network.

    uv run schema_cost.py
"""

from charter import format_path_costs, schema_tokens
from charter.packs import linear

tool = linear.issues_list_full
print("tokens of schema:", schema_tokens(tool))
print(format_path_costs(tool.paths(under="variables", by_cost=True)))
