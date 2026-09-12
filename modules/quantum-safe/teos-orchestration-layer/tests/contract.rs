use teos_common::TeosError;
use teos_orchestration_layer::{CbomAsset, CbomDocument};

#[test]
fn register_algorithm_is_stubbed() {
    assert_eq!(
        teos_orchestration_layer::register_algorithm("ML-KEM-768", "acme-impl-v1").unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn rotate_key_is_stubbed() {
    assert_eq!(
        teos_orchestration_layer::rotate_key("key-1", "SLH-DSA-SHA2-256s").unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn cbom_snapshot_is_stubbed() {
    assert_eq!(
        teos_orchestration_layer::cbom_snapshot().unwrap_err(),
        TeosError::NotImplemented
    );
}

#[test]
fn cbom_document_shape_is_constructible() {
    let doc = CbomDocument::new("1.6");
    assert_eq!(doc.spec_version, "1.6");
    assert!(doc.assets.is_empty());

    let asset = CbomAsset {
        asset_id: "asset-1".to_string(),
        algorithm_family: "ML-KEM".to_string(),
        classical_or_pq: "post-quantum".to_string(),
        key_size_bits: Some(1184),
        migration_priority: "P3".to_string(),
    };
    assert_eq!(asset.asset_id, "asset-1");
    assert_eq!(asset.key_size_bits, Some(1184));
}
