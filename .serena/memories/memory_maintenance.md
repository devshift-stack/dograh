# Memory Maintenance

## Discovery model

- Treat `mem:core` as the graph root.
- Organize focused memories by domain or module when stable complexity warrants it.
- References use the `mem:` prefix inside backticks and explain the referenced content precisely.
- The referring memory states when another memory is relevant; referenced memories contain facts, not read-routing prose.

## Style

- Dense agent notes; prefer terse invariants and bullets.
- Record only durable, non-obvious repo facts that prevent costly rediscovery.
- Exclude generic framework knowledge, task-local state, transient versions, local machine state, secrets, and session notes.

## Maintenance

- Update a memory only when a stable repo contract changes.
- Use Serena's rename tool so references are updated atomically.
- Run `serena memories check` from the project root after structural memory changes.