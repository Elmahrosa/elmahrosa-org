# Phase 3.4 — Field-Level At-Rest Encryption Evidence (DRAFT — preparatory, not gated)

**Status:** 🟡 **DRAFT** — non-normative preparatory document authorized by founder (2026-09-13). Not an acceptance artifact. No production schema changes are authorized by this document.
**Evidence base:** `docs/quantum-safe-stack/inventory/0_1_current_crypto_inventory.md`. **Closes, in part, Phase 2.3 CONDITIONAL PASS minor issue #2 (no documented integrity protection for stored cryptographic assets) — per `validation/security/2_3_security_properties_report.md` (recorded 2026-09-13).**

---

## 1. Verified baseline (0.1)

- PostgreSQL sessions and data at rest: **no field-level at-rest encryption found** (`pgcrypto` absent, no column-level encryption).
- Session tokens: stored as **SHA-256 hashes at rest** (opaque 256-bit tokens; `services/session.js`) — digest-at-rest already mitigates token theft exposure; this must NOT be weakened.
- Credentials: PBKDF2-SHA512 (100k iters, 64-byte key, 16-byte salt) as derived-key storage (`services/auth.js`).

## 2. Gap statement

Collecting PII/credential-like data in plaintext columns is an accepted 0.1 residual risk. Closing it is a **runtime-enablement** action gated under Phase 3 (this file provides the evidence plan, not the solution).

## 3. Candidate approach (for evaluation, no commitment)

- `pgcrypto` **AES-256-GCM** column-level encryption for the sensitive field set (as defined in 3.4 data classification table).
- **Envelope encryption**: DEK per record/column family, KEK in external KMS or hardware boundary; DEK never logged.
- Key rotation with versioned key IDs; tombstoned keys retained for decrypt.
- Network transport for PG remains TLS (Z4 in `3_3_tls_zone_cipher_profile_draft.md`).

## 4. Evidence / validation plan (for gate)

| Check | Method | Gate |
|---|---|---|
| `pgcrypto` availability | `CREATE EXTENSION pgcrypto;` | ✅ eligible |
| Ciphertext at rest | `pg_dump` of sensitive table shows no plaintext values | ✅ PASS required |
| No plaintext in logs | log-scan SAR pattern over sensitive fields | ✅ PASS required |
| Key rotation | rotate version, decrypt with old version, re-encrypt | ✅ PASS required |
| Performance | query latency delta benchmark recorded | ✅ recorded |

## 5. Non-change guarantees

- Session-token hashing and PBKDF2 credential derivation stay as-is (do not weaken).
- CBOM inventory (`quantum-inventory.cbom.json`) must be updated when implemented (add AES-256-GCM usage under `teos:` namespace).
- No claim of at-rest encryption is made until the above checks pass with committed evidence.

## 6. Status summary

- Draft prepared (2026-09-13). Implementation evidence: **NONE yet** — remains OPEN.
- Owner: Elmahrosa-Teos (founder); scheduled for Phase 3 runtime enablement.