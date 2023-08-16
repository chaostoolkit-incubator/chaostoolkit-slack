# -*- coding: utf-8 -*-
import os
from typing import List

from chaoslib.discovery.discover import (
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import DiscoveredActivities, Discovery, Secrets
from logzero import logger
from slack_sdk import WebClient

__all__ = ["get_client", "get_channel_id", "discover"]
__version__ = "0.7.0"


def get_client(secrets: Secrets) -> WebClient:
    secrets = secrets or {}
    slack_token = secrets.get("slack", {}).get(
        "token", os.getenv("SLACK_BOT_TOKEN")
    )
    client = WebClient(token=slack_token)
    return client


def get_channel_id(client: WebClient, channel: str) -> str:
    channel = channel.lstrip("#")

    result = client.conversations_list()

    for c in result["channels"]:
        if c["name"] == channel:
            return c["id"]

    raise ActivityFailed(f"slack channel '{channel}' could not be found")


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Slack capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-slack")

    discovery = initialize_discovery_result(
        "chaostoolkit-slack", __version__, "slack"
    )
    discovery["activities"].extend(load_exported_activities())
    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_probes("chaosslack.probes"))
    return activities
