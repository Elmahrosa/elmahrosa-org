use teos_common::{Params, TeosError};

#[test]
fn keypair_is_stubbed_for_all_param_families() {
    let cases = [
        Params::MLKem512,
        Params::MLKem768,
        Params::MLKem1024,
        Params::MLDsa65,
        Params::SlhDsaSha2_256s,
    ];
    for params in cases {
        assert_eq!(
            teos_pqc::keypair(params).unwrap_err(),
            TeosError::NotImplemented,
            "keypair({params}) must be NotImplemented"
        );
    }
}

#[test]
fn kdf_operations_are_stubbed() {
    let pk = b"dummy public key";
    assert_eq!(
        teos_pqc::encapsulate(pk).unwrap_err(),
        TeosError::NotImplemented
    );
    assert_eq!(
        teos_pqc::decapsulate(b"dummy sk", b"dummy ct").unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn signature_operations_are_stubbed() {
    assert_eq!(
        teos_pqc::sign(b"dummy sk", b"dummy msg").unwrap_err(),
        TeosError::NotImplemented
    );
    assert_eq!(
        teos_pqc::verify(b"dummy pk", b"dummy msg", b"dummy sig").unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn stub_functions_never_produce_bytes() {
    assert!(teos_pqc::keypair(Params::MLKem768).is_err());
    assert!(teos_pqc::encapsulate(b"pk").is_err());
    assert!(teos_pqc::sign(b"sk", b"msg").is_err());
    assert!(teos_pqc::verify(b"pk", b"msg", b"sig").is_err());
}
