# 0.1 — Current Cryptography in Use (Inventory)

**Milestone:** Phase 0.1 (FINAL_ORDER.md §2)
**Method:** Read-only source inspection of the DealMaker application codebase (`repos/teos-dealmaker`, working tree inspected 2026-09-13).
**Scope boundary:** This inventory records *live, classical* cryptography currently in use by the DealMaker application that the Quantum-Safe Stack (QSS) migration must later address. The QSS program itself (this repository) remains **interface-only with zero live cryptographic operations** — nothing in `modules/quantum-safe/` is exercised.
**Evidence:** Each row cites the verifiable location. **Never inferred:** rows with no source citation are explicitly marked.

## Inventory Table

| # | Area | Mechanism & Parameters | Evidence | State |
|---|---|---|---|---|
| 1 | Session tokens (at-rest) | 256-bit opaque bearer token from `crypto.randomBytes(32)`; only **SHA-256** hex digest persisted; TTL 24h default | `services/session.js:23-33`, `hashToken()`, `newToken()` | VERIFIED (live) |
| 2 | Session cookie (transport) | `teos_session` cookie; `httpOnly`, `sameSite: strict`, `secure` only over TLS; fail-closed verify | `services/session.js:74-89`, `setSessionCookie()`, server `checkFounderSession` (`server/index.js:198`) | VERIFIED (live) |
| 3 | Password hashing | **PBKDF2-SHA512**, 100,000 iterations, 64-byte derived key, 16-byte random salt | `services/auth.js:16,28` | VERIFIED (live) |
| 4 | HMAC — webhook signature | **HMAC-SHA256** over raw body, `sha256=` prefix, constant-time compare via `timingSafeEqual` | `services/billing/index.js:99-107` (SparkPost webhook verification) | VERIFIED (live) |
| 5 | HMAC — outbound payload | **HMAC-SHA256** payload signature | `services/outboundWorker/index.js:607` | VERIFIED (live) |
| 6 | Report tokens | Unguessable 192-bit `report_token` for public mission report URLs `/report/:reportToken`; stored in `plans` table | `server/index.js:565-575`, `services/missionReport.js:107-108` | VERIFIED (live) |
| 7 | Content / audit digests | **SHA-256** fingerprints for email-content dedup and audit-log integrity | `services/customer0/index.js:150,467`, `services/outboundWorker/index.js:184-185`, `utils/auditLogger.js:17` | VERIFIED (live) |
| 8 | Database transport | PostgreSQL via `pg` `Pool`; TLS on connection configurable via `ssl` setting; **no evidence of at-rest field encryption** (no `pgcrypto`/field-level encryption found) | `db/index.js:16`, `db/adapter.js:73`, `package.json` (`pg ^8.22.0`) | VERIFIED — at-rest encryption **NOT FOUND** |
| 9 | JWT | **NOT PRESENT** — no `jsonwebtoken`/`jose`/`jwt` dependency; no local JWT issuance or verification | `package.json` | VERIFIED (absent) |
| 10 | OAuth2 — connectors | Authorization-code flow for CRM/email/calendar/storage connector access tokens; tokens held in environment variables | `services/integrations/oauth.js`, `services/integrations/catalog.js` | VERIFIED (live, outbound only) |
| 11 | TLS termination | Application binds plain HTTP on `PORT` (`server/index.js:1763`); TLS terminated at deployment platform edge (Railway/Hostinger); `req.secure` honours configured trust proxy for cookie hardening | `server/index.js:1763`, `services/session.js:70` | VERIFIED (platform edge) |
| 12 | CSPRNG | Node `crypto.randomBytes` (OpenSSL-backed system CSPRNG) for session tokens and salts | `services/session.js:29`, `services/auth.js:28` | VERIFIED (live) |

## Quantum-Relevant Observations

- **Harvest-now-decrypt-later exposure** is concentrated in transport and integrity primitives: TLS 1.2/1.3 sessions (row 11), HMAC-SHA256 payload signatures (rows 4–5), and SHA-256 at-rest session hashes (row 1).
- Password hashing (row 3) is not a harvest-now/decrypt-later target; PBKDF2-SHA512 remains acceptable for offline-verification resistance.
- No post-quantum primitives, QRNG, or QKD are in use anywhere — confirmed live-crypto state is purely classical.

## Limitations & Open Items

1. **Field-level encryption at rest:** No evidence found (`pgcrypto` absent). If present at another layer, it must be added to this inventory.
2. **Deployment TLS cipher/profile:** Actual zones/cipher suites at the Railway/Hostinger edge were not inspected from this repo; row 11 records termination point only.
3. **Secret storage:** Access tokens/keys live in environment variables; vault/kms usage not evidenced.
4. Internal app identity uses bearer sessions; OAuth2 is outbound-only. No mTLS.

## Approval Record

- Prepared: 2026-09-13 — source inspection by AI builder, founder-supervised.
- Found: `docs/quantum-safe-stack/inventory/0_1_current_crypto_inventory.md`