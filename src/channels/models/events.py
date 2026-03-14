from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

ChannelType = Literal["voice", "whatsapp", "ussd", "sms"]


class ChannelEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: uuid4().hex)
    session_id: str
    channel: ChannelType
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    customer_phone_hash: str
    region: str | None = None
    language: str | None = None


class QualityMetrics(BaseModel):
    packet_loss: float
    jitter_ms: float
    latency_ms: float


class AgentResponse(BaseModel):
    text: str
    short_text: str = Field(max_length=160)
    options: list[str] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)
    requires_input: bool = False
    language: str = "en"


class ChaosTestReport(BaseModel):
    total_sessions: int
    failures_injected: int
    sessions_resolved: int
    survival_rate: float
    avg_recovery_time_seconds: float
    fallback_paths: dict[str, int]
    sessions_with_fallback: int
    sessions_with_reengagement: int
    reengagement_rate: float
