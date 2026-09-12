# Teos-Orchestration-Layer Module

## Interface Definition
(Stub - no live implementation)

This module defines the unified orchestration layer for quantum-safe security, including CBOM generation, gap analysis, and unified management of QRNG, QKD, PQC, and key lifecycle.

## Interface Contract
- `register_algorithm(fips_id, impl) -> handle`: Register a PQC implementation (e.g., FIPS 203 ML-KEM-768) and return a handle for later use.
- `rotate_key(key_id, new_algo) -> key_id'`: Rotate a cryptographic key to a new algorithm (or parameter set), returning the new key identifier.
- `cbom_snapshot() -> CBOM_Document`: Generate a Cryptographic Bill of Materials snapshot compliant with the CBOM schema (see ./cbom-schema.md).

## Common Contract Conventions
See [COMMON-CONTRACT.md](../COMMON-CONTRACT.md)