use teos_common::{Params, ParamsFamily, TeosError};

#[test]
fn error_variants_are_distinct() {
    let variants = [
        TeosError::NotImplemented,
        TeosError::InvalidParam,
        TeosError::UnsupportedAlgo,
        TeosError::AuthFail,
        TeosError::DecapsFail,
        TeosError::EntropyHealthFail,
        TeosError::KeyNotFound,
    ];
    for (i, a) in variants.iter().enumerate() {
        for (j, b) in variants.iter().enumerate() {
            assert_eq!(a == b, i == j, "{a:?} vs {b:?}");
        }
    }
}

#[test]
fn error_names_match_common_contract() {
    assert_eq!(TeosError::NotImplemented.to_string(), "NOT_IMPLEMENTED");
    assert_eq!(TeosError::InvalidParam.to_string(), "INVALID_PARAM");
    assert_eq!(TeosError::UnsupportedAlgo.to_string(), "UNSUPPORTED_ALGO");
    assert_eq!(TeosError::AuthFail.to_string(), "AUTH_FAIL");
    assert_eq!(TeosError::DecapsFail.to_string(), "DECAPS_FAIL");
    assert_eq!(
        TeosError::EntropyHealthFail.to_string(),
        "ENTROPY_HEALTH_FAIL"
    );
    assert_eq!(TeosError::KeyNotFound.to_string(), "KEY_NOT_FOUND");
}

#[test]
fn canonical_fips_names_parse() {
    for (s, expected) in [
        ("ML-KEM-512", Params::MLKem512),
        ("ML-KEM-768", Params::MLKem768),
        ("ML-KEM-1024", Params::MLKem1024),
        ("ML-DSA-44", Params::MLDsa44),
        ("ML-DSA-65", Params::MLDsa65),
        ("ML-DSA-87", Params::MLDsa87),
        ("SLH-DSA-SHA2-128s", Params::SlhDsaSha2_128s),
        ("SLH-DSA-SHA2-256f", Params::SlhDsaSha2_256f),
    ] {
        assert_eq!(s.parse::<Params>().unwrap(), expected, "canonical {s}");
    }
}

#[test]
fn legacy_aliases_parse_but_render_canonical() {
    assert_eq!("Kyber768".parse::<Params>().unwrap(), Params::MLKem768);
    assert_eq!(
        "Kyber768".parse::<Params>().unwrap().to_string(),
        "ML-KEM-768"
    );
    assert_eq!("Dilithium3".parse::<Params>().unwrap(), Params::MLDsa65);
    assert_eq!(
        "Dilithium3".parse::<Params>().unwrap().to_string(),
        "ML-DSA-65"
    );
    assert_eq!(
        "SPHINCS+-128s".parse::<Params>().unwrap(),
        Params::SlhDsaSha2_128s
    );
}

#[test]
fn unknown_param_is_invalid_param() {
    assert_eq!(
        "TLS-1.3".parse::<Params>().unwrap_err(),
        TeosError::InvalidParam
    );
    assert_eq!("".parse::<Params>().unwrap_err(), TeosError::InvalidParam);
}

#[test]
fn family_split_is_kem_vs_signature() {
    assert_eq!(Params::MLKem768.family(), ParamsFamily::Kem);
    assert_eq!(Params::MLDsa65.family(), ParamsFamily::Signature);
    assert_eq!(Params::SlhDsaSha2_256s.family(), ParamsFamily::Signature);
}
