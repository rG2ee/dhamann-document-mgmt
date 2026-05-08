"""Gemeinsame IMAP-Verbindung zur Protonmail Bridge."""

from __future__ import annotations

import imaplib
import os
import ssl
from pathlib import Path

from dotenv import load_dotenv


def connect() -> imaplib.IMAP4:
    """Stellt eine IMAP-Verbindung zur lokalen Protonmail Bridge her."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)

    host = os.environ["IMAP_Address"]
    port = int(os.environ["IMAP_port"])
    username = os.environ["IMAP_Username"]
    password = os.environ["IMAP_Password"]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    mail = imaplib.IMAP4(host, port)
    mail.starttls(ssl_context=ctx)
    mail.login(username, password)
    return mail
