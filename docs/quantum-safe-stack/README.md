# Quantum-Safe Stack — Reviewer Entry Point

Status: A3 LOCKED · tag qss-a3-locked.  
Baseline commit: 72217ed · Lock tag (on signature): qss-a3-locked  
Live cryptography: None. Every module is an interface stub returning NOT_IMPLEMENTED.

## What this is
Interface-only scaffolding and specification for a quantum-safe security stack  
(PQC, QKD, QRNG, orchestration/CBOM), aligned to NIST FIPS 203/204/205 and  
validated against CycloneDX 1.6. No secrets, keys, or entropy are generated anywhere.

## Modules (modules/quantum-safe/)
| Module | Standards anchor | Contract |
|---|---|---|
| teos-pqc | FIPS 203 ML-KEM, 204 ML-DSA, 205 SLH-DSA | keypair / encapsulate / decapsulate / sign / verify |
| teos-qkd | SP 1800-38, ETSI/ITU QKD; FIPS 204 for channel auth (QKD is not NIST-standardized) | authenticate_channel / exchange_key |
| teos-qrng | SP 800-90B/C (validation pending, CMVP path) | health_test / get_entropy / continuous_validation |
| teos-orchestration-layer | SP 800-57 Pt 3; FIPS 203/204/205 tracking | register_algorithm / rotate_key / cbom_snapshot |

Shared conventions: COMMON-CONTRACT.md — Result, FIPS parameter  
names, byte-length rules, secret zeroization. All four modules use this contract.

## Gate history (docs/quantum-safe-stack/)
A2 — NIST interface contract review: BLOCKED (4 issues) → fixed → PASS  
   Evidence: A2_NIST_INTERFACE_CONTRACT_VALIDATION_REPORT.md → A2_NIST_INTERFACE_CONTRACT_REVALIDATION_REPORT.md
A3 — CBOM API & schema: OpenAPI 3.1 (Redocly, 0 errors); CBOM fixture  
   VALID against pinned CycloneDX 1.6 via ajv-cli; Teos extensions declared in  
   namespace (hybrids via composition linkage, not a native field); NISTIR 8547  
   material source-qualified, not presented as deprecation dates.
Governance (open): M2.5 external review.

## Founder decisions:
- D1 native CycloneDX 1.6
- D2 hybrid composition linkage  
- D3 append-only SP 800-57 audit events

## Reading order for reviewers
1. A2_NIST_INTERFACE_CONTRACT_REVALIDATION_REPORT.md
2. A3_VALIDATION_REPORT.md → A3_CBOM_SCHEMA_SPEC.md → A3_CBOM_API_OPENAPI.yaml
3. A3_AUDIT_TRAIL_SPEC.md, A3_ACCESS_CONTROL_POLICY.md
4. A3_CHANGE_CONTROL_PROCESS.md — any change to A2 contracts or the locked  
   A3 schema requires A2 re-validation → founder re-approval.

## Known open enhancement: 
Rate-limit headers / 429 body (non-blocking).

## When you sign and push:
Change only the first status line to:  
**Status: A3 LOCKED · tag qss-a3-locked.**