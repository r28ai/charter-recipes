# /// script
# requires-python = ">=3.10"
# dependencies = ["charter-ai>=0.5.1,<0.6"]
# ///
"""One URL, many possible edits. Allow three.

Every edit to a Google Doc is the same POST to the same path with the same
token. The kind of edit is inside the body, so anything that only sees the
method, host and path can't tell insertText from deleteTableRow. Cutting the
tool can: the model can only express the edits you keep.
No credentials, no network.

    uv run edit_text_only.py
"""

from charter.packs import gdocs

full = gdocs.documents_batch_update
edit = full.derived(name="edit_text", keep={"insert_text", "delete_content_range", "replace_all_text"})

print("full:     ", full.method, full.url_template, len(full.paths(under="body.requests")), "kinds of edit")
print("edit_text:", edit.method, edit.url_template, edit.paths(under="body.requests"))
