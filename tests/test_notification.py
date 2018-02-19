# -*- coding: utf-8 -*-
import time
import types
from unittest.mock import MagicMock, patch

from chaoslib.notification import RunFlowEvent
import pytest
import requests
import requests_mock

from chaosslack.notification import notify


def test_notify():
    payload = {
        "msg": "hello",
        "ts": str(time.time())
    }
    event_payload = {
        "event": str(RunFlowEvent.RunStarted),
        "phase": "run",
        "payload": payload
    }
    with requests_mock.mock() as m:
        m.post(
            'https://slack.com/api/chat.postMessage',
            status_code=200,
            json={
                "ok": True,
                "channel": "C1H9RESGL",
                "ts": "1503435956.000247"
            }
        )

        notify(
            {
                "token": "xop-1234",
                "channel": "#general"
            },
            event_payload
        )

        assert m.called