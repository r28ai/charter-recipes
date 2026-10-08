# /// script
# requires-python = ">=3.10"
# dependencies = ["charter-ai>=0.5.1,<0.6"]
# ///
"""The line that stops a $15.00 refund going out as fifteen cents.

A small model read 15.00 off a spreadsheet and sent amount=15, a valid refund
of fifteen cents. Stripe's description says "smallest currency unit". The pack
keeps those words as they are and puts one line of its own beside them, a
Gloss, which the model reads with the field and loses with it.
No credentials, no network.

    uv run gloss.py
"""

from textwrap import fill

from charter.packs import stripe

refund = stripe.refunds_create
theirs = refund.args_schema.model_fields["amount"].description
sent = refund.to_json_schema()["parameters"]["properties"]["amount"]["description"]

print("stripe's words:\n" + fill(theirs, 76))
print("\nwhat the model reads on top:\n" + fill(sent.removeprefix(theirs).strip(), 76))
