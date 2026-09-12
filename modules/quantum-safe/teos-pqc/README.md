# Teos-PQC Module

## Interface Definition
(Stub - no live implementation)

This module defines the interface for Post-Quantum Cryptography mechanisms.

## Interface Contract
- `keypair(params) -> (public_key, private_key)`: Generate a key pair for the given parameter set (e.g., ML-KEM-512, ML-DSA-65).
- `encapsulate(public_key) -> (ciphertext, shared_secret)`: For KEM schemes (ML-KEM), encapsulate a shared secret.
- `decapsulate(private_key, ciphertext) -> shared_secret`: For KEM schemes, decapsulate to recover shared secret.
- `sign(private_key, message) -> signature`: For signature schemes (ML-DSA, SLH-DSA), sign a message.
- `verify(public_key, message, signature) -> bool`: Verify a signature.
*Note: Implementations must specify which algorithm (KEM vs signature) they support; the wrapper should allow runtime selection of parameter sets and algorithm families.*

## Common Contract Conventions
See [COMMON-CONTRACT.md](../COMMON-CONTRACT.md)