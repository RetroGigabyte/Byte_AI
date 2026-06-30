#!/usr/bin/env python3
"""
Example integration of NTP time functions into chatbot
Shows how to add time/date capabilities to the knowledge bot
"""

import ntp_time
from datetime import datetime, timedelta
import pytz


class ChatbotTimeExtension:
    """Extends chatbot with NTP-based time functionality"""

    def __init__(self):
        """Initialize NTP manager on chatbot startup"""
        success, message = ntp_time.init_ntp()
        self.ntp_ready = success
        print(f"[Chatbot Time Module] {message}")

    def handle_time_query(self, query: str) -> str:
        """Process time-related queries from user

        Examples:
            "what time is it?"
            "what's the current time in Tokyo?"
            "how much time until New Year?"
        """
        query_lower = query.lower().strip()

        # Current time queries
        if any(word in query_lower for word in ['time', 'what time', 'current time', 'now']):
            if 'tokyo' in query_lower or 'jst' in query_lower:
                return f"Current time in Tokyo: {ntp_time.get_readable_time('Asia/Tokyo')}"
            elif 'london' in query_lower:
                return f"Current time in London: {ntp_time.get_readable_time('Europe/London')}"
            elif 'new york' in query_lower or 'eastern' in query_lower:
                return f"Current time in New York: {ntp_time.get_readable_time('US/Eastern')}"
            elif 'los angeles' in query_lower or 'pacific' in query_lower:
                return f"Current time in Los Angeles: {ntp_time.get_readable_time('US/Pacific')}"
            else:
                return f"Current time (UTC): {ntp_time.get_readable_time()}"

        # Date queries
        elif any(word in query_lower for word in ['date', 'today', 'what date']):
            current = ntp_time.get_ntp_time()
            return f"Today is {current.strftime('%A, %B %d, %Y')}"

        # Tomorrow/next day queries
        elif any(word in query_lower for word in ['tomorrow', 'next day']):
            tomorrow = ntp_time.add_time(days=1)
            return f"Tomorrow will be {tomorrow.strftime('%A, %B %d, %Y')}"

        # Yesterday queries
        elif 'yesterday' in query_lower:
            yesterday = ntp_time.subtract_time(days=1)
            return f"Yesterday was {yesterday.strftime('%A, %B %d, %Y')}"

        # Time until queries
        elif any(word in query_lower for word in ['until', 'countdown', 'how long', 'remaining']):
            if 'christmas' in query_lower:
                christmas = datetime(2026, 12, 25, tzinfo=pytz.UTC)
                delta = ntp_time.time_until(christmas)
                return f"Time until Christmas 2026: {delta['days']} days, {delta['hours']} hours"
            elif 'new year' in query_lower:
                new_year = datetime(2027, 1, 1, tzinfo=pytz.UTC)
                delta = ntp_time.time_until(new_year)
                return f"Time until New Year 2027: {delta['days']} days, {delta['hours']} hours"
            else:
                return "Please specify what event you're counting down to"

        # Timestamp queries
        elif 'timestamp' in query_lower or 'unix' in query_lower:
            ts = ntp_time.get_timestamp()
            return f"Current Unix timestamp: {int(ts)}"

        # ISO format
        elif 'iso' in query_lower or 'iso8601' in query_lower or 'iso 8601' in query_lower:
            return f"ISO 8601 format: {ntp_time.get_iso_time()}"

        # NTP status
        elif 'sync' in query_lower or 'ntp' in query_lower or 'synchronized' in query_lower:
            status = ntp_time.get_status()
            synced = "✓ Yes" if status['synced'] else "✗ No"
            return (f"NTP Status:\n"
                    f"  Synchronized: {synced}\n"
                    f"  Last sync: {status['last_sync']}\n"
                    f"  Current UTC: {status['current_time_utc']}")

        else:
            return "Try asking: 'What time is it?', 'What's today?', or 'Time until New Year?'"

    def get_training_data(self) -> list:
        """Return time-related training data for knowledge base"""
        return [
            "time: The current time can be retrieved in multiple timezones",
            "time: NTP synchronization ensures accurate timekeeping across the network",
            "time: Unix timestamp is a single number representing seconds since epoch",
            "date: Current date can be formatted in multiple styles",
            "date: Days of the week are Monday through Sunday",
            "date: Months have 28-31 days depending on the month",
            "timezone: UTC is Coordinated Universal Time used worldwide",
            "timezone: EST/EDT is Eastern Standard/Daylight Time in North America",
            "timezone: JST is Japan Standard Time 9 hours ahead of UTC",
            "timezone: BST is British Summer Time 1 hour ahead of UTC",
            "timestamp: Unix epoch is January 1, 1970 at 00:00:00 UTC",
            "countdown: Countdowns show remaining time until an event",
            "ntp: NTP pools synchronize computer clocks with atomic time",
        ]


# ============================================
# DEMO: Integration Example
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("CHATBOT TIME EXTENSION - DEMO")
    print("=" * 60)

    # Initialize extension
    extension = ChatbotTimeExtension()

    # Example queries
    queries = [
        "what time is it?",
        "current time in Tokyo",
        "what date is it today?",
        "time until New Year",
        "yesterday",
        "unix timestamp",
        "is NTP synced?",
        "what time in London?",
    ]

    print("\n💬 Example Conversations:\n")
    for query in queries:
        response = extension.handle_time_query(query)
        print(f"  Q: {query}")
        print(f"  A: {response}")
        print()

    print("\n📚 Training Data Sample:")
    for line in extension.get_training_data()[:5]:
        print(f"  {line}")
