#!/usr/bin/env python3
"""
NTP-based Date and Time Functions
Provides accurate time synchronization and manipulation using Network Time Protocol
"""

import ntplib
import time
import datetime
import pytz
from typing import Optional, Tuple, Dict


class NTPTimeManager:
    """Manages NTP synchronization and time operations"""

    # Public NTP servers
    NTP_SERVERS = [
        'pool.ntp.org',
        'time.nist.gov',
        'time.google.com',
        'time.cloudflare.com',
    ]

    def __init__(self, timeout: int = 5):
        """Initialize NTP time manager

        Args:
            timeout: NTP request timeout in seconds
        """
        self.client = ntplib.NTPClient()
        self.timeout = timeout
        self.last_sync: Optional[datetime.datetime] = None
        self.ntp_offset: float = 0.0
        self.is_synced: bool = False

    def sync_time(self, server: str = 'pool.ntp.org') -> Tuple[bool, str]:
        """Synchronize with NTP server

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            response = self.client.request(server, version=3, timeout=self.timeout)
            self.ntp_offset = response.tx_time - time.time()
            self.last_sync = datetime.datetime.now(pytz.UTC)
            self.is_synced = True
            return True, f"✓ Synced with {server} at {self.last_sync.strftime('%Y-%m-%d %H:%M:%S UTC')}"
        except Exception as e:
            return False, f"✗ NTP sync failed: {str(e)}"

    def auto_sync(self) -> Tuple[bool, str]:
        """Try multiple NTP servers until one succeeds

        Returns:
            Tuple of (success: bool, message: str)
        """
        for server in self.NTP_SERVERS:
            success, message = self.sync_time(server)
            if success:
                return True, message

        self.is_synced = False
        return False, "✗ Could not sync with any NTP server"

    def get_ntp_time(self, tz: Optional[str] = None) -> datetime.datetime:
        """Get current time from NTP offset

        Args:
            tz: Timezone string (e.g., 'US/Eastern', 'Europe/London')

        Returns:
            Current datetime object
        """
        if self.is_synced:
            ntp_time = datetime.datetime.fromtimestamp(
                time.time() + self.ntp_offset,
                tz=pytz.UTC
            )
        else:
            ntp_time = datetime.datetime.now(pytz.UTC)

        if tz:
            try:
                ntp_time = ntp_time.astimezone(pytz.timezone(tz))
            except:
                pass

        return ntp_time

    def get_timestamp(self) -> float:
        """Get current Unix timestamp (NTP-synchronized)"""
        if self.is_synced:
            return time.time() + self.ntp_offset
        return time.time()

    def format_time(self, fmt: str = '%Y-%m-%d %H:%M:%S', tz: Optional[str] = None) -> str:
        """Format current time

        Args:
            fmt: strftime format string
            tz: Timezone string

        Returns:
            Formatted time string
        """
        current_time = self.get_ntp_time(tz)
        return current_time.strftime(fmt)

    def get_iso_time(self, tz: Optional[str] = None) -> str:
        """Get ISO 8601 formatted time"""
        current_time = self.get_ntp_time(tz)
        return current_time.isoformat()

    def get_readable_time(self, tz: Optional[str] = None) -> str:
        """Get human-readable time

        Returns: e.g., "Sunday, June 29, 2026 at 3:45 PM UTC"
        """
        current_time = self.get_ntp_time(tz)
        return current_time.strftime('%A, %B %d, %Y at %I:%M %p %Z')

    def time_until(self, target: datetime.datetime) -> Dict[str, int]:
        """Calculate time remaining until target datetime

        Args:
            target: Target datetime

        Returns:
            Dict with days, hours, minutes, seconds
        """
        current = self.get_ntp_time()
        if isinstance(target, datetime.datetime) and target.tzinfo is None:
            target = pytz.UTC.localize(target)

        delta = target - current

        if delta.total_seconds() < 0:
            return {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'negative': True}

        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': secs,
            'negative': False,
            'total_seconds': delta.total_seconds()
        }

    def time_since(self, start: datetime.datetime) -> Dict[str, int]:
        """Calculate time elapsed since start datetime

        Args:
            start: Start datetime

        Returns:
            Dict with days, hours, minutes, seconds
        """
        current = self.get_ntp_time()
        if isinstance(start, datetime.datetime) and start.tzinfo is None:
            start = pytz.UTC.localize(start)

        delta = current - start

        if delta.total_seconds() < 0:
            return {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0}

        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': secs,
            'total_seconds': delta.total_seconds()
        }

    def add_time(self, days: int = 0, hours: int = 0,
                 minutes: int = 0, seconds: int = 0) -> datetime.datetime:
        """Add time to current NTP time

        Returns:
            New datetime
        """
        current = self.get_ntp_time()
        delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return current + delta

    def subtract_time(self, days: int = 0, hours: int = 0,
                      minutes: int = 0, seconds: int = 0) -> datetime.datetime:
        """Subtract time from current NTP time

        Returns:
            New datetime
        """
        current = self.get_ntp_time()
        delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return current - delta

    def get_status(self) -> Dict[str, any]:
        """Get NTP synchronization status"""
        return {
            'synced': self.is_synced,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'offset_seconds': self.ntp_offset,
            'current_time_utc': self.get_ntp_time().isoformat(),
        }


# Global instance
_manager: Optional[NTPTimeManager] = None


def init_ntp() -> Tuple[bool, str]:
    """Initialize global NTP manager

    Returns:
        Tuple of (success: bool, message: str)
    """
    global _manager
    _manager = NTPTimeManager()
    return _manager.auto_sync()


def get_ntp_time(tz: Optional[str] = None) -> datetime.datetime:
    """Get current NTP-synchronized time"""
    if _manager is None:
        init_ntp()
    return _manager.get_ntp_time(tz)


def get_current_time(fmt: str = '%Y-%m-%d %H:%M:%S', tz: Optional[str] = None) -> str:
    """Get formatted current time"""
    if _manager is None:
        init_ntp()
    return _manager.format_time(fmt, tz)


def get_timestamp() -> float:
    """Get current Unix timestamp"""
    if _manager is None:
        init_ntp()
    return _manager.get_timestamp()


def get_iso_time(tz: Optional[str] = None) -> str:
    """Get ISO 8601 formatted time"""
    if _manager is None:
        init_ntp()
    return _manager.get_iso_time(tz)


def get_readable_time(tz: Optional[str] = None) -> str:
    """Get human-readable time"""
    if _manager is None:
        init_ntp()
    return _manager.get_readable_time(tz)


def time_until(target: datetime.datetime) -> Dict[str, int]:
    """Calculate time until target"""
    if _manager is None:
        init_ntp()
    return _manager.time_until(target)


def time_since(start: datetime.datetime) -> Dict[str, int]:
    """Calculate time since start"""
    if _manager is None:
        init_ntp()
    return _manager.time_since(start)


def add_time(days: int = 0, hours: int = 0,
             minutes: int = 0, seconds: int = 0) -> datetime.datetime:
    """Add time to current time"""
    if _manager is None:
        init_ntp()
    return _manager.add_time(days, hours, minutes, seconds)


def subtract_time(days: int = 0, hours: int = 0,
                  minutes: int = 0, seconds: int = 0) -> datetime.datetime:
    """Subtract time from current time"""
    if _manager is None:
        init_ntp()
    return _manager.subtract_time(days, hours, minutes, seconds)


def get_status() -> Dict[str, any]:
    """Get NTP status"""
    if _manager is None:
        init_ntp()
    return _manager.get_status()


# ============================================
# EXAMPLE USAGE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("NTP TIME FUNCTIONS - DEMO")
    print("=" * 60)

    print("\n⏱️  Initializing NTP synchronization...")
    success, message = init_ntp()
    print(f"   {message}")

    if success:
        print("\n✅ Current Time Functions:")
        print(f"   UTC Time: {get_readable_time()}")
        print(f"   US/Eastern: {get_readable_time('US/Eastern')}")
        print(f"   Europe/London: {get_readable_time('Europe/London')}")
        print(f"   Asia/Tokyo: {get_readable_time('Asia/Tokyo')}")
        print(f"   ISO 8601: {get_iso_time()}")
        print(f"   Timestamp: {get_timestamp()}")

        print("\n📅 Time Calculations:")
        tomorrow = add_time(days=1)
        print(f"   Tomorrow: {tomorrow.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        next_week = add_time(days=7)
        time_remaining = time_until(next_week)
        print(f"   Next week at this time: {time_remaining}")

        yesterday = subtract_time(days=1)
        time_elapsed = time_since(yesterday)
        print(f"   Time since yesterday: {time_elapsed}")

        print("\n📊 NTP Status:")
        status = get_status()
        print(f"   Synchronized: {status['synced']}")
        print(f"   Last sync: {status['last_sync']}")
        print(f"   Offset: {status['offset_seconds']:.3f} seconds")
    else:
        print(f"\n❌ {message}")
        print("   Using system time instead")
        print(f"   Current time: {get_readable_time()}")
