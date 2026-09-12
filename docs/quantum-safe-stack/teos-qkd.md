# Teos-QKD

## Mechanism
Quantum Key Distribution via single-photon encoding

## Security property
Interception collapses quantum state → enables eavesdrop detection

## Status
Architecture reference only — no physical QKD hardware integration in this repo

## Standards References
- ETSI GS QKD 014 — Key delivery API (REST) — governs `exchange_key` shape
- ETSI GS QKD 004 — Application interface
- ITU-T Y.3800 series — QKD network architecture
- NIST SP 1800-38 — PQC migration / crypto-agility context
- FIPS 204 (ML-DSA) — authentication of the QKD classical channel

> Note: QKD is not NIST-standardized or CMVP-validated. In this
> architecture QKD is an optional key source layered on top of PQC,
> never a substitute for it. Classical-channel authentication MUST
> use ML-DSA (FIPS 204).