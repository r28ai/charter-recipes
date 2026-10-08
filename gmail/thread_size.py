# /// script
# requires-python = ">=3.10"
# dependencies = ["charter-ai>=0.5.1,<0.6"]
# ///
"""What a Gmail thread costs a model, before and after Charter reads it.

threads.get returns the whole MIME tree: base64url bodies, HTML beside the
text, every header each server added. Charter's threads_get keeps the decoded
body, the headers worth reading, and each attachment's id without its bytes,
because the next call needs the id. This prints both sizes.

    GOOGLE_TOKEN_FILE=google.json uv run thread_size.py THREAD_ID  # any authorized-user JSON
"""

import argparse
import asyncio
import json

from charter import pass_through
from charter.packs import gmail

# The same tool with the response left as Gmail sent it.
as_sent = gmail.threads_get.derived(name="threads_get_as_sent", response_handler=pass_through)


async def sizes(thread_id: str) -> None:
    raw = await as_sent.ainvoke({"id": thread_id})
    kept = await gmail.threads_get.ainvoke({"id": thread_id})
    kb_raw, kb_kept = (len(json.dumps(r)) / 1000 for r in (raw, kept))
    print(f"Gmail returned {kb_raw:.1f} KB")
    print(f"Charter kept   {kb_kept:.2f} KB, {kb_raw / kb_kept:.0f}x smaller")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("thread_id")
    asyncio.run(sizes(cli.parse_args().thread_id))
