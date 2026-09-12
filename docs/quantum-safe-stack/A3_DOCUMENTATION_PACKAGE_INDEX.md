# A3 Documentation Package Index

Index of the interface-only documentation package for the Teos Quantum-Safe Orchestration Layer. This package is validation-focused: **no live cryptographic operations, key generation, or QKD hardware integration** is included or authorized.

## Package Root

- Location: `docs/quantum-safe-stack/`
- Module contracts: `modules/quantum-safe/`
- Committed baseline: `32fe5d7` (`main`)

## Specification Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `README.md` | Stack overview and module links | ✅ |
| `teos-qkd.md` | QKD module spec (FIPS 204 classical-channel auth) | ✅ |
| `teos-qrng.md` | QRNG module spec (SP 800-90B/C entropy) | ✅ |
| `teos-pqc.md` | PQC module spec and FIPS 203/204/205 parameter tables | ✅ |
| `teos-quantum-safe-orchestration-layer.md` | Orchestration layer spec | ✅ |
| `vision.md` | Stack vision/context | ✅ |

## A2 Contract Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `A2_NIST_INTERFACE_CONTRACT_VALIDATION_REPORT.md` | Original A2 validation | ✅ |
| `A2_NIST_INTERFACE_CONTRACT_REVALIDATION_REPORT.md` | A2 re-validation of blocking-issue resolutions | ✅ (re-verified this session on committed state) |

## A3 Specification Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `A3_CBOM_SCHEMA_SPEC.md` | CBOM mapping to CycloneDX 1.6 + Teos extensions, canonical enums | ✅ |
| `A3_TEOS_CBOM_EXTENSION.schema.json` | JSON Schema for `teos:*` extension properties | ✅ |
| `A3_CBOM_EXAMPLE.json` | Machine-readable CBOM fixture (valid JSON, keys corrected to bits, `metadata.component.type` present) | ✅ |
| `bom-1.6.schema.json` + `spdx.schema.json` + `jsf-0.82.schema.json` | Official CycloneDX 1.6 schemas pinned locally for validation | ✅ |
| `A3_CBOM_EXAMPLE.cyclonedx-valid.json` | CycloneDX-1.6-conformant array-form transform of the fixture (schema-valid) | ✅ |
| `A3_CBOM_API_OPENAPI.yaml` | OpenAPI 3.1 spec: registration, rotation, snapshot | ✅ (Redocly 0 errors; scopes include `cbom.audit`, `cbom.admin`) |
| `A3_DATAFLOW_DIAGRAM.md` | Mermaid data-flow diagrams cross-checked vs A2 | ✅ |
| `A3_AUDIT_TRAIL_SPEC.md` | Append-only SHA-256 hash-chained audit events | ✅ |
| `A3_ACCESS_CONTROL_POLICY.md` | mTLS/OAuth2, RBAC/ABAC, graduated redaction | ✅ (GDPR 2016/679 corrected) |

## Validation and Process Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `A3_VALIDATION_REPORT.md` | Mechanical validation results | ✅ (state as documented; CycloneDX run pending) |
| `PRE_SIGNATURE_CHECKLIST.md` | Pre-signature verification checklist | ✅ (paths normalized) |
| `A3_IMPLEMENTATION_ROADMAP.md` | 6-month interface-only roadmap | ✅ (milestones deduplicated) |
| `A3_READINESS_REVIEW.md` | Readiness criteria vs. roadmap success criteria, open items | ✅ created |
| `A3_CHANGE_CONTROL_PROCESS.md` | Change categories, approval matrix, A2 re-validation gate | ✅ created |
| `A3_IMPLEMENTATION_GUIDANCE.md` | Implementer guidance (contracts, CBOM, audit, security) | ✅ created |
| `A3_TRAINING_MATERIALS.md` | Training outline for implementation teams | ✅ created |
| `A3_FOUNDER_SIGN_OFF.md` | Founder sign-off | ⏳ **DRAFT — awaiting founder signature** |

## Module Contract Documents

| Document | Purpose |
|----------|---------|
| `modules/quantum-safe/COMMON-CONTRACT.md` | Central error model and conventions (`Result<T, TeosError>`, `NOT_IMPLEMENTED`) |
| `modules/quantum-safe/teos-qkd/README.md` | QKD interfaces |
| `modules/quantum-safe/teos-qrng/README.md` | QRNG interfaces |
| `modules/quantum-safe/teos-pqc/README.md` | PQC interfaces |
| `modules/quantum-safe/teos-orchestration-layer/README.md` | Orchestration interfaces incl. `cbom_snapshot()` |
| `modules/quantum-safe/teos-orchestration-layer/cbom-schema.md` | CBOM TypeScript schema (aligned enums) |
| `modules/quantum-safe/teos-orchestration-layer/A1_CBOM_SCHEMA_VALIDATION_REPORT.md` | A1 CBOM schema validation report |

## Planned But Not Yet Created

| Document | Milestone | Status |
|----------|-----------|--------|
| `A3_FEEDBACK_AND_RESPONSES.md` | M2.5 External review | pending external review |
| `A3_FINAL_REVIEW_PACKAGE.md` | M3.5 Final review | pending M3.1-M3.4 plus founder signature |

## Open Integration Questions

- MAPI.6: `Idempotency-Key` header support (unresolved design question #1)
- Rate limiting / 429 behavior (unresolved design question #2)

## Commit Baseline

Package contents are committed on `main` (SET A batch `32fe5d7`; Phase-3 artifacts `4ebb412`). CycloneDX 1.6 validation results and schema/artifact additions in this index are versioned in the follow-up commit.