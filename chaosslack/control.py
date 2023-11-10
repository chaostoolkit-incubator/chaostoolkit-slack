import json
import os
import platform
from typing import Any, Dict, List, Optional

import yaml
from chaoslib.exceptions import InvalidActivity
from chaoslib.types import (
    Activity,
    Configuration,
    Experiment,
    Hypothesis,
    Journal,
    Run,
    Secrets,
)
from logzero import logger
from slack_sdk import WebClient

__all__ = [
    "after_loading_experiment_control",
    "before_experiment_control",
    "after_experiment_control",
    "before_hypothesis_control",
    "after_hypothesis_control",
    "before_method_control",
    "before_rollback_control",
    "after_rollback_control",
    "before_activity_control",
    "after_activity_control",
]


def after_loading_experiment_control(
    context: str,
    state: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        "Experiment loaded",
        state,
        get_state(),
        channel,
        configuration=configuration,
        secrets=secrets,
        in_thread=True,
        thread_data=None,
    )


def before_experiment_control(
    context: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    extra = configuration.get("slack_extra")
    send(
        "Experiment is starting",
        context,
        get_state(),
        channel,
        in_thread=False,
        extra=extra,
        configuration=configuration,
        secrets=secrets,
    )

    if current_msg:
        c = context.setdefault("configuration", {})
        c["slack_thread"] = {
            "channel": current_msg.get("channel"),
            "ts": current_msg.get("ts"),
        }


def after_experiment_control(
    context: Experiment,
    state: Journal,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        "Experiment is finished",
        context,
        get_state(state),
        channel,
        in_thread=False,
        configuration=configuration,
        secrets=secrets,
    )

    phrase = get_state(state).lower()
    send(
        f"Experiment is finished with status `{phrase}`",
        context,
        get_state(state),
        channel,
        in_thread=True,
        thread_data=None,
        configuration=configuration,
        secrets=secrets,
    )


def before_hypothesis_control(
    context: Hypothesis,
    experiment: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        "Steady state hypothesis is being evaluated",
        experiment,
        get_state(),
        channel,
        in_thread=True,
        configuration=configuration,
        secrets=secrets,
    )


def after_hypothesis_control(
    context: Hypothesis,
    state: Dict[str, Any],
    experiment: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    phrase = "and did not deviate"
    if state["steady_state_met"] is False:
        phrase = "and *deviated*"
    send(
        f"Steady state hypothesis finished {phrase}",
        experiment,
        get_state(),
        channel,
        in_thread=True,
        thread_data=state,
        configuration=configuration,
        secrets=secrets,
    )


def before_method_control(
    context: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        "Method is starting",
        context,
        get_state(),
        channel,
        in_thread=True,
        configuration=configuration,
        secrets=secrets,
    )


def after_method_control(
    context: Experiment,
    state: List[Run],
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        "Method is finished",
        context,
        get_state(),
        channel,
        in_thread=True,
        configuration=configuration,
        secrets=secrets,
    )


def before_rollback_control(
    context: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        "Rollback is starting",
        context,
        get_state(),
        channel,
        in_thread=True,
        configuration=configuration,
        secrets=secrets,
    )


def after_rollback_control(
    context: Experiment,
    state: List[Run],
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        "Rollback is finished",
        context,
        get_state(),
        channel,
        in_thread=True,
        configuration=configuration,
        secrets=secrets,
    )


def before_activity_control(
    context: Activity,
    experiment: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        f"Activity `{context['name']}` is starting",
        experiment,
        get_state(),
        channel,
        in_thread=True,
        configuration=configuration,
        secrets=secrets,
    )


def after_activity_control(
    context: Activity,
    state: Run,
    experiment: Experiment,
    configuration: Configuration,
    secrets: Secrets,
    channel: Optional[str] = None,
) -> None:
    send(
        f"Activity `{context['name']}` "
        f"finished with status `{state['status']}`",
        experiment,
        get_state(),
        channel,
        in_thread=True,
        thread_data=state,
        configuration=configuration,
        secrets=secrets,
    )


###############################################################################
# Internals
###############################################################################
current_msg = None  # SlackResponse
client = None  # WebClient


def get_state(journal: Journal = None) -> str:
    if not journal:
        return "Running"

    if journal["status"] == "completed" and journal["deviated"] is False:
        return "Completed successfully"
    elif journal["status"] == "completed" and journal["deviated"] is True:
        return "Deviated"
    elif journal["status"] == "interrupted":
        return "Interrupted by operator or signal"
    elif journal["status"] == "failed":
        return "Failed to complete"


def get_client(secrets: Secrets) -> WebClient:
    secrets = secrets or {}
    slack_token = secrets.get("slack", {}).get(
        "token", os.getenv("SLACK_BOT_TOKEN")
    )
    client = WebClient(token=slack_token)
    return client


def send(
    message: str,
    experiment: Experiment,
    state: str,
    channel: Optional[str],
    in_thread: bool,
    thread_data: Any = None,
    thread_text: str = None,
    extra: Optional[List[str]] = None,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> None:
    global client, current_msg
    if not client:
        client = get_client(secrets)

    if not channel:
        channel = os.getenv("SLACK_CHANNEL")

    if not channel:
        raise InvalidActivity("missing slack channel name")

    if not current_msg:
        current_msg = r = client.chat_postMessage(
            channel=channel,
            fallback=message,
            text=message,
            extra=extra,
            attachments=attachments(
                state,
                message,
                experiment,
            ),
        )
    elif in_thread and thread_data:
        state_content = yaml.safe_dump(thread_data or {}, indent=2)
        r = client.files_upload_v2(
            channel=current_msg.get("channel"),
            thread_ts=current_msg.get("ts"),
            initial_comment=message,
            snippet_type="yaml",
            content=state_content,
            length=len(state_content),
            title="state.yaml",
        )
    elif in_thread:
        r = client.chat_postMessage(
            channel=channel,
            fallback=message,
            text=message,
            thread_ts=current_msg.get("ts"),
        )
    else:
        r = client.chat_update(
            channel=current_msg.get("channel"),
            ts=current_msg.get("ts"),
            text=message,
            attachments=attachments(state, message, experiment),
            reply_broadcast=False,
        )

    if r.get("ok") is False:
        logger.debug(f"Failed to send slack message or file: {json.dumps(r)}")


def attachments(
    state: str,
    fallback: str,
    experiment: Experiment,
    extra: Optional[List[str]] = None,
) -> Dict[str, Any]:
    if state == "Running":
        color = "#222831"
    elif state == "Completed successfully":
        color = "#06FF00"
    elif state == "Interrupted by operator or signal":
        color = "#CEAB93"
    elif state == "Failed to complete":
        color = "#FF8E00"
    elif state == "Deviated":
        color = "#FF1700"
    else:
        color = "#000000"

    payload = [
        {
            "color": color,
            "fallback": fallback,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{experiment['title']}*",
                    },
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Host:* {platform.node()}\n"
                            f"*State:* {state}",
                        }
                    ],
                },
            ],
        }
    ]

    if extra:
        for x in extra:
            payload[0]["blocks"].append(
                {"type": "section", "text": {"type": "mrkdwn", "text": x}}
            )

    return payload
