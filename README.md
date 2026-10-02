# Charter recipes

Small scripts built on [Charter](https://github.com/r28ai/charter), each doing one job end to end. Every one runs
with `uv run`, straight from its URL, with nothing to install first.

These are demos. To put Charter in your own agent, start from
[the docs](https://docs.r28.ai/charter) and the
[examples in the main repo](https://github.com/r28ai/charter/tree/main/examples) instead.

## Gmail

| recipe | what it does |
|---|---|
| [`gmail/reply_all.py`](gmail/reply_all.py) | Reply-all that keeps every To and Cc recipient, in the same thread |
| [`gmail/send.py`](gmail/send.py) | Send to a name like `"Müller, José"` without breaking the header |
| [`gmail/read.py`](gmail/read.py) | Read a message as its reader sees it, even when text/plain is only a "view in browser" stub |
| [`gmail/save_attachments.py`](gmail/save_attachments.py) | Save a message's attachments to disk, and show what a model would read |

They read a Google grant from `GOOGLE_TOKEN_FILE`: any JSON holding a `client_id`, `client_secret` and
`refresh_token`. `gws auth export --unmasked` writes one, and so does
[the five-step setup](https://docs.r28.ai/charter/auth/your-own-account).

```
GOOGLE_TOKEN_FILE=google.json uv run https://raw.githubusercontent.com/r28ai/charter-recipes/main/gmail/read.py <message-id>
```

The two that send print the message instead, unless given `--send`.
