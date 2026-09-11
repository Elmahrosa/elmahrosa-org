# CBOM (Cryptographic Bill of Materials) Schema

This document defines the schema for a Cryptographic Bill of Materials (CBOM) used in the Teos Quantum-Safe Orchestration Layer module for gap analysis.

## TypeScript Interface

```typescript
interface CBOM {
  cbom_version: string;
  generated_at: string; // ISO8601 timestamp
  scope: {
    repo: string;
    component: string;
    environment: "dev" | "staging" | "production";
  };
  assets: {
    asset_id: string;
    asset_type: "algorithm" | "key" | "certificate" | "library" | "protocol";
    name: string;
    location: string;
    classical_or_pq: "classical" | "post-quantum" | "hybrid";
    algorithm_family: string;
    key_size_bits: number | null;
    usage: string;
    crypto_agility_status: "hardcoded" | "configurable" | "abstracted";
    quantum_vulnerable: boolean;
    migration_priority: "P0" | "P1" | "P2" | "P3";
    notes: string;
  }[];
  gap_analysis: {
    total_assets_scanned: number;
    quantum_vulnerable_count: number;
    migration_ready_count: number;
    blockers: {
      asset_id: string;
      blocker_type: "hardcoded_algorithm" | "no_abstraction_layer" | "third_party_dependency" | "unknown";
      description: string;
      remediation_suggestion: string;
    }[];
  };
  compliance_refs: {
    nist_pqc_standards: string[]; // e.g. ["ML-KEM", "ML-DSA", "SLH-DSA"]
    framework: string | null;
  };
}
```

## Migration Priority Levels

- **P0**: quantum-vulnerable, in production, handles sensitive data — migrate first
- **P1**: quantum-vulnerable, in production, lower sensitivity
- **P2**: quantum-vulnerable, not yet in production
- **P3**: already crypto-agile or already PQC — monitor only

## Status

- This is a SCHEMA + DOCUMENTATION stub only.
- No scanning tool, no CBOM auto-generation logic, no execution against real repos/keys in this pass.
- Flag before building the actual scanner — that's a separate scoped task requiring its own review (repo access scope, what gets flagged as "sensitive," false-positive handling).
