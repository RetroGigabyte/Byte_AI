# NTP-Based Date and Time Functions Guide

## Overview

The chatbot now includes comprehensive NTP (Network Time Protocol) based date and time functionality. This ensures accurate, synchronized timekeeping across multiple timezones with atomic clock precision.

## Installation

Add to your chatbot initialization:

```python
import ntp_time

# Initialize NTP synchronization
success, message = ntp_time.init_ntp()
print(message)  # ✓ Synced with pool.ntp.org at 2026-06-30 02:42:37 UTC
```

## Core Functions

### Getting Current Time

#### `get_ntp_time(tz: Optional[str] = None) -> datetime.datetime`
Get current time as Python datetime object.

```python
# UTC time
utc_time = ntp_time.get_ntp_time()
print(utc_time)  # 2026-06-30 02:42:37.527766+00:00

# Specific timezone
tokyo_time = ntp_time.get_ntp_time('Asia/Tokyo')
print(tokyo_time)  # 2026-06-30 11:42:37.527766+09:00
```

#### `get_current_time(fmt: str = '%Y-%m-%d %H:%M:%S', tz: Optional[str] = None) -> str`
Get formatted current time.

```python
# Default format
ntp_time.get_current_time()
# Output: "2026-06-30 02:42:37"

# Custom format
ntp_time.get_current_time('%A, %B %d, %Y at %I:%M %p')
# Output: "Tuesday, June 30, 2026 at 02:42 AM"

# With timezone
ntp_time.get_current_time(tz='US/Eastern')
# Output: "2026-06-29 22:42:37"
```

#### `get_readable_time(tz: Optional[str] = None) -> str`
Get human-readable time with full formatting.

```python
ntp_time.get_readable_time()
# Output: "Tuesday, June 30, 2026 at 02:42 AM UTC"

ntp_time.get_readable_time('US/Pacific')
# Output: "Monday, June 29, 2026 at 07:42 PM PDT"
```

#### `get_iso_time(tz: Optional[str] = None) -> str`
Get ISO 8601 formatted time (useful for APIs and databases).

```python
ntp_time.get_iso_time()
# Output: "2026-06-30T02:42:37.527766+00:00"
```

#### `get_timestamp() -> float`
Get Unix timestamp (seconds since epoch).

```python
ntp_time.get_timestamp()
# Output: 1782787357.527766
```

## Time Calculations

### Adding Time

#### `add_time(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime.datetime`

```python
# Tomorrow
tomorrow = ntp_time.add_time(days=1)

# Next week
next_week = ntp_time.add_time(days=7)

# In 2 hours 30 minutes
later = ntp_time.add_time(hours=2, minutes=30)

# Complex: 3 days, 4 hours, 15 minutes from now
future = ntp_time.add_time(days=3, hours=4, minutes=15)
```

### Subtracting Time

#### `subtract_time(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime.datetime`

```python
# Yesterday
yesterday = ntp_time.subtract_time(days=1)

# Last week
last_week = ntp_time.subtract_time(days=7)

# 3 hours ago
earlier = ntp_time.subtract_time(hours=3)
```

### Time Differences

#### `time_until(target: datetime.datetime) -> Dict[str, int]`
Calculate time remaining until a target datetime.

```python
from datetime import datetime
import pytz

# Time until Christmas
christmas = datetime(2026, 12, 25, tzinfo=pytz.UTC)
delta = ntp_time.time_until(christmas)
print(delta)
# Output: {'days': 179, 'hours': 21, 'minutes': 45, 'seconds': 23, 'negative': False, 'total_seconds': 15546323.45}

# Readable format
print(f"Christmas in {delta['days']} days and {delta['hours']} hours")
# Output: "Christmas in 179 days and 21 hours"
```

#### `time_since(start: datetime.datetime) -> Dict[str, int]`
Calculate time elapsed since a start datetime.

```python
from datetime import datetime
import pytz

# Time since this year started
year_start = datetime(2026, 1, 1, tzinfo=pytz.UTC)
elapsed = ntp_time.time_since(year_start)
print(elapsed)
# Output: {'days': 180, 'hours': 2, 'minutes': 42, 'seconds': 37, 'total_seconds': 15552157.45}

# Readable format
print(f"Started {elapsed['days']} days ago")
```

## Supported Timezones

### Common Timezones

