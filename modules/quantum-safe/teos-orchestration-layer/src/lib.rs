//! Teos-Orchestration-Layer — unified management and CBOM interface stub.
//!
//! Interface-only implementation of
//! [`modules/quantum-safe/teos-orchestration-layer/README.md`](../../README.md).
//! All operations are stubs returning [`TeosError::NotImplemented`]; no CBOM
//! scanning, key rotation, or algorithm registration state is maintained.
//!
//! Extends the standard CycloneDX 1.6 baseline with Teos extension properties;
//! see `A3_CBOM_SCHEMA_SPEC.md` and this module's `cbom-schema.md`.

use teos_common::{TeosError, TeosResult};

/// Handle returned by `register_algorithm` for later reference.
pub type Handle = String;

/// Key identifier returned by `rotate_key`.
pub type KeyId = String;

/// Minimal CBOM document shape returned by `cbom_snapshot`. Mirrors the
/// CycloneDX 1.6 + Teos extension model defined in `cbom-schema.md`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CbomDocument {
    /// CBOM / CycloneDX specification version (e.g., "1.6").
    pub spec_version: String,
    /// ISO 8601 generation timestamp.
    pub generated_at: String,
    /// Cryptographic assets in the bill of materials.
    pub assets: Vec<CbomAsset>,
}

/// A single cryptographic asset entry in a CBOM document.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CbomAsset {
    /// Unique asset identifier.
    pub asset_id: String,
    /// Algorithm family (e.g., "ML-KEM", "ML-DSA", "SLH-DSA").
    pub algorithm_family: String,
    /// `classical` | `post-quantum` | `hybrid`.
    pub classical_or_pq: String,
    /// Key size in bits; `None` when not applicable (e.g., entropy sources).
    pub key_size_bits: Option<u64>,
    /// Migration priority `P0`..`P3`.
    pub migration_priority: String,
}

impl CbomDocument {
    /// Constructs an empty document at a given spec version.
    pub fn new(spec_version: impl Into<String>) -> Self {
        Self {
            spec_version: spec_version.into(),
            generated_at: String::new(),
            assets: Vec::new(),
        }
    }
}

/// Register a PQC implementation (e.g., FIPS 203 ML-KEM-768) and return a
/// handle for later use. This package maintains no registry state.
pub fn register_algorithm(_fips_id: &str, _implementation: &str) -> TeosResult<Handle> {
    Err(TeosError::NotImplemented)
}

/// Rotate a cryptographic key to a new algorithm (or parameter set), returning
/// the new key identifier. This package maintains no key state.
pub fn rotate_key(_key_id: &str, _new_algo: &str) -> TeosResult<KeyId> {
    Err(TeosError::NotImplemented)
}

/// Generate a Cryptographic Bill of Materials snapshot. Stub only: no scanning
/// or CBOM generation logic is implemented in this package.
pub fn cbom_snapshot() -> TeosResult<CbomDocument> {
    Err(TeosError::NotImplemented)
}
