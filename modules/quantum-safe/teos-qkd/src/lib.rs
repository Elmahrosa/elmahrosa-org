//! Teos-QKD — Quantum Key Distribution interface stub.
//!
//! Interface-only implementation of
//! [`modules/quantum-safe/teos-qkd/README.md`](../../README.md). All operations
//! are stubs returning [`TeosError::NotImplemented`]; no QKD hardware
//! integration or key exchange occurs in this package.
//!
//! Note: QKD is not NIST-standardized. Classical-channel authentication
//! requires ML-DSA (FIPS 204).

use teos_common::{TeosError, TeosResult};

/// Authentication token produced by `authenticate_channel`, containing the
/// session ID negotiated for the QKD classical channel.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AuthToken {
    /// Session identifier for the authenticated channel.
    pub session_id: String,
}

/// Metadata accompanying a QKD key exchange (e.g., key rate, timestamp).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct KeyMetadata {
    /// Key rate in bits per second.
    pub key_rate_bits_per_sec: u64,
    /// Unix timestamp of the exchange.
    pub timestamp_unix: u64,
}

/// Authenticate the QKD classical channel using the local ML-DSA secret key
/// and the peer's ML-DSA public key, returning an [`AuthToken`].
pub fn authenticate_channel(
    _peer_id: &str,
    _local_sk: &[u8],
    _peer_pk: &[u8],
) -> TeosResult<AuthToken> {
    Err(TeosError::NotImplemented)
}

/// Perform a QKD key exchange after authentication, returning the shared key,
/// a key identifier, and [`KeyMetadata`].
pub fn exchange_key(_auth_token: &AuthToken) -> TeosResult<(Vec<u8>, String, KeyMetadata)> {
    Err(TeosError::NotImplemented)
}
