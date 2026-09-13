# Phase 3.5 — Crypto Module Security Documentation (DRAFT — preparatory, not gated)

**Status:** 🟡 **DRAFT** — non-normative preparatory document authorized by founder (2026-09-13). Not an acceptance artifact. No interface contract change is authorized by this document.
**Relationship:** Closes, in part, the remaining **Phase 2.3 CONDITIONAL PASS** items — minor issue #1 (missing explicit confidentiality statements), #4 (API non-repudiation weaker), #5 (no side-channel resistance documentation) — per `validation/security/2_3_security_properties_report.md` (recorded 2026-09-13), and Recommendation #6 (cross-cutting security-properties appendix in `COMMON-CONTRACT.md`).
**Current verified state:** `modules/quantum-safe/COMMON-CONTRACT.md` contains **no** confidentiality assertions, side-channel resistance requirements, or API non-repudiation definitions (grep-checked 2026-09-13). This matches 2.3 findings. Nothing here claims these are already present.

---

## 1. Scope

This draft defines the **documentation requirements to add** to the interface/contract layer so the documented gaps are closed. It is a plan of record, not an implementation.

## 2. Confidentiality assertions (2.3 minor issue #1; Recommendation #1)

Each crypto module interface shall assert, for keys/secrets/entropy it handles:

- **Teos-PQC:** secret key material never leaves the interface boundary except via the defined key-export path; callers own secret protection after handoff.
- **Teos-QKD:** key material is distributed under authenticated channel; entropy/key material at rest protected per Phase 3.4.
- **Teos-QRNG:** output randomness is the output of the validated entropy source (SP 800-90B); raw noise not exported.

## 3. Side-channel resistance documentation (2.3 minor issue #5; Recommendation #5)

- Add a side-channel requirements subsection to **each** crypto module interface spec referencing at least one of: **ISO/IEC 17825**, **FIPS 140-3**, **NIST SP 800-53 SC-46**.
- SP 800-90B coverage in Teos-QRNG addresses entropy-source side-channels only — document this explicitly, and state it is **not** a module-wide side-channel mitigation claim.
- Teos-PQC/QKD interfaces shall document expected countermeasures (constant-time operations, secret zeroization) where applicable.

## 4. API non-repudiation (2.3 minor issue #4; Recommendation #4)

- High-value API operations: evaluate **proof-of-possession** for OAuth2 tokens, or document explicit **mTLS** non-repudiation expectations with entity-bound client certificates.
- Key registration/rotation operations: specify a signing/audit mechanism (see `A3_AUDIT_TRAIL_SPEC.md`).

## 5. Cross-cutting appendix (2.3 Recommendation #6)

- Create a **security-properties appendix** in `COMMON-CONTRACT.md` summarizing inherited protections: secret zeroization, constant-time comparison, audit logging, and the per-module confidentiality/at-rest/side-channel statements above.

## 6. Non-change guarantees

- No module interface specification, source change, or live implementation is authorized by this document.
- CBOM inventory must be updated if any of these become normative (add references under `teos:` namespace).
- No claim of gap closure is made until the corresponding docs are written, committed, and re-validated.

## 7. Status summary

- Draft prepared (2026-09-13). Documentation authoring for sections 2–5: **NOT STARTED** — remains OPEN, gated on Phase 2 closure.
- Owner: Elmahrosa-Teos (founder).