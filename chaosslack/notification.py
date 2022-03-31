# -*- coding: utf-8 -*-
import json
import warnings
from typing import Any, Dict

from chaoslib.types import EventPayload
from logzero import logger
from slack import WebClient
from slack.errors import SlackApiError

__all__ = ["notify"]


def notify(settings: Dict[str, Any], event: EventPayload):
    """
    Send a chat message to a channel to relate this Chaos Toolkit event.

    The settings must contain:

    - `"token"`: a slack API token
    - `"channel"`: the channel where to send this event notification

    If one of these two attributes is missing, no notification is sent.

    """
    warnings.warn(
        "Notifications have been deprecated, please switch to using the "
        "control instead",
        DeprecationWarning,
        stacklevel=2,
    )

    # This function is ugly.

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

    sc = WebClient(token=token)

    phase = event.get("phase")

    color = "#439FE0"
    icon = "https://avatars1.githubusercontent.com/u/32068152?s=16&v=4"

    attachments = []
    fields = []
    activities_fields = []
    steady_states_fields = []
    rollbacks_fields = []

    main_attachement = {
        "fields": fields,
        "color": color,
        "ts": event.get("ts"),
        "footer_icon": icon,
        "footer": "Chaos Toolkit",
    }
    attachments.append(main_attachement)

    steady_states_attachment = {
        "text": "Steady State",
        "fields": steady_states_fields,
        "color": color,
        "ts": event.get("ts"),
        "footer_icon": icon,
        "footer": "Chaos Toolkit",
    }

    activities_attachment = {
        "text": "Failed Activities",
        "fields": activities_fields,
        "color": "danger",
        "ts": event.get("ts"),
        "footer_icon": icon,
        "footer": "Chaos Toolkit",
    }

    rollbacks_attachment = {
        "text": "Failed Rollbacks",
        "fields": rollbacks_fields,
        "color": "danger",
        "ts": event.get("ts"),
        "footer_icon": icon,
        "footer": "Chaos Toolkit",
    }

    fields.append({"title": "Source", "value": phase, "short": True})

    fields.append({"title": "Event", "value": event.get("name"), "short": True})

    payload = event.get("payload")
    if payload and isinstance(payload, dict):
        title = payload.get("title")
        if not title:
            title = payload.get("experiment", {}).get("title")
        if title:
            fields.append(
                {"title": "Experiment", "value": title, "short": False}
            )

        hypo = payload.get("steady-state-hypothesis")
        if not hypo:
            hypo = payload.get("experiment", {}).get("steady-state-hypothesis")
        title = hypo.get("title") if hypo else "N/A"
        steady_states_fields.append(
            {"title": "Hypothesis", "value": title, "short": False}
        )

        steady_states = payload.get("steady_states")
        if steady_states:
            before = steady_states.get("before")
            if before:
                met = before["steady_state_met"]
                msg = "ok" if met else "not met"

                steady_states_fields.append(
                    {"title": "Before", "value": msg, "short": False}
                )

                if not met:
                    steady_states_attachment["color"] = "warning"
                    probe = before["probes"][-1]
                    msg = probe.get("output")
                    if not msg and probe.get("exception"):
                        msg = probe.get("exception")[-1].strip()
                    steady_states_fields.append(
                        {
                            "title": "Tolerance Output",
                            "value": "```{}```".format(msg),
                            "short": False,
                        }
                    )

            after = steady_states.get("after")
            if after:
                met = after["steady_state_met"]
                msg = "ok" if met else "not met"

                steady_states_fields.append(
                    {"title": "After", "value": msg, "short": False}
                )

                if not met:
                    steady_states_attachment["color"] = "danger"
                    probe = after["probes"][-1]
                    msg = probe.get("output")
                    if not msg and probe.get("exception"):
                        msg = probe.get("exception")[-1].strip()
                    steady_states_fields.append(
                        {
                            "title": "Tolerance Output",
                            "value": "```{}```".format(msg),
                            "short": False,
                        }
                    )

        runs = payload.get("run")
        if runs:
            for run in runs:
                if run["status"] == "failed":
                    msg = run.get("output")
                    if not msg and run.get("exception"):
                        msg = run.get("exception")[-1].strip()
                    activities_fields.append(
                        {
                            "title": run.get("activity").get("name"),
                            "value": "```{}```".format(msg),
                            "short": False,
                        }
                    )

        rollbacks = payload.get("rollbacks")
        if rollbacks:
            for rollback in rollbacks:
                if rollback.get("status") == "failed":
                    msg = rollback.get("output")
                    if not msg and rollback.get("exception"):
                        msg = rollback.get("exception")[-1].strip()
                    rollbacks_fields.append(
                        {
                            "title": rollback.get("activity").get("name"),
                            "value": "```{}```".format(msg),
                            "short": False,
                        }
                    )

    # let's not clutter the view
    if steady_states_fields:
        main_attachement.pop("ts", None)
        main_attachement.pop("footer", None)
        main_attachement.pop("footer_icon", None)
        attachments.append(steady_states_attachment)

    if activities_fields:
        steady_states_attachment.pop("ts", None)
        steady_states_attachment.pop("footer", None)
        steady_states_attachment.pop("footer_icon", None)
        attachments.append(activities_attachment)

    if rollbacks_fields:
        steady_states_attachment.pop("ts", None)
        steady_states_attachment.pop("footer", None)
        steady_states_attachment.pop("footer_icon", None)
        activities_attachment.pop("ts", None)
        activities_attachment.pop("footer", None)
        activities_attachment.pop("footer_icon", None)
        attachments.append(rollbacks_attachment)

    try:
        result = sc.chat_postMessage(
            channel=channel,
            text="New Chaos Experiment Event",
            attachments=attachments,
        )
    except SlackApiError as x:
        logger.debug(
            "Slack client call failed: {}".format(str(x)), exc_info=True
        )
        return

    logger.debug(
        "Slack client return call: {}".format(
            json.dumps(result["data"], indent=2)
        )
    )
