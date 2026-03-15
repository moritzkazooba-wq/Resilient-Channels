from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from channels.models.events import ChannelType


class LiveMetrics(BaseModel):
    active_sessions: int
    sessions_by_channel: dict[str, int]
    resolution_rate_1h: float
    avg_v2v_latency_ms: float
    escalation_rate_1h: float
    cost_per_interaction_usd: dict[str, float]
    fallback_success_rate_1h: float


class ChannelHealth(BaseModel):
    channel: ChannelType
    status: Literal["healthy", "degraded", "down"]
    avg_latency_ms: float
    error_rate: float
    active_sessions: int
    fallback_count_1h: int
