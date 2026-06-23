from app.services.ai_service import normalize_key_points


def test_normalize_key_points_returns_empty_list_for_non_list():
    result = normalize_key_points("not a list")

    assert result == []


def test_normalize_key_points_converts_values_to_strings():
    result = normalize_key_points(["Bitcoin", 123, True])

    assert result == ["Bitcoin", "123", "True"]


def test_normalize_key_points_removes_empty_values():
    result = normalize_key_points(["Bitcoin", "", None, "Gold"])

    assert result == ["Bitcoin", "Gold"]
