# M2.5 External Review Checklist - Teos Quantum-Safe Stack A3 Baseline

**Review Target**: Tag `qss-a3-locked` (commit 3877cfb)  
**Review Type**: Cryptographic engineering and security validation  
**Prerequisites**: 
- ✅ Founder sign-off received (A3_FOUNDER_SIGN_OFF.md signed 2026-09-13)
- ✅ A3 contract locked as `qss-a3-locked`
- ✅ No live cryptographic operations (all stubs return `TeosError::NotImplemented`)
- ✅ Phase 1 interface-only foundation validated

## 📋 Review Scope
Review the Teos Quantum-Safe Stack A3 specification artifacts for:
- Standards alignment and accuracy
- Interface clarity and implementability
- Security and privacy considerations
- Compliance mapping correctness
- Documentation quality and consistency

## ✅ Review Checklist

### 1. Foundational Documents
| Item | Status | Notes/Evidence |
|------|:------:|----------------|
| A3_FOUNDER_SIGN_OFF.md signed and dated | [ ] | Verify signature and date (2026-09-13) |
| Tag `qss-a3-locked` exists and points to correct commit | [ ] | Verify git tag and commit 3877cfb |
| No live crypto confirmed (all stubs NOT_IMPLEMENTED) | [ ] | Spot-check module implementations |
| A2 contract integrity verified (COMMON-CONTRACT.md) | [ ] | Check for NOT_IMPLEMENTED and Result<T,TeosError> |

### 2. Module Interface Specifications
| Module | Item | Status | Notes/Evidence |
|--------|------|:------:|----------------|
| **Teos-PQC** | FIPS 203/204/205 alignment (ML-KEM/ML-DSA/SLH-DSA) | [ ] | Check parameter sets and function signatures |
|  | KEM vs signature distinction clear | [ ] | Verify keypair/encapsulate/decapsulate vs sign/verify |
|  | Legacy aliases accepted but not preferred | [ ] | Check teos-common Params enum |
|  | Function signatures match COMMON-CONTRACT.md | [ ] | Verify Result<T,TeosError> usage |
| **Teos-QKD** | Explicit statement: QKD not NIST-standardized | [ ] | Verify in README |
|  | FIPS 204 (ML-DSA) required for classical auth | [ ] | Check authenticate_channel signature |
|  | References to SP 1800-38, ETSI/ITU QKD standards | [ ] | Validate standards citations |
|  | AuthToken contains session ID | [ ] | Check struct definition |
| **Teos-QRNG** | SP 800-90B/C requirements correctly specified | [ ] | Verify health_test, get_entropy, continuous_validation |
|  | Startup test: ≥1024 samples RCT/APT | [ ] | Check health_test() documentation |
|  | Entropy output conditioned via vetted functions | [ ] | Review entropy requirements section |
|  | Consumption via DRBG only (never raw source) | [ ] | Verify documentation constraints |
| **Teos-Orchestration** | SP 800-57 Pt 3 key management alignment | [ ] | Check register_algorithm, rotate_key |
|  | cbom_snapshot() returns CBOM_Document | [ ] | Validate interface contract |
|  | Algorithm agility tracking (FIPS 203/204/205) | [ ] | Verify metadata fields |
|  | Key lifecycle management interfaces clear | [ ] | Review rotation and registration |

### 3. Shared Components & Conventions
| Item | Status | Notes/Evidence |
|------|:------:|----------------|
| COMMON-CONTRACT.md defines Result<T,TeosError> | [ ] | Check error model |
| TeosError includes NOT_IMPLEMENTED | [ ] | Verify enum values |
| FIPS-named strings used for params | [ ] | Check Params enum |
| Legacy aliases handled in FromStr impl | [ ] | Verify teos-common |
| Secret zeroization requirement documented | [ ] | Check COMMON-CONTRACT.md |
| No exceptions - only Result<T,TeosError> | [ ] | Verify all functions |

### 4. CBOM Specification & API
| Item | Status | Notes/Evidence |
|------|:------:|----------------|
| A3_CBOM_SCHEMA_SPEC.md maps to CycloneDX 1.6 | [ ] | Validate mapping document |
| Teos extension properly namespaced (teos:) | [ ] | Check schema and examples |
| Hybrid algorithms via composition linkage | [ ] | Verify no native field modification |
| A3_CBOM_EXAMPLE.json valid JSON fixture | [ ] | Spot-check structure |
| A3_CBOM_EXAMPLE.cyclonedx-valid.json validates | [ ] | Confirm schema validation |
| A3_CBOM_API_OPENAPI.yaml validates (Redocly 0 errors) | [ ] | Note: Redocly validation required |
| API endpoints secured with mTLS/OAuth2 | [ ] | Check security schemes |
| Error responses map to TeosError enum | [ ] | Validate responses section |
| Examples illustrate usage and error cases | [ ] | Review API spec examples |
| Idempotency considerations documented | [ ] | Check for Idempotency-Key discussion |
| Tenant scoping and authorization model specified | [ ] | Review OpenAPI spec |

