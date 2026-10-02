"""The Gmail recipes, run against a mocked Gmail API: no credentials, no network."""

import base64
import email
import email.policy
import importlib.util
import json
import sys
from pathlib import Path

import httpx
import respx

from charter.auth import StaticTokenProvider
from charter.packs import gmail

RECIPES = Path(__file__).resolve().parent.parent / "gmail"
API = "https://gmail.googleapis.com/gmail/v1/users/me/messages"


def load(name: str):
    """Import a recipe by path, the way `uv run` would execute it."""
    spec = importlib.util.spec_from_file_location(f"recipe_{name}", RECIPES / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def b64(data: bytes) -> str:
    """Gmail's form: base64url, unpadded."""
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def sent_message(route):
    """The request body a mocked messages.send received, and its RFC 822 message parsed."""
    body = json.loads(route.calls.last.request.content)
    raw = body["raw"]
    parsed = email.message_from_bytes(
        base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)), policy=email.policy.default
    )
    return body, parsed


def test_every_recipe_is_short_enough_to_read():
    for path in RECIPES.glob("*.py"):
        lines = len(path.read_text().splitlines())
        assert lines <= 60, f"{path.name} is {lines} lines"


@respx.mock
async def test_reply_all_keeps_a_cc_that_outlook_spelled_in_capitals():
    gmail.configure(StaticTokenProvider("tok"))
    headers = [
        {"name": "Delivered-To", "value": "me@example.com"},
        {"name": "From", "value": "Ada <ada@example.com>"},
        {"name": "To", "value": "me@example.com"},
        {"name": "CC", "value": "Bob <bob@example.com>, cy@example.com"},
        {"name": "Subject", "value": "Q4"},
        {"name": "Message-ID", "value": "<m1@example.com>"},
    ]
    respx.get(f"{API}/m1").mock(
        return_value=httpx.Response(
            200, json={"id": "m1", "threadId": "t1", "payload": {"headers": headers}}
        )
    )
    send = respx.post(f"{API}/send").mock(
        return_value=httpx.Response(200, json={"id": "m2", "threadId": "t1"})
    )
    respx.get(f"{API}/m2").mock(
        return_value=httpx.Response(200, json={"id": "m2", "payload": {"headers": headers[1:2]}})
    )

    await load("reply_all").reply_all("m1", "Thanks", send=True)

    body, message = sent_message(send)
    assert body["threadId"] == "t1"
    assert message["To"] == "Ada <ada@example.com>"
    assert message["Cc"] == "Bob <bob@example.com>, cy@example.com"
    assert message["Subject"] == "Re: Q4"
    assert message["In-Reply-To"] == message["References"] == "<m1@example.com>"


async def test_send_encodes_the_name_rather_than_splitting_it(capsys):
    await load("send").send("you@example.com", really=False)

    printed = capsys.readouterr().out
    assert "To: =?utf-8?q?M=C3=BCller=2C_Jos=C3=A9?= <you@example.com>" in printed
    assert "Müller" not in printed


@respx.mock
async def test_read_returns_the_html_when_text_plain_is_a_stub(capsys):
    gmail.configure(StaticTokenProvider("tok"))
    html = "<p>" + " ".join(f"word{i}" for i in range(40)) + "</p>"
    payload = {
        "mimeType": "multipart/alternative",
        "parts": [
            {"mimeType": "text/plain", "body": {"data": b64(b"View this email in your browser")}},
            {"mimeType": "text/html", "body": {"data": b64(html.encode())}},
        ],
    }
    respx.get(f"{API}/m1").mock(
        return_value=httpx.Response(200, json={"id": "m1", "payload": payload})
    )

    await load("read").read("m1")

    printed = capsys.readouterr().out
    assert "text/plain part: 6 words" in printed
    assert "Charter's bodyText: 40 words" in printed
    assert "word39" in printed  # the whole body, not a prefix


@respx.mock
async def test_save_attachments_writes_the_file_and_tells_a_model_it_is_binary(tmp_path, capsys):
    gmail.configure(StaticTokenProvider("tok"))
    pdf = b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n" + bytes(range(256))
    part = {
        "mimeType": "application/pdf",
        "filename": "../../report.pdf",
        "body": {"attachmentId": "a1", "size": len(pdf)},
    }
    respx.get(f"{API}/m1").mock(
        return_value=httpx.Response(200, json={"id": "m1", "payload": {"parts": [part]}})
    )
    respx.get(f"{API}/m1/attachments/a1").mock(
        return_value=httpx.Response(200, json={"size": len(pdf), "data": b64(pdf)})
    )

    await load("save_attachments").save("m1", tmp_path)

    assert (tmp_path / "report.pdf").read_bytes() == pdf  # and never outside tmp_path
    assert "<no content: it is a binary file" in capsys.readouterr().out
