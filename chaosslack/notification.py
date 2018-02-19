# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import EventPayload
from logzero import logger
from slackclient import SlackClient

__all__ = ["notify"]


def notify(settings: Dict[str, Any], event: EventPayload):
    """
    Send a chat message to a channel to relate this Chaos Toolkit event.

    The settings must contain:

    - `"token"`: a slack API token
    - `"channel"`: the channel where to send this event notification

    If one of these two attributes is missing, no notification is sent.
    """
    token = settings.get("token")
    channel = settings.get("channel")

    if not token:
        logger.debug("Slack notifier requires a token")
        return

    if not channel:
        logger.debug("Slack notifier requires a channel")
        return

    token = token.strip()
    channel = "#{c}".format(c=channel.lstrip("#").strip())

    sc = SlackClient(token)

    attachments = []
    attachments.append({
        "title": "Source",
        "text": event.get("phase")
    })

    attachments.append({
        "title": "Event",
        "text": event.get("name")
    })

    payload = event.get("payload")
    if payload:
        title = payload.get("title")
        if not title:
            title = payload.get("experiment", {}).get("title")
        if title:
            attachments.append({
                "title": "Experiment",
                "text": title
            })

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text="Chaos Toolkit notification",
        attachments=attachments
    )
