use teos_common::TeosError;

#[test]
fn health_test_is_stubbed() {
    assert_eq!(
        teos_qrng::health_test().unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn continuous_validation_is_stubbed() {
    assert_eq!(
        teos_qrng::continuous_validation().unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn get_entropy_is_stubbed_for_positive_lengths() {
    assert_eq!(
        teos_qrng::get_entropy(16).unwrap_err(),
        TeosError::NotImplemented
    );
    assert_eq!(
        teos_qrng::get_entropy(1024).unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn get_entropy_rejects_zero_length() {
    assert_eq!(
        teos_qrng::get_entropy(0).unwrap_err(),
        TeosError::InvalidParam
    );
}

#[test]
fn stub_functions_never_produce_entropy() {
    assert!(teos_qrng::health_test().is_err());
    assert!(teos_qrng::get_entropy(32).is_err());
    assert!(teos_qrng::continuous_validation().is_err());
}
