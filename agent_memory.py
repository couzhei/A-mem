"""
This module the version 0 of the Agent's memory schema
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

MEMORY_STORE_DIR = "."  # TODO: To be determined


class AgentMemory:
    """
    Agent memory class

    version: 0
    """

    def __init__(self, agent_id: str):
        self.agent_id: str = agent_id
        self.system_prompt: str = ""  # Editable per agent
        self.preferences: Dict[str, Any] = {}  # Personality, interests, etc.

        # Social graph
        self.followed_accounts: List[str] = []  # screen_names

        # Activity logs
        self.tweets: List[Dict] = []  # Each: {id, content, timestamp}
        self.retweets: List[Dict] = []  # Each: {id, content, timestamp}
        self.replies: List[Dict] = []  # Each: {id, content, parent_id, timestamp}
        self.likes: List[Dict] = []  # Each: {id, content, timestamp}
        self.mentions: List[Dict] = []  # Each: {id, content, timestamp}no

        # Conversations
        self.conversations: Dict[
            str, List[Dict]
        ] = {}  # conversation_id -> list of {sender:<screen_name>, text:<content>, timestamp:<datetime>}

        # Tool usage history (optional)
        self.tool_calls: List[Dict] = []  # Each: {tool_name, input, output, timestamp}

    # Example methods for adding data
    def add_tweet(self, tweet_id: str, content: str):
        """
        Add a tweet to the memory
        """
        self.tweets.append(
            {
                "id": tweet_id,
                "content": content,
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            }
        )

    def add_follow(self, user_id: str):
        """
        Add a followed account to the memory
        """
        if user_id not in self.followed_accounts:
            self.followed_accounts.append(user_id)

    def add_conversation_message(self, conversation_id: str, sender: str, text: str):
        """
        Add a conversation message to the memory
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.conversations[conversation_id].append(
            {
                "sender": sender,
                "text": text,
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            }
        )

    # TODO: similar methods for retweets, replies, likes, mentions, tool_calls

    def save(self):
        """Persist memory to disk (as JSON)."""
        os.makedirs(MEMORY_STORE_DIR, exist_ok=True)
        path = os.path.join(MEMORY_STORE_DIR, f"{self.agent_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, agent_id):
        """Load memory from disk if exists, else return None."""
        path = os.path.join(MEMORY_STORE_DIR, f"{agent_id}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            mem = cls(agent_id)
            mem.__dict__.update(data)
            return mem
        return None


def get_or_create_agent_memory(
    agent_id: str,
    system_prompt: str = None,
    # preferences:
):
    mem = AgentMemory.load(agent_id)
    if mem is not None:
        return mem

    mem = AgentMemory()
