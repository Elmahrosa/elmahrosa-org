//! Teos-PQC — Post-Quantum Cryptography interface stub.
//!
//! Interface-only implementation of
//! [`modules/quantum-safe/teos-pqc/README.md`](../../README.md). All operations
//! are stubs returning [`TeosError::NotImplemented`]; no live cryptographic
//! operations, key generation, or entropy handling occur in this package.
//!
//! Conventions follow [`COMMON-CONTRACT.md`](../../COMMON-CONTRACT.md):
//! every function returns a `TeosResult` (no exceptions), and `params` uses
//! FIPS-named strings (legacy aliases accepted on parse, never preferred).

use teos_common::{Params, TeosError, TeosResult};

fn stub<T>() -> TeosResult<T> {
    Err(TeosError::NotImplemented)
}

/// Generate a key pair for the given FIPS parameter set
/// (`keypair(params) -> (public_key, private_key)`).
pub fn keypair(_params: Params) -> TeosResult<(Vec<u8>, Vec<u8>)> {
    stub()
}

/// Encapsulate a shared secret for a KEM public key
/// (`encapsulate(public_key) -> (ciphertext, shared_secret)`).
pub fn encapsulate(_public_key: &[u8]) -> TeosResult<(Vec<u8>, Vec<u8>)> {
    stub()
}

/// Decapsulate a shared secret for a KEM private key and ciphertext
/// (`decapsulate(private_key, ciphertext) -> shared_secret`).
pub fn decapsulate(_private_key: &[u8], _ciphertext: &[u8]) -> TeosResult<Vec<u8>> {
    stub()
}

/// Sign a message with a signing private key
/// (`sign(private_key, message) -> signature`).
pub fn sign(_private_key: &[u8], _message: &[u8]) -> TeosResult<Vec<u8>> {
    stub()
}

/// Verify a signature over a message with a public key
/// (`verify(public_key, message, signature) -> bool`).
///
/// All functions follow the `Result<T, TeosError>` error model, so this
/// returns `TeosResult<bool>` per `COMMON-CONTRACT.md`.
pub fn verify(_public_key: &[u8], _message: &[u8], _signature: &[u8]) -> TeosResult<bool> {
    stub()
}
