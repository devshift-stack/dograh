from types import SimpleNamespace
from unittest.mock import patch

import pytest

from api.services.configuration.registry import (
    FISH_TTS_MODELS,
    REGISTRY,
    FishAudioTTSConfiguration,
    ServiceProviders,
    ServiceType,
)
from api.services.pipecat.service_factory import create_tts_service


def test_fish_audio_configuration_defaults():
    config = FishAudioTTSConfiguration(api_key="test-key", voice="voice-reference")

    assert config.provider == ServiceProviders.FISH
    assert config.model == "s2.1-pro"
    assert config.voice == "voice-reference"
    assert config.speed == 1.0
    assert FISH_TTS_MODELS == ["s2.1-pro"]
    assert FishAudioTTSConfiguration.model_json_schema()["title"] == "Fish Audio"
    assert REGISTRY[ServiceType.TTS][ServiceProviders.FISH] is FishAudioTTSConfiguration


@pytest.mark.parametrize("transport_out_sample_rate", [8000, 16000])
def test_create_fish_audio_service_uses_pcm_pipeline_settings(
    transport_out_sample_rate,
):
    user_config = SimpleNamespace(
        tts=SimpleNamespace(
            provider=ServiceProviders.FISH.value,
            api_key="test-key",
            model="s2-pro",
            voice="voice-reference",
            speed=1.25,
        )
    )
    audio_config = SimpleNamespace(
        transport_out_sample_rate=transport_out_sample_rate,
        transport_in_sample_rate=16000,
    )

    with patch(
        "api.services.pipecat.service_factory.FishAudioTTSService"
    ) as mock_service:
        create_tts_service(user_config, audio_config)

    kwargs = mock_service.call_args.kwargs
    assert kwargs["api_key"] == "test-key"
    assert kwargs["output_format"] == "pcm"
    assert kwargs["sample_rate"] == transport_out_sample_rate
    assert kwargs["settings"].model == "s2-pro"
    assert kwargs["settings"].voice == "voice-reference"
    assert kwargs["settings"].prosody_speed == 1.25


def test_create_fish_audio_service_defaults_to_s2_1_pro_when_model_is_unset():
    user_config = SimpleNamespace(
        tts=SimpleNamespace(
            provider=ServiceProviders.FISH.value,
            api_key="test-key",
            model=None,
            voice="voice-reference",
            speed=1.0,
        )
    )
    audio_config = SimpleNamespace(
        transport_out_sample_rate=16000,
        transport_in_sample_rate=16000,
    )

    with patch(
        "api.services.pipecat.service_factory.FishAudioTTSService"
    ) as mock_service:
        create_tts_service(user_config, audio_config)

    assert mock_service.call_args.kwargs["settings"].model == "s2.1-pro"


@pytest.mark.parametrize(
    "text",
    [
        "[happy] Hallo",
        "[whisper] Das bleibt unter uns.",
        "[laugh] Das war wirklich gut.",
        "Das ist [emphasis] besonders wichtig.",
        "Ich kann es [gasp] kaum glauben.",
        "[sad][sigh] Das tut mir leid.",
        "[whispers sweetly] Willkommen zurück.",
        "[excited] Čestitam, uspjeli smo!",
    ],
)
@pytest.mark.asyncio
async def test_fish_audio_filter_preserves_s2_emotion_tags(text):
    user_config = SimpleNamespace(
        tts=SimpleNamespace(
            provider=ServiceProviders.FISH.value,
            api_key="test-key",
            model="s2.1-pro",
            voice="voice-reference",
            speed=1.0,
        )
    )
    audio_config = SimpleNamespace(
        transport_out_sample_rate=16000,
        transport_in_sample_rate=16000,
    )

    with patch(
        "api.services.pipecat.service_factory.FishAudioTTSService"
    ) as mock_service:
        create_tts_service(user_config, audio_config)

    text_filter = mock_service.call_args.kwargs["text_filters"][0]
    assert await text_filter.filter(text) == text
