//! Teos Quantum-Safe Stack — shared conventions.
//!
//! Implements the error model and FIPS parameter naming defined in
//! [`COMMON-CONTRACT.md`](../../COMMON-CONTRACT.md). No C-style `TEOS_PQC_*`
//! codes are used anywhere in this stack.

use std::fmt;
use std::str::FromStr;

/// Canonical error model for all Teos Quantum-Safe interfaces.
///
/// Mirrors `TeosError` from `COMMON-CONTRACT.md`:
/// `{ NOT_IMPLEMENTED, INVALID_PARAM, UNSUPPORTED_ALGO, AUTH_FAIL,
/// DECAPS_FAIL, ENTROPY_HEALTH_FAIL, KEY_NOT_FOUND }`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TeosError {
    /// Operation is not implemented (interface-only stub). Used by every
    /// Phase 1 function until a separately scoped implementation exists.
    NotImplemented,
    /// A parameter is malformed or out of the contract's range.
    InvalidParam,
    /// A valid, recognized algorithm is not supported in this context.
    UnsupportedAlgo,
    /// Authentication of a channel or caller failed.
    AuthFail,
    /// KEM decapsulation failed (malformed ciphertext or key mismatch).
    DecapsFail,
    /// Entropy source failed a health test; source is in ERROR state.
    EntropyHealthFail,
    /// A referenced key, handle, or record was not found.
    KeyNotFound,
}

impl TeosError {
    /// Returns the canonical machine-readable name.
    pub const fn as_str(&self) -> &'static str {
        match self {
            Self::NotImplemented => "NOT_IMPLEMENTED",
            Self::InvalidParam => "INVALID_PARAM",
            Self::UnsupportedAlgo => "UNSUPPORTED_ALGO",
            Self::AuthFail => "AUTH_FAIL",
            Self::DecapsFail => "DECAPS_FAIL",
            Self::EntropyHealthFail => "ENTROPY_HEALTH_FAIL",
            Self::KeyNotFound => "KEY_NOT_FOUND",
        }
    }
}

impl fmt::Display for TeosError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

impl std::error::Error for TeosError {}

/// Result alias: every interface function returns `Result<T, TeosError>`;
/// no exceptions.
pub type TeosResult<T> = Result<T, TeosError>;

/// Algorithm family distinguishing KEM from signature schemes (roadmap MPQC.2).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ParamsFamily {
    /// Key encapsulation mechanism (ML-KEM).
    Kem,
    /// Digital signature scheme (ML-DSA, SLH-DSA).
    Signature,
}

/// A FIPS-named parameter set.
///
/// Canonical names per `COMMON-CONTRACT.md`; legacy aliases (Kyber, Dilithium,
/// SPHINCS+) are accepted on parse but never preferred.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Params {
    MLKem512,
    MLKem768,
    MLKem1024,
    MLDsa44,
    MLDsa65,
    MLDsa87,
    SlhDsaSha2_128s,
    SlhDsaSha2_128f,
    SlhDsaSha2_192s,
    SlhDsaSha2_192f,
    SlhDsaSha2_256s,
    SlhDsaSha2_256f,
}

impl Params {
    /// Returns the algorithm family (KEM vs. signature).
    pub const fn family(&self) -> ParamsFamily {
        match self {
            Self::MLKem512 | Self::MLKem768 | Self::MLKem1024 => ParamsFamily::Kem,
            Self::MLDsa44
            | Self::MLDsa65
            | Self::MLDsa87
            | Self::SlhDsaSha2_128s
            | Self::SlhDsaSha2_128f
            | Self::SlhDsaSha2_192s
            | Self::SlhDsaSha2_192f
            | Self::SlhDsaSha2_256s
            | Self::SlhDsaSha2_256f => ParamsFamily::Signature,
        }
    }
}

impl FromStr for Params {
    type Err = TeosError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let norm = s.to_ascii_lowercase().replace(['-', '_'], "");
        match norm.as_str() {
            "mlkem512" | "kyber512" | "kyber" => Ok(Self::MLKem512),
            "mlkem768" | "kyber768" => Ok(Self::MLKem768),
            "mlkem1024" | "kyber1024" => Ok(Self::MLKem1024),
            "mldsa44" | "dilithium2" => Ok(Self::MLDsa44),
            "mldsa65" | "dilithium3" => Ok(Self::MLDsa65),
            "mldsa87" | "dilithium5" => Ok(Self::MLDsa87),
            "slhdsasha2128s" | "sphincs+128s" | "sphincs128s" => Ok(Self::SlhDsaSha2_128s),
            "slhdsasha2128f" | "sphincs+128f" | "sphincs128f" => Ok(Self::SlhDsaSha2_128f),
            "slhdsasha2192s" | "sphincs+192s" | "sphincs192s" => Ok(Self::SlhDsaSha2_192s),
            "slhdsasha2192f" | "sphincs+192f" | "sphincs192f" => Ok(Self::SlhDsaSha2_192f),
            "slhdsasha2256s" | "sphincs+256s" | "sphincs256s" => Ok(Self::SlhDsaSha2_256s),
            "slhdsasha2256f" | "sphincs+256f" | "sphincs256f" => Ok(Self::SlhDsaSha2_256f),
            _ => Err(TeosError::InvalidParam),
        }
    }
}

impl fmt::Display for Params {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self {
            Self::MLKem512 => "ML-KEM-512",
            Self::MLKem768 => "ML-KEM-768",
            Self::MLKem1024 => "ML-KEM-1024",
            Self::MLDsa44 => "ML-DSA-44",
            Self::MLDsa65 => "ML-DSA-65",
            Self::MLDsa87 => "ML-DSA-87",
            Self::SlhDsaSha2_128s => "SLH-DSA-SHA2-128s",
            Self::SlhDsaSha2_128f => "SLH-DSA-SHA2-128f",
            Self::SlhDsaSha2_192s => "SLH-DSA-SHA2-192s",
            Self::SlhDsaSha2_192f => "SLH-DSA-SHA2-192f",
            Self::SlhDsaSha2_256s => "SLH-DSA-SHA2-256s",
            Self::SlhDsaSha2_256f => "SLH-DSA-SHA2-256f",
        })
    }
}
