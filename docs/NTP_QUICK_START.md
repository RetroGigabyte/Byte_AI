# NTP Time Functions - Quick Start

## Installation

```bash
pip install -r requirements.txt  # Includes ntplib and pytz
```

## Basic Usage

### Initialize Once at Startup

```python
import ntp_time

# Initialize NTP synchronization
success, message = ntp_time.init_ntp()
print(message)
```

### Get Current Time

```python
# Simple functions
current_time = ntp_time.get_current_time()  # "2026-06-30 02:42:37"
readable = ntp_time.get_readable_time()     # "Tuesday, June 30, 2026 at 02:42 AM UTC"
iso_time = ntp_time.get_iso_time()          # "2026-06-30T02:42:37.527766+00:00"

# Different timezones
ny_time = ntp_time.get_readable_time('US/Eastern')
tokyo_time = ntp_time.get_readable_time('Asia/Tokyo')
london_time = ntp_time.get_readable_time('Europe/London')
```

### Time Math

```python
# Add/subtract time
tomorrow = ntp_time.add_time(days=1)
next_week = ntp_time.add_time(days=7)
earlier = ntp_time.subtract_time(hours=2)

# Time until/since
christmas = datetime(2026, 12, 25, tzinfo=pytz.UTC)
countdown = ntp_time.time_until(christmas)
print(f"Days until Christmas: {countdown['days']}")

start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
elapsed = ntp_time.time_since(start)
print(f"Days since New Year: {elapsed['days']}")
```

## Integration with Chatbot

### Using the Chatbot Extension

```python
from ntp_integration_example import ChatbotTimeExtension

# Initialize
extension = ChatbotTimeExtension()

# Handle time queries
queries = [
    "what time is it?",
    "current time in Tokyo",
    "time until New Year",
]

for query in queries:
    response = extension.handle_time_query(query)
    print(f"Q: {query}")
    print(f"A: {response}\n")
```

## Common Patterns

### Get User's Local Time

```python
def get_user_time(user_timezone):
    """Get current time in user's timezone"""
    readable = ntp_time.get_readable_time(user_timezone)
    timestamp = ntp_time.get_timestamp()
    return {"readable": readable, "timestamp": timestamp}

# Usage
user_time = get_user_time('US/Eastern')
print(user_time['readable'])  # "Monday, June 29, 2026 at 10:42 PM EDT"
```

### Schedule Countdown

```python
def countdown_to_event(event_name, event_date):
    """Show countdown to an event"""
    delta = ntp_time.time_until(event_date)
    
    if delta['negative']:
        return f"{event_name} has already passed"
    
    d, h, m, s = delta['days'], delta['hours'], delta['minutes'], delta['seconds']
    return f"{event_name} in {d}d {h}h {m}m {s}s"

# Usage
christmas = datetime(2026, 12, 25, tzinfo=pytz.UTC)
print(countdown_to_event("Christmas", christmas))
# Output: "Christmas in 179d 21h 45m 23s"
```

### Session Duration Tracking

```python
class ChatSession:
    def __init__(self):
        self.start_time = ntp_time.get_ntp_time()
    
    def get_duration(self):
        elapsed = ntp_time.time_since(self.start_time)
        return f"{elapsed['minutes']}m {elapsed['seconds']}s"

# Usage
session = ChatSession()
# ... user interacts ...
print(f"Session duration: {session.get_duration()}")
```

### Handle Timezone-Aware Events

```python
def format_event_time(utc_time, user_timezone):
    """Convert UTC event time to user's timezone"""
    # utc_time is datetime object in UTC
    local_dt = utc_time.astimezone(pytz.timezone(user_timezone))
    return local_dt.strftime('%A, %B %d at %I:%M %p %Z')

# Usage
event_utc = datetime(2026, 7, 4, 18, 0, 0, tzinfo=pytz.UTC)
user_tz = 'US/Eastern'
print(format_event_time(event_utc, user_tz))
# Output: "Saturday, July 04 at 02:00 PM EDT"
```

## Troubleshooting

### NTP Not Syncing

```python
success, message = ntp_time.init_ntp()
if not success:
    print(f"Warning: {message}")
    print("Using system time instead")
    # Code continues to work, just uses system time
```

### Wrong Timezone

```python
# Wrong (abbreviated)
ntp_time.get_readable_time('EST')  # May not work

# Correct (full timezone name)
ntp_time.get_readable_time('US/Eastern')  # Always works
```

### Custom Time Format

```python
# Use strftime format codes
ntp_time.get_current_time('%d/%m/%Y')              # 30/06/2026
ntp_time.get_current_time('%I:%M %p')              # 02:42 AM
ntp_time.get_current_time('%A, %B %d, %Y')        # Tuesday, June 30, 2026
ntp_time.get_current_time('%Y-W%V-%w')             # 2026-W27-2 (ISO week)
```

## Available Timezones (Samples)

```python
# North America
'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific', 'Canada/Eastern'

# Europe
'Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Europe/Moscow'

# Asia
'Asia/Tokyo', 'Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Bangkok', 'Asia/Dubai'

# Australia
'Australia/Sydney', 'Australia/Melbourne', 'Australia/Perth'

# Other
'UTC', 'GMT', 'Africa/Cairo', 'America/Sao_Paulo'
```

[See full timezone list](NTP_TIME_GUIDE.md#supported-timezones)

## Files

- **ntp_time.py** - Core NTP time module
- **ntp_integration_example.py** - Chatbot integration example
- **NTP_TIME_GUIDE.md** - Comprehensive documentation
- **NTP_QUICK_START.md** - This file
- **training/time_and_date.txt** - Training data for time/date queries

## Running Tests

```bash
# Test NTP module
python ntp_time.py

# Test chatbot integration
python ntp_integration_example.py
```

## Next Steps

1. ✅ Add `ntp_time.py` to your project
2. ✅ Update `requirements.txt`
3. ✅ Initialize in chatbot startup: `ntp_time.init_ntp()`
4. ✅ Use `ChatbotTimeExtension` for time queries
5. ✅ Add `time_and_date.txt` to training data

---

Built with ❤️ into Byte Knowledge Bot 📡⏰
