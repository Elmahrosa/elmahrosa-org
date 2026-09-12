# CBOM Schema Validation Report: Banking TLS Migration Scenario

**Subagent**: A1: CBOM Schema Validator  
**Date**: 2026-09-11  
**Scenario**: Banking TLS Migration  
**File Analyzed**: `modules/quantum-safe/teos-orchestration-layer/cbom-schema.md`

## Executive Summary

The CBOM schema demonstrates good coverage for Banking TLS Migration scenarios but has limitations in capturing complex dependency relationships, third-party library vulnerabilities, and detailed key usage contexts that are critical in banking environments. The schema needs enhancement to properly model banking-specific assets like HSM-protected keys, certificate chains, and legacy system dependencies.

## Scenario Context: Banking TLS Migration

Banking TLS migrations typically involve:
- Thousands of TLS certificates across customer-facing, internal, and API systems
- Mixed RSA/ECC certificates with varying key sizes (2048-bit RSA, 256-bit ECC, etc.)
- Certificates stored in various locations: load balancers, web servers, application servers, HSMs
- Legacy systems with hardcoded cryptographic implementations
- Third-party dependencies (payment processors, core banking systems)
- High-priority migration needs for customer-facing systems handling PII/financial data
- Complex certificate chains and trust stores
- Regulatory compliance requirements (PCI DSS, GDPR, SOX, etc.)

## Schema Validation Results

### ✅ Strengths

1. **Asset Identification Coverage**
   - ✅ `asset_id`: Unique identification for tracking individual certificates/keys
   - ✅ `name`: Human-readable asset description (e.g., "customer-portal-tls-cert")
   - ✅ `location`: File paths, HSM slots, or deployment locations
   - ✅ `asset_type`: Properly includes "certificate" and "key" types essential for TLS
   - ✅ `algorithm_family`: Captures RSA, ECDSA, etc. for cryptographic analysis
   - ✅ `key_size_bits`: Key strength assessment (critical for migration prioritization)
   - ✅ `usage`: Specific use cases (TLS server, TLS client, code signing, etc.)

2. **Migration Prioritization**
   - ✅ `classical_or_pq`: Distinguishes classical vs. post-quantum algorithms
   - ✅ `quantum_vulnerable`: Boolean flag for immediate vulnerability assessment
   - ✅ `migration_priority`: P0-P3 levels align with banking risk assessment needs
   - ✅ `crypto_agility_status`: Identifies hardcoded vs. configurable implementations

3. **Analysis & Reporting**
   - ✅ `gap_analysis`: Summary statistics for executive reporting
   - ✅ `blockers`: Identifies migration obstacles common in banking (hardcoded algorithms, lack of abstraction)
   - ✅ `compliance_refs`: Space for referencing banking regulations (PCI DSS, etc.)

### ⚠️ Limitations & Gaps

1. **Certificate Chain Modeling**
   - ❌ No mechanism to represent certificate trust chains (root → intermediate → leaf)
   - ❌ Banking environments rely heavily on proper chain validation
   - ❌ Missing fields: `issuer`, `subject`, `serial_number`, `validity_period`

2. **Key Storage & Protection Details**
   - ❌ No distinction between software keys, HSM-protected keys, or smart card keys
   - ❌ Critical for banking where HSM usage is common for private key protection
   - ❌ Missing field: `key_protection` (software/hsm/smartcard/etc.)

3. **Dependency & Relationship Mapping**
   - ❌ No way to represent which assets depend on others (e.g., application depends on specific TLS cert)
   - ❌ Missing fields: `dependencies`, `dependents`, `service_association`
   - ❌ Banking systems have complex interdependencies that affect migration sequencing

4. **Deployment Context**
   - ❌ Limited environment tracking (only dev/staging/production)
   - ❌ Missing: specific deployment targets (load balancer type, web server version, container orchestration)
   - ❌ Missing: `deployment_scale` (number of instances, geographic distribution)

5. **Third-Party & Supply Chain**
   - ❌ No explicit tracking of third-party library cryptographic usage
   - ❌ Banking relies on many third-party components (payment gateways, fraud detection)
   - ❌ Missing field: `source` (internal/third-party/vendor-name)

6. **Operational Metadata**
   - ❌ No renewal/expiration tracking automation hints
   - ❌ Missing: `auto_renewable`, `certificate_authority`, `key_rotation_frequency`
   - ❌ Important for banking operational planning

### 🟡 Partial Coverage

1. **Algorithm Representation**
   - ⚠️ `algorithm_family` as string is flexible but lacks standardization
   - ⚠️ Could benefit from enum or reference to standard identifiers (like NIST names)
   - ⚠️ No field for protocol version (TLS 1.0 vs 1.2 vs 1.3) which affects migration approach

2. **Notes Field Usage**
   - ⚠️ `notes` field is generic catch-all but unstructured
   - ⚠️ Banking-specific metadata would be better as structured fields

## Recommendations for Schema Enhancement

### Immediate Additions (Zero Breaking Change)
1. Add optional fields to `assets` objects:
   ```typescript
   issuer?: string;           // Certificate issuer
   subject?: string;          // Certificate subject
   serial_number?: string;    // Certificate serial number
   not_before?: string;       // Validity start (ISO8601)
   not_after?: string;        // Validity end (ISO8601)
   key_protection?: "software" | "hsm" | "smartcard" | "cloud-kms"; // Key storage type
   dependencies?: string[];   // Asset IDs this asset depends on
   source?: "internal" | "third-party"; // Origin of the asset
   ```

### Structured Enhancement (May Require Version Update)
1. Consider adding certificate-specific sub-schema:
   ```typescript
   certificate_details?: {
     chain_depth: number;
     trusted_roots: string[];
     ocsp_url?: string;
     crl_url?: string;
   };
   ```

2. Add banking-context fields:
   ```typescript
   sensitivity_level?: "public" | "internal" | "confidential" | "restricted"; // Data classification
   regulatory_frameworks?: string[]; // ["PCI-DSS", "GDDP", "SOX", etc.]
   customer_facing?: boolean;       // Whether asset serves external customers
   ```

## Validation Conclusion

The CBOM schema provides a solid foundation for cryptographic asset inventory and is **suitable for initial Banking TLS Migration scoping exercises**. It successfully captures the core elements needed to:
- Identify quantum-vulnerable TLS certificates and keys
- Prioritize migration based on vulnerability and sensitivity
- Document crypto-agility status for planning migration efforts
- Generate gap analysis reports for stakeholder communication

However, for **detailed migration planning and execution** in complex banking environments, the schema should be enhanced to better represent certificate chains, key protection mechanisms, third-party dependencies, and deployment-specific metadata.

**Recommendation**: Approve current schema for Phase 1 (discovery and gap analysis) while planning enhancements for Phase 2 (detailed migration planning and execution).

## Next Steps

1. Use current schema for initial CBOM generation in banking TLS discovery phase
2. Document limitations encountered during real-world implementation
3. Plan schema version 2.0 enhancements based on field experience
4. Consider extending schema with banking-specific extensions module

---
*Validation completed by Subagent A1: CBOM Schema Validator*