from unittest.mock import patch

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwk, jwt

from app.core.security import verify_clerk_token
from app.core.settings import get_settings


def _generate_key_pair(kid: str) -> tuple[str, dict]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()

    public_jwk = jwk.construct(public_pem, algorithm="RS256").to_dict()
    public_jwk["kid"] = kid
    return private_pem, public_jwk


def test_verify_clerk_token_accepts_a_validly_signed_token() -> None:
    private_pem, public_jwk = _generate_key_pair("test-kid")
    issuer = get_settings().clerk_issuer
    token = jwt.encode({"sub": "user_abc123", "iss": issuer}, private_pem, algorithm="RS256", headers={"kid": "test-kid"})

    with patch("app.core.security._fetch_jwks", return_value=[public_jwk]):
        assert verify_clerk_token(token) == "user_abc123"


def test_verify_clerk_token_rejects_a_token_signed_by_an_unknown_key() -> None:
    _, public_jwk = _generate_key_pair("test-kid")
    other_private_pem, _ = _generate_key_pair("test-kid")
    issuer = get_settings().clerk_issuer
    forged_token = jwt.encode({"sub": "user_abc123", "iss": issuer}, other_private_pem, algorithm="RS256", headers={"kid": "test-kid"})

    with patch("app.core.security._fetch_jwks", return_value=[public_jwk]):
        with pytest.raises(ValueError):
            verify_clerk_token(forged_token)


def test_verify_clerk_token_rejects_a_malformed_token() -> None:
    with pytest.raises(ValueError):
        verify_clerk_token("not-a-jwt")
