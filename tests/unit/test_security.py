from app.core.security import hash_password, verify_password


def test_password_hash_roundtrip() -> None:
    password = "secret123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_wrong_password_fails() -> None:
    password = "secret123"

    hashed = hash_password(password)

    assert not verify_password("wrong-password", hashed)


def test_hashes_are_different() -> None:
    password = "secret123"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
    assert verify_password(password, first_hash)
    assert verify_password(password, second_hash)
