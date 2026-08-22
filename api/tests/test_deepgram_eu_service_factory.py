from types import SimpleNamespace
from unittest.mock import patch

from api.services.configuration.registry import (
    REGISTRY,
    DeepgramEUSTTConfiguration,
    ServiceProviders,
    ServiceType,
)
from api.services.pipecat.audio_config import AudioConfig
from api.services.pipecat.service_factory import (
    DEEPGRAM_EU_BASE_URL,
    DEEPGRAM_EU_FLUX_URL,
    DEEPGRAM_EU_USAGE_TAGS,
    create_stt_service,
)


def _audio_config() -> AudioConfig:
    return AudioConfig(
        transport_in_sample_rate=16000,
        transport_out_sample_rate=16000,
    )


def test_deepgram_eu_configuration_title_and_defaults():
    config = DeepgramEUSTTConfiguration(api_key="test-key")

    assert config.provider == ServiceProviders.DEEPGRAM_EU
    assert config.model == "nova-3-general"
    assert config.language == "multi"
    assert DeepgramEUSTTConfiguration.model_json_schema()["title"] == "Deepgramm EU"
    assert (
        REGISTRY[ServiceType.STT][ServiceProviders.DEEPGRAM_EU]
        is DeepgramEUSTTConfiguration
    )


def test_create_deepgram_eu_nova_uses_eu_host_and_fixed_tags():
    user_config = SimpleNamespace(
        stt=SimpleNamespace(
            provider=ServiceProviders.DEEPGRAM_EU.value,
            api_key="test-key",
            model="nova-3-general",
            language="multi",
        )
    )

    with patch(
        "api.services.pipecat.service_factory.DeepgramSTTService"
    ) as mock_service:
        create_stt_service(user_config, _audio_config())

    kwargs = mock_service.call_args.kwargs
    assert kwargs["base_url"] == DEEPGRAM_EU_BASE_URL == "api.eu.deepgram.com"
    assert (
        kwargs["settings"].extra["tag"]
        == DEEPGRAM_EU_USAGE_TAGS
        == [
            "dograh",
            "eu",
        ]
    )
    assert kwargs["settings"].model == "nova-3-general"


def test_create_deepgram_eu_flux_uses_eu_v2_url_and_fixed_tags():
    user_config = SimpleNamespace(
        stt=SimpleNamespace(
            provider=ServiceProviders.DEEPGRAM_EU.value,
            api_key="test-key",
            model="flux-general-multi",
            language="multi",
        )
    )

    with patch(
        "api.services.pipecat.service_factory.DeepgramFluxSTTService"
    ) as mock_service:
        create_stt_service(user_config, _audio_config())

    kwargs = mock_service.call_args.kwargs
    assert kwargs["url"] == DEEPGRAM_EU_FLUX_URL
    assert kwargs["url"] == "wss://api.eu.deepgram.com/v2/listen"
    assert kwargs["tag"] == DEEPGRAM_EU_USAGE_TAGS == ["dograh", "eu"]
