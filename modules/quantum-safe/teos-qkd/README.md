# Teos-QKD Module

## Interface Definition
(Stub - no live implementation)

This module defines the interface for Quantum Key Distribution mechanisms.

## Interface Contract
- `authenticate_channel(peer_id, local_sk, peer_pk) -> Result<AuthToken>`: Authenticates the QKD classical channel using the local ML-DSA secret key and peer's ML-DSA public key. Returns an authentication token (containing a session ID) or error.
- `exchange_key(auth_token) -> Result<(shared_key, key_id, metadata)>`: Performs QKD key exchange after authentication, returns the shared secret key, a key identifier, and metadata (e.g., key rate, timestamp).

## Common Contract Conventions
See [COMMON-CONTRACT.md](../COMMON-CONTRACT.md)