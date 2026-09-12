# Elmahrosa Org — Quantum-Safe Stack

> **Status:** A3 LOCKED (qss-a3-locked) · No live crypto

This repository contains the quantum-safe security architecture for the
Elmahrosa platform: documentation, interface contracts, CBOM schema
mapping, and validation artifacts aligned with NIST FIPS 203/204/205
and supporting standards.

All module implementations are **interface-only stubs** returning
`TeosError::NOT_IMPLEMENTED`. No cryptographic operations are active.

---

## Quick Links

| What | Where |
|------|-------|
| **Package index (start here)** | `docs/quantum-safe-stack/A3_DOCUMENTATION_PACKAGE_INDEX.md` |
| **Readiness review** | `docs/quantum-safe-stack/A3_READINESS_REVIEW.md` |
| **Founder sign-off** | `docs/quantum-safe-stack/A3_FOUNDER_SIGN_OFF.md` |
| **OpenAPI spec** | `docs/quantum-safe-stack/A3_CBOM_API_OPENAPI.yaml` |
| **CBOM schema + fixture** | `docs/quantum-safe-stack/A3_CBOM_SCHEMA_SPEC.md` |
| **Validation report** | `docs/quantum-safe-stack/A3_VALIDATION_REPORT.md` |
| **Contract revalidation** | `docs/quantum-safe-stack/A2_NIST_INTERFACE_CONTRACT_REVALIDATION_REPORT.md` |
| **Common contract conventions** | `modules/quantum-safe/COMMON-CONTRACT.md` |
| **Implementation roadmap** | `docs/quantum-safe-stack/A3_IMPLEMENTATION_ROADMAP.md` |

---

## Module Stack

| Module | Standards | Interface Contract |
|--------|-----------|-------------------|
| **Teos-PQC** | FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) | `keypair`, `encapsulate`, `decapsulate`, `sign`, `verify` |
| **Teos-QKD** | ETSI GS QKD 014, ITU-T Y.3800, NIST SP 1800-38, FIPS 204 (auth) | `authenticate_channel`, `exchange_key` |
| **Teos-QRNG** | NIST SP 800-90B/C | `health_test`, `get_entropy`, `continuous_validation` |
| **Orchestration** | NIST SP 800-57 Part 3, CycloneDX 1.6 | `register_algorithm`, `rotate_key`, `cbom_snapshot` |

> **Note:** QKD is not NIST-standardized. In this architecture QKD is
> an optional key source layered on top of PQC, never a substitute for
> it. Classical-channel authentication requires ML-DSA (FIPS 204).

---

## Gate State

```
A2  Interface contracts     PASS · immutable
A3  CBOM schema + API       LOCKED · qss-a3-locked
    Live crypto             None — all stubs return NOT_IMPLEMENTED
    Open enhancements       Rate-limit headers / 429 body
    Change control          Any touch to locked A3 → A2 re-validation → founder re-approval
Phase 1                     Not started
```

---

## Commits

| Hash | Description |
|------|-------------|
| `32fe5d7` | Quantum-Safe SET A documentation + site audit fixes |
| `4ebb412` | Phase-3 (A3) progression artifacts |
| `72217ed` | CycloneDX 1.6 schema validation, metadata fix, pinned schemas |

---

## For External Reviewers

Start at `docs/quantum-safe-stack/A3_DOCUMENTATION_PACKAGE_INDEX.md`.
It maps every deliverable to its purpose, status, and evidence file.
Validate the CBOM fixture against the pinned CycloneDX 1.6 schema:

```bash
ajv validate -s schemas/bom-1.6.schema.json \
             -d docs/quantum-safe-stack/A3_CBOM_EXAMPLE.cyclonedx-valid.json
```

---

## License / Confidentiality

[Insert org-specific license or confidentiality notice here]