```python
# US/Canada
ntp_time.get_readable_time('US/Eastern')      # EST/EDT
ntp_time.get_readable_time('US/Central')      # CST/CDT
ntp_time.get_readable_time('US/Mountain')     # MST/MDT
ntp_time.get_readable_time('US/Pacific')      # PST/PDT
ntp_time.get_readable_time('US/Alaska')       # AKST/AKDT
ntp_time.get_readable_time('US/Hawaii')       # HST

# Europe
ntp_time.get_readable_time('Europe/London')   # GMT/BST
ntp_time.get_readable_time('Europe/Paris')    # CET/CEST
ntp_time.get_readable_time('Europe/Berlin')   # CET/CEST
ntp_time.get_readable_time('Europe/Madrid')   # CET/CEST
ntp_time.get_readable_time('Europe/Rome')     # CET/CEST
ntp_time.get_readable_time('Europe/Moscow')   # MSK

# Asia/Pacific
ntp_time.get_readable_time('Asia/Tokyo')      # JST
ntp_time.get_readable_time('Asia/Shanghai')   # CST
ntp_time.get_readable_time('Asia/Hong_Kong')  # HKT
ntp_time.get_readable_time('Asia/Bangkok')    # ICT
ntp_time.get_readable_time('Asia/Singapore')  # SGT
ntp_time.get_readable_time('Asia/Dubai')      # GST
ntp_time.get_readable_time('Asia/Kolkata')    # IST
ntp_time.get_readable_time('Australia/Sydney') # AEDT/AEST
ntp_time.get_readable_time('Australia/Perth')  # AWDT/AWST

# Africa
ntp_time.get_readable_time('Africa/Cairo')    # EET
ntp_time.get_readable_time('Africa/Johannesburg') # SAST

# South America
ntp_time.get_readable_time('America/Sao_Paulo')  # BRT/BRST
ntp_time.get_readable_time('America/Buenos_Aires') # ART

# UTC
ntp_time.get_readable_time()                  # UTC
ntp_time.get_readable_time('UTC')             # Explicit UTC
```

## Status and Diagnostics

### `get_status() -> Dict[str, any]`
Get NTP synchronization status.

```python
status = ntp_time.get_status()
print(status)

# Output:
# {
#   'synced': True,
#   'last_sync': '2026-06-30T02:42:37.170541+00:00',
#   'offset_seconds': 0.344,
#   'current_time_utc': '2026-06-30T02:43:00.352778+00:00'
# }

# Check if synchronized
if status['synced']:
    print("✓ Clock is synchronized with atomic time")
else:
    print("✗ Using system time (NTP not available)")

# Show offset
print(f"Clock offset: {status['offset_seconds']} seconds")
```

## Integration with Chatbot

### Example: Time Query Handler

```python
from ntp_integration_example import ChatbotTimeExtension

# Initialize extension in chatbot
time_extension = ChatbotTimeExtension()

# Handle user queries
user_query = "what time is it in Tokyo?"
response = time_extension.handle_time_query(user_query)
print(response)
# Output: "Current time in Tokyo: Tuesday, June 30, 2026 at 11:43 AM JST"
```

### Supported Queries

The chatbot can now answer:

- "What time is it?"
- "What's the current time in [city]?"
- "What's today's date?"
- "What was yesterday?"
- "What's tomorrow?"
- "Time until [event]?" (Christmas, New Year, etc.)
- "Unix timestamp?"
- "Is NTP synchronized?"
- "Time in London/Tokyo/New York/LA?"

## Python Format Strings

Customize time formatting with strftime format codes:

```python
ntp_time.get_current_time('%Y-%m-%d')           # 2026-06-30
ntp_time.get_current_time('%d/%m/%Y')           # 30/06/2026
ntp_time.get_current_time('%H:%M:%S')           # 02:42:37
ntp_time.get_current_time('%I:%M %p')           # 02:42 AM
ntp_time.get_current_time('%A')                 # Tuesday
ntp_time.get_current_time('%B')                 # June
ntp_time.get_current_time('%A, %B %d, %Y')     # Tuesday, June 30, 2026
ntp_time.get_current_time('%Y-W%V-%w')          # 2026-W27-2 (ISO week)
```

