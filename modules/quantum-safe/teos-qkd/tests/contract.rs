use teos_common::TeosError;
use teos_qkd::{AuthToken, KeyMetadata};

#[test]
fn authenticate_channel_is_stubbed() {
    assert_eq!(
        teos_qkd::authenticate_channel("peer-1", b"local sk", b"peer pk").unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn exchange_key_is_stubbed() {
    let token = AuthToken {
        session_id: "session-1".to_string(),
    };
    assert_eq!(
        teos_qkd::exchange_key(&token).unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn bearer_types_are_defined() {
    let token = AuthToken {
        session_id: "session-1".to_string(),
    };
    assert_eq!(token.session_id, "session-1");
    let meta = KeyMetadata {
        key_rate_bits_per_sec: 1000,
        timestamp_unix: 1_700_000_000,
    };
    assert_eq!(meta.key_rate_bits_per_sec, 1000);
    assert_eq!(meta.timestamp_unix, 1_700_000_000);
}
