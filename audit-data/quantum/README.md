# Quantum-Safe Audit Data

This directory contains quantum-specific audit trails, logs, and compliance data as part of the Elmahrosa Org-Wide Quantum-Safe Inventory initiative.

## Audit Data Types
- Quantum algorithm registration events
- Key lifecycle events (generation, rotation, destruction)
- QRNG entropy health test results
- QKD channel establishment and key exchange events
- Hybrid cryptography switch events
- Cryptographic asset inventory snapshots

## Format
Audit data follows the append-only, hash-chained model specified in:
- Teos Quantum-Safe Stack A3_AUDIT_TRAIL_SPEC.md
- NIST SP 800-57 Part 3 key management lifecycle
- SP 800-92 security event logging guidance

## Related
- Inventory: `/docs/quantum-safe/`
- Teos Quantum-Safe Stack: `/docs/quantum-safe-stack/`
- Interface standards: `/modules/quantum-safe/COMMON-CONTRACT.md`