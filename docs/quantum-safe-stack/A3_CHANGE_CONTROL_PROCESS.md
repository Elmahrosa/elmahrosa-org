# Change Control Process — Quantum-Safe Stack Interfaces

> Applies to all A2-validated interfaces and the A3 interface/documentation package. A2 contracts are immutable founding interfaces; any modification is a controlled change, not an edit.

## Scope

This process governs changes to:

- A2-validated interface contracts (function signatures, error model, data formats) in `modules/quantum-safe/COMMON-CONTRACT.md`
- Module READMEs that document those contracts (`teos-qkd`, `teos-qrng`, `teos-pqc`, `teos-orchestration-layer`)
- A3 specification documents (`A3_CBOM_SCHEMA_SPEC.md`, `A3_CBOM_API_OPENAPI.yaml`, `A3_AUDIT_TRAIL_SPEC.md`, `A3_ACCESS_CONTROL_POLICY.md`, `A3_CBOM_EXAMPLE.json`, `A3_TEOS_CBOM_EXTENSION.schema.json`)

## Guiding Principles

1. **Interface-First**: All work remains interface/documentation only. No live crypto, key generation, or QKD hardware changes enter through this process.
2. **Immutability**: A2-validated contracts are treated as immutable foundations.
3. **Traceability**: Every change has a documented request, impact analysis, and disposition.
4. **Re-validation**: Interface changes require A2 re-validation before they take effect.
5. **Founder Approval**: Security-critical and interface-affecting changes require founder approval.

## Change Categories

| Category | Examples | Re-validation | Founder Approval |
|----------|----------|---------------|------------------|
| **Documentation-only** | Clarifying prose, fixing typographical error, adding examples | Not required | No |
| **Interface-affecting** | Changing a function signature, adding/removing an error code, altering a data format or field | Required (A2 re-validation) | Required |
| **Security-critical** | Altering audit trail semantics, access control scopes, redaction levels, key lifecycle state machine | Required (A2 re-validation) | Required |
| **Standards-alignment** | Updating NIST/ISO/GDPR references, FIPS parameter set naming | Required if it changes a contract; DOCUMENTED anyway | Recommended |
| **TEOS-extension** | Adding/modifying Teos extension properties in CBOM schema (teos:* properties) | Required if it changes A3 schema; DOCUMENTED anyway | Required if changes affect validation gate criteria |

## Process

1. **Submit Change Request (CR)**
   - Description of the change and its business/technical rationale
   - Categorization per the table above
   - Reference to the affected A2 contract or A3 artifact
   - For TEOS-extension changes: specify which teos:* properties are affected

2. **Impact Analysis and Risk Assessment**
   - Affected interfaces and dependent modules/components
   - Compatibility impact (breaking vs. non-breaking)
   - Security implications (confidentiality, integrity, availability, auditability)
   - Compliance impact (NIST, ISO, PCI DSS, HIPAA, GDPR)
   - For TEOS-extension changes: impact on CBOM validation and gap analysis capabilities

3. **Review**
   - Technical review of the proposed change against the existing contract
   - For interface-affecting or security-critical changes: A2 re-validation is triggered
   - For TEOS-extension changes: CycloneDX 1.6 validation is verified (extensions treated as custom properties)

4. **Approval**
   - Documentation-only: approver is the responsible technical lead
   - Interface-affecting and security-critical: founder approval required
   - TEOS-extension: founder approval required if changes affect A3 validation gate criteria

5. **Implementation**
   - Change applied to contracts, module READMEs, and affected A3 artifacts in one atomic change
   - Artifacts updated in lockstep to avoid drift (e.g., OpenAPI, JSON Schema, fixture, spec mapping)
   - TEOS-extension changes require synchronized updates to:
     * A3_CBOM_SCHEMA_SPEC.md (mapping document)
     * A3_TEOS_CBOM_EXTENSION.schema.json (JSON Schema)
     * A3_CBOM_EXAMPLE.json (fixture)
     * A3_CBOM_EXAMPLE.cyclonedx-valid.json (validated transform)
     * teos-orchestration-layer/cbom-schema.md (TypeScript schema)

6. **Recording**
   - CR logged with decision, rationale, approvals, and effective date
   - Validation result attached for re-validated changes
   - For TEOS-extension changes: CycloneDX 1.6 validation report attached

## Validation Gate for Interface Changes

A2 re-validation must confirm at minimum:

- No reintroduction of `hodos-pqc` or C-style `TEOS_PQC_OK`/`TEOS_PQC_ERR_*` identifiers in `docs/` or `modules/`
- `Result<T, TeosError>` remains the sole error model with `NOT_IMPLEMENTED` preserved in `TeosError`
- FIPS designations use approved NIST parameter set names (ML-KEM-768, ML-DSA-65, SLH-DSA-SHA2-128s)
- QKD classical-channel authentication retains the ML-DSA (FIPS 204) requirement
- QRNG entropy remains validated to SP 800-90B/C and consumed via DRBG (never raw)

## TEOS-Extension Validation Gate

For changes affecting the Teos extension properties in the CBOM schema:

- CBOM schema validates against CycloneDX 1.6 JSON schema when Teos extensions are treated as custom properties
- Hybrid algorithm representation through composition linkage is properly specified
- All required teos:* properties from A3_TEOS_CBOM_EXTENSION.schema.json are present in the mapping
- The fixture (A3_CBOM_EXAMPLE.json) validates against both the Teos extension schema and CycloneDX 1.6 (with extensions as custom properties)

## Integration with Development Workflow

- Changes land as single atomic commits with the CR reference in the commit message
- CI audit workflow (`.github/workflows/audit.yml`) runs the forbidden-term and interface checks on the committed state
- TEOS-extension changes trigger additional validation:
  - JSON Schema validation for A3_TEOS_CBOM_EXTENSION.schema.json
  - CycloneDX 1.6 validation via ajv-cli (extensions as custom properties)
  - Fixture validation against both schemas
- No stray files (`.bak`, editor artifacts) are committed; `*.bak` is gitignored

## Status

Interface-only process documentation. No live cryptographic operations, key generation, or QKD hardware integration is implied or authorized by this document.