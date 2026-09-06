"""
Thread Execution Watchdog Timer and Deadline Governor.
Zero external dependencies, standard library only.
"""

import time
import threading
from typing import Dict, Any, Callable, Tuple

class ExecutionTimeoutWatchdogClient:
    """
    Executes worker callables under strict deadline bounds:
    - Spawns background worker thread
    - Enforces timeout threshold in seconds
    - Returns TIMEOUT_EXCEEDED without blocking main execution thread
    """

    def run_with_timeout(self, fn: Callable, args: Tuple = (), kwargs: Dict = None, timeout_sec: float = 2.0) -> Dict[str, Any]:
        """Runs callable and enforces timeout deadline."""
        kwargs = kwargs or {}
        container = {"result": None, "error": None, "completed": False}

        def worker():
            try:
                container["result"] = fn(*args, **kwargs)
                container["completed"] = True
            except Exception as e:
                container["error"] = f"{type(e).__name__}: {str(e)}"
                container["completed"] = True

        start_time = time.time()
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        thread.join(timeout=timeout_sec)

        elapsed = round(time.time() - start_time, 4)

        if not container["completed"]:
            return {
                "status": "TIMEOUT_EXCEEDED",
                "timeout_sec": timeout_sec,
                "elapsed_sec": elapsed,
                "result": None,
                "error": f"Operation exceeded maximum deadline of {timeout_sec}s"
            }

        if container["error"]:
            return {
                "status": "EXECUTION_ERROR",
                "elapsed_sec": elapsed,
                "result": None,
                "error": container["error"]
            }

        return {
            "status": "SUCCESS",
            "elapsed_sec": elapsed,
            "result": container["result"],
            "error": None
        }
