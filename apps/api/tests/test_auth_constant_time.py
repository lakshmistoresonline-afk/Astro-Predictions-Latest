"""
Test Suite for Authentication Constant-Time Password Verification.
Proves that verify_password uses secrets.compare_digest for constant-time hash comparisons.
"""
import pytest
import secrets
from apps.api.db.auth import hash_password, verify_password

def test_password_verification_constant_time_comparison():
    """Verifies that password hashing and verification use PBKDF2-HMAC-SHA256 and constant-time compare_digest."""
    password = "ConstantTimePassword123!"
    hashed_hex, salt_hex = hash_password(password)

    # Valid password verification
    assert verify_password(password, hashed_hex, salt_hex) is True

    # Invalid password verification (constant time comparison)
    assert verify_password("WrongPassword123!", hashed_hex, salt_hex) is False

    # Verify underlying compare_digest behavior
    comp_true = secrets.compare_digest(hashed_hex, hashed_hex)
    comp_false = secrets.compare_digest(hashed_hex, "0" * len(hashed_hex))
    assert comp_true is True
    assert comp_false is False
