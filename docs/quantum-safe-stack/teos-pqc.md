# Teos-PQC

### Algorithm Agility Specs (Lattice-Based)

ML-KEM and ML-DSA are NIST-standardized lattice-based primitives serving different cryptographic roles:

- **KEM interface:** key generation, encapsulation, and decapsulation.
- **Signature interface:** key generation, signing, and verification.

The wrapper should support algorithm and parameter selection **within each role**. ML-KEM cannot replace ML-DSA, or vice versa. For an interface-only scaffold, this section describes intended contracts and algorithm metadata—not implemented or validated cryptographic capabilities.

| Property | ML-KEM, derived from CRYSTALS-Kyber | ML-DSA, derived from CRYSTALS-Dilithium |
|---|---|---|
| **Role** | Establish a shared secret | Sign messages and verify signatures |
| **Standard** | FIPS 203 | FIPS 204 |
| **Parameter sets** | ML-KEM-512 / ML-KEM-768 / ML-KEM-1024 | ML-DSA-44 / ML-DSA-65 / ML-DSA-87 |
| **NIST security categories** | 1 / 3 / 5 | 2 / 3 / 5 |
| **Underlying problems** | Module-LWE | Module-LWE and module-SIS–type problems |
| **Public key size, bytes** | 800 / 1,184 / 1,568 | 1,312 / 1,952 / 2,592 |
| **Private key size, bytes** | 1,632 / 2,400 / 3,168 | **2,560 / 4,032 / 4,896** |
| **Ciphertext size, bytes** | 768 / 1,088 / 1,568 | Not applicable |
| **Signature size, bytes** | Not applicable | **2,420 / 3,309 / 4,627** |
| **Shared-secret size, bytes** | 32 for every parameter set | Not applicable |
| **Example applications** | Secure-channel key establishment, including protocol-defined hybrid constructions | Code signing, signed updates, authentication, and certificate signatures where supported |

**Interpretation and implementation notes**

- Values follow the parameter-set order shown above. Sizes describe raw algorithm encodings; certificate/container overhead is excluded. Compact seed-based private-key representations have different sizes.
- ML-KEM alone does **not authenticate the peer**. Authentication must come from the surrounding protocol.
- Do not assume compatibility with pre-standardization Kyber or Dilithium implementations.
- Performance claims should identify the parameter set, implementation/version, CPU, compiler settings, and measurement method.
- Constant-time behavior, masking, and resistance to other side channels require implementation-specific assessment.
- Implementing a FIPS-standardized algorithm does **not** by itself make a cryptographic module FIPS 140 validated.

**Primary references:** [FIPS 203 — ML-KEM](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204 — ML-DSA](https://csrc.nist.gov/pubs/fips/204/final).

---

For later expansion, **SLH-DSA (FIPS 205)** is a standardized hash-based option. Isogeny-based schemes should not be presented as a NIST-standardized PQC family.