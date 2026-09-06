"""
Demonstration of genpark-code-execution-timeout-watchdog-timer-skill
"""

import time
from client import ExecutionTimeoutWatchdogClient

def fast_calculation():
    return sum(x * x for x in range(1000))

def slow_infinite_loop():
    time.sleep(1.0)
    return "Never returns"

def main():
    watchdog = ExecutionTimeoutWatchdogClient()

    # Fast task passes cleanly
    res1 = watchdog.run_with_timeout(fast_calculation, timeout_sec=0.5)
    print("=== FAST TASK RUN ===")
    print(f"Status: {res1['status']} | Elapsed: {res1['elapsed_sec']}s | Result: {res1['result']}")

    # Slow task is safely timed out
    res2 = watchdog.run_with_timeout(slow_infinite_loop, timeout_sec=0.2)
    print("\n=== SLOW TASK RUN ===")
    print(f"Status: {res2['status']} | Elapsed: {res2['elapsed_sec']}s | Error: {res2['error']}")

if __name__ == "__main__":
    main()
