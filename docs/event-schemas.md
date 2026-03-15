# Kafka Event Schemas

## Topics

### 1. `channel.events`

All inbound and outbound channel interactions.

- **Event types**: `message.inbound`, `message.outbound`, `call.started`, `call.ended`, `ussd.input`, `sms.sent`
- **Partitioning**: By `customer_phone_hash` — ensures all events for a given customer land on the same partition for ordered processing.
- **Schema**: `ChannelEvent`

### 2. `channel.quality`

Real-time quality metrics per active session.

- **Event types**: `quality.report`
- **Partitioning**: By `session_id` — keeps all quality samples for a session together.
- **Schema**: `QualityMetrics` wrapped in a `ChannelEvent` payload.

### 3. `channel.fallback`

Channel switch / fallback events.

- **Event types**: `fallback.initiated`, `fallback.completed`, `fallback.failed`
- **Partitioning**: By `session_id` — maintains ordering of fallback attempts within a session.
- **Schema**: `ChannelEvent` with `payload` containing `from_channel`, `to_channel`, and `reason`.

### 4. `channel.sessions`

Session lifecycle events.

- **Event types**: `session.created`, `session.updated`, `session.resolved`, `session.expired`
- **Partitioning**: By `customer_phone_hash` — groups all session lifecycle events per customer.
- **Schema**: `ChannelEvent` with `payload` containing the serialised `SessionState`.
