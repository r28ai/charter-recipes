# /// script
# requires-python = ">=3.10"
# dependencies = ["charter-ai>=0.5.1,<0.6"]
# ///
"""Declare a tool word for word from the docs, then cut it to the job.

gmail.messages_list carries every parameter Google documents for
users.messages.list, in Google's own words. A search agent needs two of them,
and derived() keeps those two: the model never sees the rest.
No credentials, no network.

    uv run cut_to_the_job.py
"""

from charter.packs import gmail

fields = gmail.messages_list.args_schema.model_fields
print("declared:        ", list(fields))
print("in google's words:", repr(fields["includeSpamTrash"].description))

search = gmail.messages_list.derived(name="search_mail", keep={"q", "maxResults"})
print("the model sees:   ", search.paths())
