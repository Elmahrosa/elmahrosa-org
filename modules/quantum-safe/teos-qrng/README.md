# Teos-QRNG Module

## Interface Definition
(Stub - no live implementation)

This module defines the interface for Quantum Random Number Generation mechanisms.

## Interface Contract
- `health_test() -> Result<bool>`: Runs startup test (≥1024 samples through RCT/APT) per SP 800-90B §4.3; returns true if passes.
- `get_entropy(n_bytes) -> Result<bytes>`: Returns n_bytes of conditioned entropy output; min-entropy declared per SP 800-90B.
- `continuous_validation() -> Result<bool>`: Performs online continuous validation tests (RCT+APT) on every output per SP 800-90B; returns true if validation passes.

## Common Contract Conventions
See [COMMON-CONTRACT.md](../COMMON-CONTRACT.md)

## Entropy Validation Requirements (SP 800-90B/C)
- Noise source: declared min-entropy H per sample (SP 800-90B §3.1.3),
  supported by the IID/non-IID track assessment.
- Conditioning: vetted function only (SHA-256, HMAC, CMAC, or
  Hash_df per §3.1.5). Output entropy claim ≤ conditioned-output
  bound; full-entropy claims only per SP 800-90C.
- Health tests: startup (≥1024 samples), continuous RCT + APT,
  on-demand. Any failure → source enters ERROR state and
  `get_entropy` returns ENTROPY_HEALTH_FAIL until reset.
- Consumption: output feeds an SP 800-90A DRBG or is used directly
  only under a 90C full-entropy construction. PQC keygen (FIPS
  203/204/205) consumes randomness via the DRBG, never raw source.