# -*- coding: utf-8 -*-
import time
from unittest.mock import MagicMock, patch

from chaoslib.notification import RunFlowEvent
from slack import WebClient

from chaosslack.notification import notify


@patch("chaosslack.notification.WebClient", autospec=True)
def test_notify(sc: WebClient):
    payload = {"msg": "hello", "ts": str(time.time())}
    event_payload = {
        "event": str(RunFlowEvent.RunStarted),
        "phase": "run",
        "payload": payload,
    }
    c = MagicMock()
    sc.return_value = c
    c.chat_postMessage.return_value = {"data": {"ok": True}}
    notify({"token": "xyz", "channel": "#general"}, event_payload)
