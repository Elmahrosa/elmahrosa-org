# Common Contract Conventions

- All byte outputs are raw `bytes`; length is defined by the FIPS parameter set (see teos-pqc.md size table).
- Errors: functions return `Result<T, TeosError>`; no exceptions.
  TeosError ∈ { NOT_IMPLEMENTED, INVALID_PARAM, UNSUPPORTED_ALGO, AUTH_FAIL,
  DECAPS_FAIL, ENTROPY_HEALTH_FAIL, KEY_NOT_FOUND }
- `params` is a FIPS-named string: "ML-KEM-768", "ML-DSA-65",
  "SLH-DSA-SHA2-128s". Legacy names (Kyber768, Dilithium3) are
  accepted as aliases only.
- Secrets (private keys, shared secrets) MUST be zeroized by the
  caller; the interface never logs or serializes them.