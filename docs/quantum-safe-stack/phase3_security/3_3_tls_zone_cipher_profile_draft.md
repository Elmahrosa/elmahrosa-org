# Phase 3.3 — TLS Zone & Cipher Profile (DRAFT — preparatory, not gated)

**Status:** 🟡 **DRAFT** — non-normative preparatory document authorized by founder (2026-09-13). Not an acceptance artifact. No deployment provider claim has been verified yet.
**Relationship:** Inputs to Phase 3.3 connector/integration work and Phase 3.4 readiness gate; addresses 0.1 open item "deployment TLS zone/cipher profile verification (Phase 3.3/3.4)". **Closes, in part, Phase 2.3 CONDITIONAL PASS minor issue #3 (API lacks application-level integrity beyond TLS) and the documented HNDL exposure (threat `T1`) — per `validation/security/2_3_security_properties_report.md` (recorded 2026-09-13).**
**Evidence base:** `docs/quantum-safe-stack/inventory/0_1_current_crypto_inventory.md` (TLS 1.2/1.3 terminated at platform edge; app container binds plain HTTP internally).

---

## 1. TLS Zones

| Zone | Description | Current verified state (0.1 evidence) | Target |
|---|---|---|---|
| Z1 | Edge / ingress (Railway / Hostinger platform) | TLS 1.2/1.3 terminated at platform edge | TLS 1.3 preferred, TLS 1.2 minimum, HSTS |
| Z2 | App container internal (HTTP binding) | App binds plain HTTP — TLS currently courtesy of platform edge only | Keep internal non-TLS only where loopback/unroutable; document explicitly |
| Z3 | Inter-service / outbound connectors (CRM, storage, email, webhooks) | OAuth2 tokens / HMAC-SHA256 per inventory rows 4–5 | TLS 1.2+ on all egress; token + payload secrecy |
| Z4 | Database (PostgreSQL via `pg` Pool) | No transport-level client cert; at-rest encryption **NOT FOUND** (see 3.4 draft) | TLS for PG connections; field-level encryption per 3.4 |

## 2. Cipher Suite Profile (draft)

**TLS 1.3 (preferred):**
- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_GCM_SHA256`
- Key exchange: ECDHE with X25519 or P-256 (or curve PQC-hybrid when available)

**TLS 1.2 (minimum, no TLS < 1.2):**
- `ECDHE_RSA_AES_256_GCM_SHA384`
- `ECDHE_ECDSA_AES_256_GCM_SHA384`
- `ECDHE_RSA_AES_128_GCM_SHA256`
- Disable: TLS 1.0/1.1, CBC-mode cipher suites, RSA key exchange, SHA-1

**Headers/behaviors to verify at edge:** HSTS (`max-age`), OCSP stapling, certificate rotation slack, no forward secrecy downgrade.

## 3. HNDL (harvest-now-decrypt-later) mitigation posture

- Until PQC hybrid key exchange is implemented (later phase), the TLS transport remains the **primary HNDL exposure** (threat `T1` in `A3_THREAT_MODEL.md`). Residual risk **documented, not closed**.
- Priority mitigations: enforce TLS 1.3 + forward secrecy now; migrate transport key exchange to a PQC-hybrid (FIPS 203) profile as part of runtime enablement; keep session hash-at-rest (SHA-256) intact.

## 4. Verification (OPEN — requires deployment provider)

| Check | Method | Status |
|---|---|---|
| Actual edge cipher suite list | `testssl.sh` / `sslscan` against live endpoint (or platform docs) | 🔲 NOT VERIFIED |
| HSTS presence & policy | curl -sI | 🔲 NOT VERIFIED |
| Cert chain / expiry slack | OpenSSL parse | 🔲 NOT VERIFIED |
| Internally reachable zone mapping (Z2) | host network inspection | 🔲 NOT VERIFIED |

**Clearance of these checks is required before Phase 3.3/3.4 gating.**