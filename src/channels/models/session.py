from __future__ import annotations

from datetime import datetime
from random import randint
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from channels.models.events import ChannelType


class SessionState(BaseModel):
    session_id: str = Field(default_factory=lambda: uuid4().hex[:12])
    customer_phone: str
    customer_name: str = "Customer"
    language: str = "en"
    current_channel: ChannelType
    previous_channel: ChannelType | None = None
    original_channel: ChannelType | None = None
    current_intent: str | None = None
    current_agent: str | None = None
    pending_action: dict[str, Any] | None = None
    conversation_summary: str = ""
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    channel_history: list[str] = Field(default_factory=list)
    resolved: bool = False
    resolution_channel: ChannelType | None = None
    resume_code: str = Field(default_factory=lambda: f"{randint(100000, 999999)}")
    fallback_initiated: bool = False
    fallback_hint: str | None = None
    user_reengaged: bool = False
