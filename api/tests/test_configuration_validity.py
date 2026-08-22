from unittest.mock import patch

import httpx
import pytest

from api.services.configuration.check_validity import UserConfigurationValidator
from api.services.configuration.registry import ServiceProviders


def test_deepgram_eu_uses_existing_deepgram_key_validator():
    validator = UserConfigurationValidator()

    assert (
        validator._validator_map[ServiceProviders.DEEPGRAM_EU.value].__func__
        is validator._check_deepgram_api_key.__func__
    )


def test_fish_audio_is_registered_for_key_validation():
    validator = UserConfigurationValidator()

    assert ServiceProviders.FISH.value in validator._validator_map


def test_fish_audio_key_validation_accepts_authenticated_response():
    validator = UserConfigurationValidator()

    with patch("api.services.configuration.check_validity.httpx.get") as mock_get:
        mock_get.return_value.status_code = 200
        assert validator._check_fish_api_key("s2-pro", "fish-test-key") is True

    assert mock_get.call_args.args[0] == "https://api.fish.audio/model"
    assert mock_get.call_args.kwargs["headers"] == {
        "Authorization": "Bearer fish-test-key"
    }


@pytest.mark.parametrize("status_code", [401, 403])
def test_fish_audio_key_validation_rejects_auth_failures_without_key_leak(
    status_code,
):
    validator = UserConfigurationValidator()

    with patch("api.services.configuration.check_validity.httpx.get") as mock_get:
        mock_get.return_value.status_code = status_code
        with pytest.raises(ValueError) as exc_info:
            validator._check_fish_api_key("s2-pro", "fish-secret-test-key")

    assert "fish-secret-test-key" not in str(exc_info.value)


def test_fish_audio_key_validation_reports_network_failure_without_key_leak():
    validator = UserConfigurationValidator()

    with patch("api.services.configuration.check_validity.httpx.get") as mock_get:
        mock_get.side_effect = httpx.ConnectError("offline")
        with pytest.raises(ValueError) as exc_info:
            validator._check_fish_api_key("s2-pro", "fish-secret-test-key")

    assert "fish-secret-test-key" not in str(exc_info.value)
