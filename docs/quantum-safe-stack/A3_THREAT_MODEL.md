# A3 — Threat Model (Phase 0.3)

**Milestone:** Phase 0.3 (FINAL_ORDER.md §2)
**Status:** DRAFT v1 — 2026-09-13, founder-supervised
**Scope boundary:** This model covers the **Quantum-Safe Stack (QSS) program** (this repository) — an interface-only foundation with **zero live cryptographic operations** — and the **classical cryptography currently in use** by the DealMaker application it will ultimately secure (see `docs/quantum-safe-stack/inventory/0_1_current_crypto_inventory.md`).

---

## 1. Assumptions & Scope

- **IN-SCOPE**
  - Live classical crypto inventory (0.1) and its forward exposure.
  - QSS interface contracts: A2 `COMMON-CONTRACT.md`, A3 CBOM/API/audit/access-control specifications, orchestration stubs.
  - Harvest-now-decrypt-later (HNDL) exposure of in-transit and at-rest data.
- **OUT-OF-SCOPE (explicitly)**
  - Any live quantum cryptographic operation (none exist — Phase 4 deployment only).
  - Physical-layer QKD/QRNG hardware validation (interface stubs only).
  - Application logic bugs not tied to cryptography or the QSS boundary.
- **Adversary model:** A quantum-capable adversary (QCA) who can (a) harvest and store ciphertext/signatures/tokens today, (b) later break RSA/ECDH/ECDSA-class classical asymmetric primitives on a cryptographically relevant quantum computer (CRQC), and (c) mount offline Grover-speed attacks where applicable. Classical adversaries remain in scope for defense-in-depth.

---

## 2. Assets

| ID | Asset | Confidentiality | Integrity | Availability |
|---|---|---|---|---|
| A1 | Session tokens (opaque bearer; SHA-256 hash at rest) | High | High | Medium |
| A2 | Report tokens (192-bit, public report URLs) | High | Medium | Low |
| A3 | Webhook/outbound HMAC keys and payload signatures | High | High | Medium |
| A4 | Password hashes (PBKDF2-SHA512) | High | High | High |
| A5 | Connector OAuth2 access/refresh tokens (env vars) | High | High | Medium |
| A6 | TLS-protected data in transit (DealMaker ↔ edge ↔ clients) | High | High | High |
| A7 | CBOM / A3 contract data (this repo) | Medium | High | Medium |
| A8 | Audit trail (hash-chained, SP 800-57 Pt 3) | Medium | High | Medium |

---

## 3. Threat Statements

| ID | Threat | Adversary | Asset | Quantum relevance |
|---|---|---|---|---|
| T1 | **HNDL on TLS**: adversary records TLS 1.2/1.3 traffic, later breaks classical key exchange to recover plaintext | QCA (record now, decrypt later) | A6 | **PRIMARY — FIPS 203/204/205 migration target (P1)** |
| T2 | **HNDL on OAuth2 token exchange**: bearer tokens carried over TLS are recoverable if TLS breaks | QCA | A5, A6 | High — mitigated by T1 remediation |
| T3 | **Signature forgery after CRQC**: HMAC-SHA256 (2048/3072-bit-equivalent NIST security) weakened by Grover (128-bit → ~64-bit effective) | QCA (post-break forgery) | A3 | **High — SLH-DSA/ML-DSA candidate (P2)** |
| T4 | **Session-token at-rest compromise**: stolen DB yields SHA-256 hashes; if token entropy insufficient, offline distinguishability increases | Classical thief + QCA (Grover preimage) | A1 | Medium — 256-bit tokens retain ≥128-bit post-Grover security |
| T5 | **Report-token enumeration**: 192-bit randomness; quantum no significant gain; risk is classical guess-rate / logging leakage | Classical | A2 | Low |
| T6 | **Audit tampering undetected**: without hash-chaining, adversary rewrites audit trail | Classical / QCA | A8 | Medium — chaining design already in A3_AUDIT_TRAIL_SPEC |
| T7 | **Algorithm-confusion in stub → live transition**: interfaces migrated to live crypto without re-validation | Internal (process) | A7 | Governance — Rule 1/2, change control §7 |
| T8 | **CBOM/cryptographic-asset metadata drift**: inventory diverges from reality (e.g., a new classical primitive added post-lock) | Internal | A7 | Governance — continuous inventory per §7 |

---

## 4. Mitigations (mapped to program phases)

| Threat | Primary control | Phase |
|---|---|---|
| T1, T2 | QSS migration to FIPS 203 (ML-KEM) key establishment + FIPS 204 (ML-DSA) / FIPS 205 (SLH-DSA) authentication; hybrid via CBOM composition | Phase 2/3 → Phase 4 rollout (HNDL window closure) |
| T3 | Post-quantum signature adoption for webhook payload integrity; algorithm agility via `teos:algorithmFamily` abstraction | Phase 1/2 |
| T4 | Session tokens remain 256-bit CSPRNG; store one-way hash only (already implemented); reassess with SP 800-90B/C QRNG at rollout | Phase 4 |
| T5 | Keep 192-bit report tokens; avoid logging; expiry/revocation alignment | Continuous |
| T6 | Append-only, hash-chained audit events (D3 ratified, A3_AUDIT_TRAIL_SPEC) | Phase 2 |
| T7 | No milestone marked ✅ without committed evidence + hash (Rule 1); A2 re-validation on any contract change (§7) | Governance |
| T8 | Continuous inventory (`quantum-inventory.cbom.json`, `audit-data/quantum/`), update process defined in A3_CHANGE_CONTROL_PROCESS | Continuous |

---

## 5. Residual Risks

1. **HNDL window:** Any traffic encrypted before migration is at risk if a CRQC matures before rollout. Residual risk accepted with **P1 priority** and explicit founder tracking.
2. **Platform TLS edge:** Cipher-suite/zone profile at the Railway/Hostinger edge is platform-managed; full profile audit deferred to Phase 3 (3.3/3.4).
3. **Field-level encryption at rest:** No evidence of at-rest field encryption in DealMaker DB; exposure is privacy-adjacent and tracked in 0.1 open items.
4. **QKD/QRNG adoption:** Non-NIST-standardized; adoption remains optional and requires PQC-authenticated hybrid design (already specified in `teos-qkd.md`).

---

## 6. Disposition

- This model supersedes any prior informal threat notes and becomes part of the A3 LOCKED package once Phase 0 exit gate is satisfied.
- Revisit trigger for v2: any new classical primitive added to inventory, TLS profile change, or post-quantum algorithm standard update.