from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from chaoslib.types import Secrets
from logzero import logger
from slack_sdk.errors import SlackApiError

from chaosslack import get_channel_id, get_client

__all__ = ["get_channel_history"]


def get_channel_history(
    channel: str,
    limit: int = 100,
    past: int = 15,
    include_metadata: bool = False,
    secrets: Secrets = None,
) -> List[Dict[str, Any]]:
    """
    Fetches the history of a channel up to a certain limit of messages or
    for the past minutes.

    By default no more than 100 messages in the last 15 minutes.
    """
    messages = []

    oldest = datetime.now().astimezone(tz=timezone.utc) - timedelta(
        minutes=past
    )
    ts = oldest.timestamp()

    try:
        client = get_client(secrets)
        channel_id = get_channel_id(client, channel)
        logger.debug(
            f"Fetching the last {limit} messages for the past {past}mn "
            f"[{oldest}] from channel {channel} [{channel_id}]"
        )
        result = client.conversations_history(
            channel=channel_id,
            inclusive=True,
            limit=limit,
            include_metadata=include_metadata,
            oldest=ts,
        )
        messages.extend(result["messages"])

        while (result["ok"] is True) and (result["has_more"] is True):
            cursor = result["response_metadata"]["next_cursor"]
            result = client.conversations_history(
                channel=channel_id,
                cursor=cursor,
                inclusive=True,
                limit=limit,
                include_metadata=include_metadata,
                oldest=ts,
            )

            messages.extend(result["messages"])

    except SlackApiError as e:
        logger.error(f"Failed to retrieve Slack channel history: {e}")

    return messages