### Common Format Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2026 |
| `%y` | 2-digit year | 26 |
| `%m` | Month (01-12) | 06 |
| `%d` | Day (01-31) | 30 |
| `%H` | Hour (00-23) | 02 |
| `%I` | Hour (01-12) | 02 |
| `%M` | Minute (00-59) | 42 |
| `%S` | Second (00-59) | 37 |
| `%p` | AM/PM | AM |
| `%A` | Weekday name | Tuesday |
| `%a` | Abbreviated weekday | Tue |
| `%B` | Month name | June |
| `%b` | Abbreviated month | Jun |

## NTP Servers

The module uses multiple NTP servers for reliability:

1. `pool.ntp.org` - NTP pool
2. `time.nist.gov` - NIST time server
3. `time.google.com` - Google public NTP
4. `time.cloudflare.com` - Cloudflare time server

It automatically tries each server until synchronization succeeds.

## Error Handling

The module gracefully falls back to system time if NTP is unavailable:

```python
success, message = ntp_time.init_ntp()

if success:
    print("✓ Using NTP-synchronized time")
else:
    print("⚠️  Using system time instead")
    print(message)
    # ✗ Could not sync with any NTP server

# Still works either way
current_time = ntp_time.get_readable_time()
```

## Performance Notes

- **First call**: May take 5 seconds while syncing with NTP server
- **Subsequent calls**: Instantaneous (uses cached offset)
- **Accuracy**: Within 1-100ms of atomic time (depending on network)
- **Memory**: ~500 bytes per manager instance
- **CPU**: Negligible when synced

## Best Practices

1. **Initialize once** at chatbot startup:
   ```python
   import ntp_time
   ntp_time.init_ntp()  # Call once on startup
   ```

2. **Use appropriate timezones** for users:
   ```python
   user_timezone = get_user_timezone()  # From user profile
   current = ntp_time.get_readable_time(user_timezone)
   ```

3. **Cache results** for high-frequency queries:
   ```python
   @cache(ttl=60)  # Cache for 60 seconds
   def get_current_time():
       return ntp_time.get_readable_time()
   ```

4. **Handle timezone errors**:
   ```python
   try:
       time_str = ntp_time.get_current_time(tz=user_tz)
   except:
       time_str = ntp_time.get_current_time()  # Fall back to UTC
   ```

## Examples

### Example 1: Current Time in Multiple Cities

```python
cities = {
    'New York': 'US/Eastern',
    'London': 'Europe/London',
    'Tokyo': 'Asia/Tokyo',
    'Sydney': 'Australia/Sydney',
}

for city, tz in cities.items():
    time_str = ntp_time.get_readable_time(tz)
    print(f"{city}: {time_str}")
```

### Example 2: Schedule Event Countdown

```python
from datetime import datetime
import pytz

event = datetime(2026, 12, 25, 0, 0, 0, tzinfo=pytz.UTC)  # Christmas
countdown = ntp_time.time_until(event)

print(f"Christmas countdown:")
print(f"  {countdown['days']} days")
print(f"  {countdown['hours']} hours")
print(f"  {countdown['minutes']} minutes")
print(f"  {countdown['seconds']} seconds")
```

### Example 3: Session Duration Tracking

```python
session_start = ntp_time.get_ntp_time()

# ... user interacts with chatbot ...

elapsed = ntp_time.time_since(session_start)
print(f"Session duration: {elapsed['minutes']} minutes, {elapsed['seconds']} seconds")
```

### Example 4: Business Hours Check

```python
current = ntp_time.get_ntp_time('US/Eastern')
hour = current.hour

if 9 <= hour < 17:
    print("Business hours (Eastern time)")
else:
    print("After hours")
```

## Troubleshooting

### NTP Sync Fails
- Check internet connection
- Firewall may be blocking NTP port 123
- Try manual sync: `ntp_time.init_ntp()`

### Wrong Timezone
- Verify timezone string is in `pytz.all_timezones`
- Common mistake: `'PST'` should be `'US/Pacific'`
- Use full timezone names like `'America/Los_Angeles'`

### Time is Still Wrong
- Check system clock (your computer's time)
- System time affects NTP offset calculation
- Adjust system time and re-sync

## Links

- [NTP Servers](https://www.pool.ntp.org/)
- [pytz Timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- [Unix Timestamp](https://en.wikipedia.org/wiki/Unix_time)
- [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)

---

Built into Byte Knowledge Bot with NTP support 📡⏰