### 5. Security & Privacy Specifications
| Item | Status | Notes/Evidence |
|------|:------:|----------------|
| A3_AUDIT_TRAIL_SPEC.md defines hash-chained append-only | [ ] | Verify SHA-256 and genesis record |
| Audit events cover all significant operations | [ ] | Check event types |
| Aligns with NIST SP 800-57 Pt 3 | [ ] | Verify lifecycle state mappings |
| A3_ACCESS_CONTROL_POLICY.md defines mTLS/OAuth2 | [ ] | Verify auth methods |
| RBAC/ABAC model clearly specified | [ ] | Check role/scope definitions |
| Graduated redaction policy documented | [ ] | Verify redaction levels |
| Access decisions generate audit events | [ ] | Verify logging requirements |
| No secrets/logging of sensitive data | [ ] | Confirm zeroization requirements |

### 6. Validation & Process Documents
| Item | Status | Notes/Evidence |
|------|:------:|----------------|
| A3_VALIDATION_REPORT.md reflects current state | [ ] | Check mechanical validation results |
| A3_READINESS_REVIEW.md criteria accurate | [ ] | Verify status against evidence |
| A3_CHANGE_CONTROL_PROCESS.md defined | [ ] | Check change categories and gates |
| A2 re-validation gate documented | [ ] | Verify A2 re-validation requirement |
| Founder re-approval requirement documented | [ ] | Verify for baseline changes |
| Documentation package index complete | [ ] | Verify A3_DOCUMENTATION_PACKAGE_INDEX.md |

### 7. Cross-Document Consistency
| Check | Status | Notes/Evidence |
|-------|:------:|----------------|
| Function signatures match across docs | [ ] | Compare READMEs, OpenAPI, impl |
| Error codes consistent (TeosError values) | [ ] | Verify enum usage |
| Standards references accurate and non-misleading | [ ] | Spot-check NIST citations |
| No forbidden identifiers (TEOS_PQC_, hodos-pqc) | [ ] | grep verification |
| Legacy algorithm aliases only in COMMON-CONTRACT | [ ] | Check for kyber/dilithium preferences |
| QKD non-NIST status consistently stated | [ ] | Verify all references |
| SP 800-90B/C correctly referenced for QRNG | [ ] | Validate citations |
| SP 800-57 Pt 3 correctly referenced for orchestration | [ ] | Validate citations |
| FIPS 203/204/205 correctly referenced for PQC | [ ] | Validate citations |

## 📝 Review Process & Criteria

### Reviewer Qualifications
- Cryptographic engineering expertise (PQC, QKD, or related)
- Security standards knowledge (NIST, ISO, etc.)
- Experience with API specifications and CBOM formats
- Familiarity with quantum-safe migration requirements

### Review Duration
- Recommended: 3-5 business days for thorough review
- Extension possible for complex feedback

### Feedback Disposition
All feedback must be categorized as:
- **ACCEPTED**: Incorporated into specifications
- **REJECTED**: Not incorporated with justification
- **DEFERRED**: Considered for future version with rationale

### Documentation of Review
- Create `A3_FEEDBACK_AND_RESPONSES.md` to record:
  - Reviewer qualifications and engagement dates
  - All feedback items with categorization
  - Disposition rationale for each item
  - Updated specification references (if accepted)

## ✅ Sign-off Criteria
The M2.5 external review is complete when:
1. [ ] All checklist items reviewed and status updated
2. [ ] Feedback collected and documented in A3_FEEDBACK_AND_RESPONSES.md
3. [ ] All critical feedback addressed (accepted or justified rejection)
4. [ ] No outstanding blocking issues from qualified reviewers
5. [ ] Review findings and disposition recorded

## 🔗 Reference Links
- **Baseline**: `git checkout qss-a3-locked`
- **Founder Sign-off**: `docs/quantum-safe-stack/A3_FOUNDER_SIGN_OFF.md`
- **Package Index**: `docs/quantum-safe-stack/A3_DOCUMENTATION_PACKAGE_INDEX.md`
- **Validation Report**: `docs/quantum-safe-stack/A3_VALIDATION_REPORT.md`
- **Change Control**: `docs/quantum-safe-stack/A3_CHANGE_CONTROL_PROCESS.md`