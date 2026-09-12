//! Teos-QRNG — Quantum Random Number Generation interface stub.
//!
//! Interface-only implementation of
//! [`modules/quantum-safe/teos-qrng/README.md`](../../README.md). All
//! operations are stubs returning [`TeosError::NotImplemented`]; no entropy
//! is generated or conditioned in this package.
//!
//! Entropy requirements follow NIST SP 800-90B/C: conditioning only through
//! vetted functions, health tests per SP 800-90B §4.3, and consumption via an
//! SP 800-90A DRBG (never raw source).
//!
//! NOTE: In a real implementation, a health-test failure must transition the
//! source to ERROR state and make `get_entropy` return
//! [`TeosError::EntropyHealthFail`] until reset.

use teos_common::{TeosError, TeosResult};

/// Startup health test: validates ≥1024 samples through RCT/APT
/// (SP 800-90B §4.3). Returns true if the source passes.
pub fn health_test() -> TeosResult<bool> {
    Err(TeosError::NotImplemented)
}

/// Returns `n_bytes` of conditioned entropy output with declared min-entropy
/// per SP 800-90B.
pub fn get_entropy(n_bytes: usize) -> TeosResult<Vec<u8>> {
    if n_bytes == 0 {
        return Err(TeosError::InvalidParam);
    }
    Err(TeosError::NotImplemented)
}

/// Online continuous validation (RCT + APT) applied to every output
/// (SP 800-90B). Returns true if validation passes.
pub fn continuous_validation() -> TeosResult<bool> {
    Err(TeosError::NotImplemented)
}
