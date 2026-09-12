# Implementation Guidance — Quantum-Safe Stack Interfaces

Implementation guidance for qualified cryptographic engineering teams consuming the A3 interface/documentation package. This document is guidance only; the authoritative contracts are the A2-validated module READMEs and `modules/quantum-safe/COMMON-CONTRACT.md`.

## Hard Constraints

- **Interface-only**: No live cryptographic operations, key generation, or QKD hardware integration in this effort. Interfaces are implemented at the stub level returning `NOT_IMPLEMENTED` until separately scoped and approved.
- **Error model**: All functions return `Result<T, TeosError>`; no exceptions. `TeosError ∈ { NOT_IMPLEMENTED, INVALID_PARAM, UNSUPPORTED_ALGO, AUTH_FAIL, KEY_NOT_FOUND, ... }` per `COMMON-CONTRACT.md`.
- **FIPS naming**: Algorithms must be identified by approved NIST parameter sets (ML-KEM-768, ML-DSA-65, SLH-DSA-SHA2-128s). Legacy aliases may be accepted but never preferred (see roadmap MPQC.4).
- **No secrets in fixtures**: Never commit private keys, shared secrets, or raw entropy (checked in `PRE_SIGNATURE_CHECKLIST.md` Check 4 and CI).

## Interface Conventions

- **QKD** (`teos-qkd`): `authenticate_channel(peer_id, local_sk, peer_pk) -> Result<AuthToken>` must use ML-DSA (FIPS 204) for classical-channel authentication. `exchange_key() -> Result<SharedSecret>` per A2. QKD is not NIST-standardized; document accordingly.
- **QRNG** (`teos-qrng`): `health_test()` (≥1024-sample startup test), `get_entropy()` (conditioned output, declared min-entropy), `continuous_validation()` (RCT+APT). Entropy is validated to NIST SP 800-90B/C and consumed via SP 800-90A DRBG — never raw source.
- **PQC** (`teos-pqc`): `keypair()`, `encapsulate()`, `decapsulate()`, `sign()`, `verify()`. Keep the KEM vs. signature distinction explicit (roadmap MPQC.2). Parameter sets are specified with FIPS-named strings.
- **Orchestration** (`teos-orchestration-layer`): `register_algorithm() -> Result<Handle>`, `rotate_key() -> Result<KeyId>`, `cbom_snapshot() -> Result<CBOM_Document>`. All reference `COMMON-CONTRACT.md`.

## CBOM (CycloneDX 1.6 + Teos extension)

- The internal representation uses a flat, namespaced `teos:*` property map validated by `A3_TEOS_CBOM_EXTENSION.schema.json`.
- CycloneDX 1.6 expresses custom properties as an array of `{"name", "value"}` objects; transform each `teos:*` key to that array form for official-schema validation (see `A3_CBOM_SCHEMA_SPEC.md` §Schema Validation).
- Enumerations are canonical: `cryptoAgilityStatus ∈ {abstracted, hardcoded, agile, legacy}`, `classicalOrPq ∈ {classical, post-quantum, hybrid}`, `migrationPriority ∈ {P0..P3}`, `keySizeBits` integer ≥ 0.
- Hybrid algorithms are represented by composition linkage via `teos:hybridComponents` referencing subordinate `bom-ref` values. Every `bom-ref` must be unique and resolvable.
- Redaction: public keys and identifiers (asset_id, name, algorithm_family) are never redacted; sensitive fields follow the four-level graduated redaction policy in `A3_ACCESS_CONTROL_POLICY.md`.

## Audit Trail Integration

- Audit events must be append-only / write-once, SHA-256 hash-chained with monotonic `sequence_number` starting at 1 and `previous_event_hash` linkage (genesis `previous_event_hash: null`).
- State-changing operations (registration, rotation, snapshot, denied access) emit defined event types with lifecycle states mapped to NIST SP 800-57 Part 3.
- API security: OAuth 2.0 scopes `{cbom.read, cbom.write, cbom.audit, cbom.admin}` and/or mTLS per endpoint security requirements in `A3_CBOM_API_OPENAPI.yaml`.

## Change Control

- Do not modify A2-validated contracts outside the process in `A3_CHANGE_CONTROL_PROCESS.md`. Documentation-only fixes are allowed; interface-affecting and security-critical changes require A2 re-validation and founder approval.
- Changes land as single atomic commits with the change-request referenced in the commit message.

## Production Readiness Notes (non-normative, post-Phase 1)

The following are recommendations for a separately scoped production implementation. They are guidance only; they do not alter A2 contracts or the locked A3 schema.

- **Secrets handling**: Implementations that later introduce real keys or entropy must use a managed secrets store (e.g., HashiCorp Vault, AWS Secrets Manager) with environment-driven configuration. Never commit private keys, shared secrets, or raw entropy; keep fixtures synthetic as enforced by `PRE_SIGNATURE_CHECKLIST.md` Check 4.
- **Observability**: Emit structured audit events per `A3_AUDIT_TRAIL_SPEC.md` (append-only, SHA-256 hash-chained) plus operational metrics, health checks, and alerting endpoints for monitoring integration (e.g., Grafana). Keep cryptographically protected audit trails distinct from general-purpose logs.
- **Connector / integration patterns**: When wiring external connectors (CRM, email, storage), define adapter interfaces that preserve the `Result<T, TeosError>` error model and honor the OAuth 2.0 / mTLS boundary (`cbom.read/write/audit/admin`) from `A3_CBOM_API_OPENAPI.yaml`.
- **CI/CD**: Enforce contract tests, forbidden-term checks, and coverage gates on module implementations per the integration notes in `A3_CHANGE_CONTROL_PROCESS.md`.

## Status

Guidance document for the interface-only implementation effort. No live cryptographic operations, key generation, or QKD hardware integration is implied or authorized by this document.