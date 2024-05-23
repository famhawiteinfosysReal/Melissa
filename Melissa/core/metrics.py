from prometheus_client import Counter, Gauge

EventCount = Counter(
    "Melissa_event_count",
    "Number of events being processed",
    labelnames=["type"],
)
SpamPredictionStat = Counter(
    "Melissa_spam_prediction_stat",
    "Number of spam prediction event",
    labelnames=["status"],
)
MessageStat = Counter(
    "Melissa_message_stat",
    "Number of message",
    labelnames=["type"],
)
CommandCount = Counter("Melissa_command_stats", "Number of coomand", labelnames=["name"])
UnhandledError = Counter("Melissa_unhandled_error", "Number of unhandled error")

EventLatencySecond = Gauge(
    "Melissa_event_latency",
    "Latency of event processed",
    labelnames=["type"],
    unit="second",
)
CommandLatencySecond = Gauge(
    "Melissa_command_latency",
    "Latency of command processed",
    labelnames=["name"],
    unit="second",
)
