__all__ = ["FitnessLog"]

from collections import deque
from datetime import datetime


class FitnessLog:
    """A log for tracking fitness evaluations with optional size limit to prevent unbounded memory growth."""
    
    DEFAULT_MAX_SIZE = 10_000  # Keep last 10k entries by default, None for unlimited
    
    def __init__(self, backend: str, max_size: int | None = DEFAULT_MAX_SIZE):
        """Initialize FitnessLog.
        
        Args:
            backend: Storage backend type ('list' supported)
            max_size: Maximum number of entries to keep. None for unlimited (not recommended).
                      When limit is reached, oldest entries are discarded.
        """
        if backend == "list":
            if max_size is not None:
                self._log = deque(maxlen=max_size)
            else:
                self._log = deque()
            self._max_size = max_size
        else:
            raise NotImplementedError

    def __iadd__(self, value):
        self._log.append((datetime.now(), value))
        return self  # Fix: __iadd__ must return self

    def __str__(self):
        return "[" + ",\n ".join(f"({d}, {v})" for d, v in self._log) + "]"
    
    def __len__(self):
        return len(self._log)
    
    def clear(self):
        """Clear all entries from the log."""
        self._log.clear()
