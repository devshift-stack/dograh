# Fish Audio and Deepgram EU provider notes

## Fish Audio S2.1-Pro

Dograh's Fish provider uses `s2.1-pro` by default. The project factory always
passes a non-empty model through `FishAudioTTSSettings`, so that project value
overrides Pipecat's internal `s2-pro` fallback. A configured custom model still
wins.

S2.1-Pro has no separate emotion or tag API. Delivery cues remain part of the
LLM-generated text:

```text
LLM text -> XMLFunctionTagFilter -> FishAudioTTSService -> Fish WebSocket text event
```

`XMLFunctionTagFilter` removes XML function-call markup only. Square-bracket
cues such as `[happy]` or `[emphasis]` pass through unchanged and are sent in
the WebSocket `text` event.

### Voice-agent prompt rules

- Use S2 square brackets, for example `[empathetic]`; do not use legacy S1
  parentheses or SSML.
- Put sentence-level emotion cues at the start of the sentence. Put effects and
  `[emphasis]` where they should occur.
- Combine at most three cues per sentence and avoid conflicting or excessive
  cues.
- Prefer short, lowercase English cue descriptions. S2.1-Pro supports free-form
  natural-language cues, so this list is guidance rather than a validation enum.
- Use the same cues for German and Bosnian. The spoken language comes from the
  selected voice and the sentence text, not from localized tag names.

Recommended compact set for voice agents:

| Category | Suggested cues |
| --- | --- |
| Emotion and manner | `[friendly]`, `[empathetic]`, `[confident]`, `[calm]`, `[happy]`, `[grateful]` |
| Tone | `[soft tone]`, `[whispering]`, `[emphasis]` |
| Human effects | `[laughing]`, `[sighing]`, `[gasping]` |
| Pauses | `[break]`, `[long-break]` |
| Intensity and free-form | `[slightly sad]`, `[very excited]`, `[whispers sweetly]` |

German example:

```text
[empathetic] Das verstehe ich. [break] Ich helfe Ihnen gern weiter.
```

Bosnian example:

```text
[empathetic] Razumijem. [break] Rado ću vam pomoći.
```

References:

- https://docs.fish.audio/developer-guide/models-pricing/models-overview
- https://docs.fish.audio/developer-guide/core-features/emotions
- https://docs.fish.audio/developer-guide/integrations/pipecat

## Deepgram Nova-3 defaults

Standard Deepgram and Deepgram EU share one Nova/Flux factory path. Deepgram EU
differs only by the EU endpoint and the fixed usage tags `["dograh", "eu"]`.

| Nova-3 option | Effective default | State | EU identical? |
| --- | --- | --- | --- |
| `punctuate` | `True` from Pipecat | On | Yes |
| `smart_format` | `False` from Pipecat | Off | Yes |
| `endpointing` | `100` ms from Dograh factory | On | Yes |
| `diarize` | `False` from Pipecat | Off | Yes |
| `keyterm` | Runtime keyterms or `[]` | Off when empty; on with runtime keyterms | Yes |
| `language` | Configured language or `multi` | On | Yes |
| `model` | Configured model; registry default `nova-3-general` | On | Yes |
| `filler_words` | Not configured | Off | Yes |
| `redact` | `None` from Pipecat | Off | Yes |
| `utterances` | Not configured; `utterance_end_ms=None` | Off | Yes |

The EU Nova path uses `api.eu.deepgram.com` for `/v1/listen`; the EU Flux path
uses `wss://api.eu.deepgram.com/v2/listen`. Usage tags are fixed in the factory
and are not exposed as UI configuration.
