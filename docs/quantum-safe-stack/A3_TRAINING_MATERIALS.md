# Training Materials Outline — Quantum-Safe Stack Interfaces

Training framework for implementation teams consuming the A3 package. This document provides the outline and key teaching points; detailed slide decks/exercises are developed during knowledge transfer (M3.3) in consultation with the implementation team lead. Emphasis throughout is the interface-only nature of the current work.

## Module 1 — Context and Constraints

- TEOS quantum-safe stack architecture and the 7-layer security model (see `docs/quantum-safe-stack/README.md`)
- Interface-only mandate: **no live crypto, key generation, or QKD hardware in this effort**
- A2 contract immutability and the change control process (`A3_CHANGE_CONTROL_PROCESS.md`)
- NIST landscape: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA), SP 800-90B/C (QRNG entropy), SP 800-57 Part 3 (key lifecycle); QKD is not NIST-standardized

## Module 2 — Interface Contracts

- `COMMON-CONTRACT.md`: `Result<T, TeosError>` error model, `TeosError` enum including `NOT_IMPLEMENTED`
- QKD: `authenticate_channel()` (ML-DSA mandatory), `exchange_key()`
- QRNG: `health_test()`, `get_entropy()`, `continuous_validation()`; SP 800-90B/C validation and DRBG consumption
- PQC: `keypair()`, `encapsulate()`, `decapsulate()`, `sign()`, `verify()`; KEM vs. signature distinction; FIPS-named parameter sets
- Orchestration: `register_algorithm()`, `rotate_key()`, `cbom_snapshot()`

## Module 3 — CBOM Format

- CycloneDX 1.6 base structure (components, `bom-ref`, dependencies)
- Teos extension map (`teos:*` fields) and `A3_TEOS_CBOM_EXTENSION.schema.json`
- Canonical enums: `cryptoAgilityStatus`, `classicalOrPq`, `migrationPriority`; `keySizeBits` integer ≥ 0
- Hybrid representation via `teos:hybridComponents` composition linkage
- Converting the flat internal map to the CycloneDX 1.6 `property` array form for schema validation
- Gap analysis and compliance metadata (`teos:totalAssetsScanned`, `teos:quantumVulnerableCount`, `teos:framework`, `teos:nistPqcStandards`)

## Module 4 — API and Security

- OpenAPI 3.1 specification (`A3_CBOM_API_OPENAPI.yaml`): registration, rotation, snapshot endpoints
- Authentication (mTLS) and authorization (OAuth 2.0 scopes `cbom.read`/`cbom.write`/`cbom.audit`/`cbom.admin`)
- Graduated redaction policy: what is never redacted (public keys, identifiers), the four redaction levels
- Error-to-HTTP mapping consistent with `TeosError`

## Module 5 — Audit Trail

- Append-only / write-once storage, SHA-256 hash chaining, genesis record, monotonic `sequence_number`
- Event types and NIST SP 800-57 Part 3 lifecycle-state mapping
- Tamper-evidence limits (storage integrity assumption; external anchoring is an open design question)

## Module 6 — Labs and Exercises

1. **Fixture walkthrough**: inspect `A3_CBOM_EXAMPLE.json`; identify every `bom-ref` and verify `hybridComponents` resolution
2. **Schema drill**: validate a modified fixture against `A3_TEOS_CBOM_EXTENSION.schema.json`
3. **OpenAPI review**: trace each endpoint's security requirement and error mapping
4. **CBOM transform**: convert the flat `teos:*` map to the CycloneDX 1.6 `property` array form (pending official schema run — M2.2)
5. **Change-control simulation**: draft a change request for a hypothetical interface change and walk it through the approval matrix

## Target Audience and Review

- Audience: implementation engineers, QA, security reviewers, technical writers
- Materials reviewed for accuracy against the frozen A3 documentation package before use
- Materials must not speculate about or suggest insecure or live-crypto implementations

## Status

Framework/outline only. No live cryptographic operations, key generation, or QKD hardware integration is implied or authorized.