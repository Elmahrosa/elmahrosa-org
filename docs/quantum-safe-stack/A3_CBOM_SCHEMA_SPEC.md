# Teos Quantum-Safe CBOM Schema Specification

## Overview

This document specifies how the Teos Quantum-Safe Orchestration Layer maps its internal CBOM representation to the [CycloneDX 1.6](https://cyclonedx.org/schema/) schema for Cryptographic Bills of Materials (CBOM). The Teos CBOM extends the standard CycloneDX 1.6 format with quantum-specific fields while maintaining backward compatibility and schema validity.

## CycloneDX 1.6 Baseline

The Teos CBOM uses CycloneDX 1.6 JSON as its baseline format, specifically leveraging the `cryptographic-asset` component type introduced in CycloneDX 1.4 and enhanced in 1.6 for PQC readiness.

## Teos Extension Namespace

To maintain CycloneDX 1.6 validity while extending functionality, Teos uses the following extension mechanism:

- **Extension namespace**: `http://schemas.teos.example.com/cbom/1.0`
- **Extension prefix**: `teos`
- All Teos-specific fields appear under this namespace in the XML format or as prefixed properties in JSON

## Core Mapping: Teos CBOM → CycloneDX 1.6

### Root Level Fields

| Teos CBOM Field | CycloneDX 1.6 Mapping | Notes |
|----------------|----------------------|-------|
| `cbom_version` | `metadata.component.version` | Maps to the component version in CycloneDX metadata |
| `generated_at` | `metadata.timestamp` | ISO 8601 timestamp as per CycloneDX specification |
| `scope.repo` | `metadata.component.group` | Repository/project identifier |
| `scope.component` | `metadata.component.name` | Component/subsystem identifier |
| `scope.environment` | `properties.teos:environment` | Extension field for deployment environment |

### Assets Array → Components

Each asset in the Teos `assets` array maps to a `component` of type `cryptographic-asset` in CycloneDX 1.6:

| Teos Asset Field | CycloneDX 1.6 Mapping | Notes |
|------------------|----------------------|-------|
| `asset_id` | `bom-ref` | Unique reference identifier |
| `asset_type` | `type` | Mapped according to the table below |
| `name` | `name` | Human-readable name |
| `location` | `properties.teos:location` | Extension field |
| `classical_or_pq` | `properties.teos:classicalOrPq` | Extension field |
| `algorithm_family` | `properties.teos:algorithmFamily` | Extension field |
| `key_size_bits` | `properties.teos:keySizeBits` | Extension field |
| `usage` | `properties.teos:usage` | Extension field |
| `crypto_agility_status` | `properties.teos:cryptoAgilityStatus` | Extension field |
| `quantum_vulnerable` | `properties.teos:quantumVulnerable` | Extension field |
| `migration_priority` | `properties.teos:migrationPriority` | Extension field |
| `notes` | `description` | Standard CycloneDX description field |

#### Asset Type Mapping

| Teos `asset_type` | CycloneDX `type` | Notes |
|-------------------|------------------|-------|
| `algorithm` | `cryptographic-asset` | General cryptographic algorithm |
| `key` | `cryptographic-asset` | Cryptographic key material |
| `certificate` | `cryptographic-asset` | X.509 or similar certificate |
| `library` | `cryptographic-asset` | Cryptographic software library |
| `protocol` | `cryptographic-asset` | Cryptographic protocol implementation |

### Gap Analysis

The Teos `gap_analysis` object maps to CycloneDX properties:

| Teos Gap Analysis Field | CycloneDX 1.6 Mapping | Notes |
|-------------------------|----------------------|-------|
| `total_assets_scanned` | `properties.teos:totalAssetsScanned` | Extension field |
| `quantum_vulnerable_count` | `properties.teos:quantumVulnerableCount` | Extension field |
| `migration_ready_count` | `properties.teos:migrationReadyCount` | Extension field |
| `blockers` | `properties.teos:blockers` | Extension field array |

Each blocker in the array maps to an object with:
- `asset_id` → `properties.teos:blockers[].assetId`
- `blocker_type` → `properties.teos:blockers[].blockerType`
- `description` → `properties.teos:blockers[].description`
- `remediation_suggestion` → `properties.teos:blockers[].remediationSuggestion`

### Compliance References

The Teos `compliance_refs` object maps to CycloneDX properties:

| Teos Compliance Field | CycloneDX 1.6 Mapping | Notes |
|-----------------------|----------------------|-------|
| `nist_pqc_standards` | `properties.teos:nistPqcStandards` | Extension field array |
| `framework` | `properties.teos:framework` | Extension field |

## Quantum-Specific Extensions

### Hybrid Algorithm Representation

Per founder decision D2, hybrid algorithms (combining classical and PQC for migration) are represented through composition linkage:

1. **Primary asset**: Represents the dominant algorithm (e.g., the PQC component)
2. **Composition relationship**: Uses CycloneDX's `components` relationship mechanism
3. **Extension property**: `teos:hybridComponents` array listing subordinate asset references

Example hybrid asset (X25519+ML-KEM-768 for TLS key exchange):
```json
{
  "bom-ref": "tls-key-exchange-001",
  "type": "cryptographic-asset",
  "name": "TLS 1.3 Hybrid Key Exchange",
  "properties": {
    "teos:algorithmFamily": "X25519+ML-KEM-768",
    "teos:classicalOrPq": "hybrid",
    "teos:keySizeBits": 256,
    "teos:usage": "TLS 1.3 key exchange",
    "teos:cryptoAgilityStatus": "abstracted",
    "teos:quantumVulnerable": false,
    "teos:migrationPriority": "P3",
    "teos:hybridComponents": [
      "x25519-key-exchange-001",
      "ml-kem-768-key-exchange-001"
    ]
  }
}
```

Where the component assets would be:
```json
{
  "bom-ref": "x25519-key-exchange-001",
  "type": "cryptographic-asset",
  "name": "X25519 Key Exchange",
  "properties": {
    "teos:algorithmFamily": "X25519",
    "teos:classicalOrPq": "classical",
    // ... other properties
  }
}
{
  "bom-ref": "ml-kem-768-key-exchange-001",
  "type": "cryptographic-asset",
  "name": "ML-KEM-768 Key Exchange",
  "properties": {
    "teos:algorithmFamily": "ML-KEM-768",
    "teos:classicalOrPq": "post-quantum",
    // ... other properties
  }
}
```

### NISTIR 8547 Transition Metadata

Per the founder guidance, NISTIR 8547 transition/deprecation planning is included as metadata:

| Teos Field | CycloneDX 1.6 Mapping | Notes |
|------------|----------------------|-------|
| Algorithm deprecation timeline | `properties.teos:deprecationTimeline` | Extension field array |
| Each timeline entry includes: | | |
| - algorithm | `properties.teos:deprecationTimeline[].algorithm` | FIPS identifier |
| - status | `properties.teos:deprecationTimeline[].status` | e.g., "deprecated", "disallowed" |
| - effectiveDate | `properties.teos:deprecationTimeline[].effectiveDate` | ISO 8601 date |
| - source | `properties.teos:deprecationTimeline[].source` | e.g., "NISTIR 8547", "NSA CNSA 2.0" |
| - confidence | `properties.teos:deprecationTimeline[].confidence` | "high", "medium", "low" |

Example:
```json
"properties": {
  "teos:deprecationTimeline": [
    {
      "algorithm": "RSA-2048",
      "status": "deprecated",
      "effectiveDate": "2030-01-01",
      "source": "NISTIR 8547",
      "confidence": "medium"
    }
  ]
}
```

## Schema Validation

The Teos CBOM uses a flat, namespaced `teos:*` property map for the internal representation (see `A3_TEOS_CBOM_EXTENSION.schema.json` for validation of those fields). CycloneDX 1.6 represents custom properties as an array of `{"name", "value"}` objects, so schema-level validation against the official CycloneDX 1.6 JSON schema requires transforming each `teos:*` key in that map to the standard `property` array form. The internal flat representation is documented for readability and is not asserted to pass CycloneDX 1.6 schema validation as-is; the official schema run is performed during validation (see `A3_VALIDATION_REPORT.md`).

## Example CBOM Snippet

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "version": 1,
  "metadata": {
    "timestamp": "2026-09-12T10:30:00Z",
    "component": {
      "group": "elmahrosa-org",
      "name": "teos-orchestration-layer",
      "version": "1.0"
    }
  },
  "components": [
    {
      "bom-ref": "tls-server-cert-001",
      "type": "cryptographic-asset",
      "name": "TLS Server Certificate",
      "properties": {
        "teos:location": "/etc/ssl/certs/server-cert.pem",
        "teos:algorithmFamily": "X25519+ML-KEM-768",
        "teos:classicalOrPq": "hybrid",
        "teos:keySizeBits": 256,
        "teos:usage": "TLS 1.3 key exchange",
        "teos:cryptoAgilityStatus": "abstracted",
        "teos:quantumVulnerable": false,
        "teos:migrationPriority": "P3",
        "teos:hybridComponents": [
          "x25519-key-exchange-001",
          "ml-kem-768-key-exchange-001"
        ]
      }
    },
    {
      "bom-ref": "x25519-key-exchange-001",
      "type": "cryptographic-asset",
      "name": "X25519 Key Exchange",
      "properties": {
        "teos:location": "software-library:libtls-1.3",
        "teos:algorithmFamily": "X25519",
        "teos:classicalOrPq": "classical",
        "teos:keySizeBits": 256,
        "teos:usage": "TLS 1.3 key exchange",
        "teos:cryptoAgilityStatus": "hardcoded",
        "teos:quantumVulnerable": true,
        "teos:migrationPriority": "P0"
      }
    },
    {
      "bom-ref": "ml-kem-768-key-exchange-001",
      "type": "cryptographic-asset",
      "name": "ML-KEM-768 Key Exchange",
      "properties": {
        "teos:location": "software-library:liboqs-kyber768",
        "teos:algorithmFamily": "ML-KEM-768",
        "teos:classicalOrPq": "post-quantum",
        "teos:keySizeBits": 256,
        "teos:usage": "TLS 1.3 key exchange",
        "teos:cryptoAgilityStatus": "abstracted",
        "teos:quantumVulnerable": false,
        "teos:migrationPriority": "P3"
      }
    }
  ],
  "properties": {
    "teos:environment": "production",
    "teos:totalAssetsScanned": 3,
    "teos:quantumVulnerableCount": 1,
    "teos:migrationReadyCount": 2,
    "teos:nistPqcStandards": [
      "ML-KEM-768",
      "ML-DSA-65",
      "SLH-DSA-SHA2-128s"
    ],
    "teos:framework": "NIST SP 1800-38"
  }
}
```