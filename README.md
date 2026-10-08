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
| [`gmail/thread_size.py`](gmail/thread_size.py) | What a thread costs a model: Gmail's raw response against what Charter keeps |
| [`gmail/cut_to_the_job.py`](gmail/cut_to_the_job.py) | Declare `messages.list` word for word from Google's docs, then cut it to the two fields a search needs |

They read a Google grant from `GOOGLE_TOKEN_FILE`: any JSON holding a `client_id`, `client_secret` and
`refresh_token`. `gws auth export --unmasked` writes one, and so does
[the five-step setup](https://docs.r28.ai/charter/auth/your-own-account).

```
GOOGLE_TOKEN_FILE=google.json uv run https://raw.githubusercontent.com/r28ai/charter-recipes/main/gmail/read.py <message-id>
```

The two that send print the message instead, unless given `--send`.

## No credentials needed

These read Charter's declarations and print what a model would see. No account, no network.

| recipe | what it shows |
|---|---|
| [`gmail/cut_to_the_job.py`](gmail/cut_to_the_job.py) | 6 parameters declared in Google's words, 2 handed to the model |
| [`stripe/gloss.py`](stripe/gloss.py) | Stripe's description of a refund `amount`, and the line beside it that stops $15.00 going out as fifteen cents |
| [`linear/schema_cost.py`](linear/schema_cost.py) | One Linear tool is 45,072 tokens of schema, and one field is 44,828 of them |
| [`gdocs/edit_text_only.py`](gdocs/edit_text_only.py) | 33 kinds of Docs edit behind one URL, cut to the 3 a text editor needs |

```
uv run https://raw.githubusercontent.com/r28ai/charter-recipes/main/linear/schema_cost.py
```
