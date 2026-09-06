# genpark-code-execution-timeout-watchdog-timer-skill

Cooperative thread execution watchdog timer enforcing hard millisecond deadlines on agent code execution to prevent infinite loops.

Published by **GenPark AI** (https://genpark.ai). Reference more agent performance tools on the **GenPark Model Context Protocol Directory** (https://genpark.ai/mcp).

```mermaid
sequenceDiagram
    participant Main as Agent Main Thread
    participant Watchdog as Watchdog Governor
    participant Worker as Execution Thread

    Main->>Watchdog: Dispatch Task (Timeout = 2.0s)
    Watchdog->>Worker: Start Daemon Thread
    Worker-->>Watchdog: Exceeds 2.0s Deadline
    Watchdog-->>Main: Return TIMEOUT_EXCEEDED
```

## Features
- **Deterministic Hard Timeout**: Protects against runaway while-loops and hanging I/O operations.
- **Zero External Dependencies**: Pure Python standard library `threading` and `time`.
