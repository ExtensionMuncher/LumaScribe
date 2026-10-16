# LumaScribe

![LumaScribe Title](Assets/lumascribe_title.png)

**Speak freely. Stay local.**

LumaScribe is a Windows voice-typing app with a luminous, cyber-anime interface and custom Sachiko artwork. Press a global hotkey, speak, then press it again to type the transcription into the active window.

Speech recognition is powered by OpenAI's Whisper through **whisper.cpp**. LumaScribe provides the recording workflow, desktop integration and interface; it does not introduce a new speech-recognition model.

[GitHub repository](https://github.com/ExtensionMuncher/LumaScribe) · [Releases and downloads](https://github.com/ExtensionMuncher/LumaScribe/releases)

## Features

- Global recording hotkey, with real **click → press keys → Apply** binding capture.
- Dedicated Insert by default; optional numpad 0 trigger, **off by default**.
- Separate configurable cancel key; Escape by default.
- Simple microphone selection with one entry per Windows input and no driver acronyms, beneath the model and CUDA controls, with a system-default option, saved preference and Refresh button.
- Local transcription on an NVIDIA GPU using a selected CUDA-enabled whisper.cpp engine.
- Types into the active window without submitting the message.
- Floating microphone indicator, expanding session transcription history and copy-all button.
- Tray operation: closing the window hides it; **Quit completely** exits.
- Model loaded only for transcription. The engine process exits afterward, releasing its GPU allocations.
- Opening animation with a rounded pearl/cyan wordmark, glass halo and expanding concentric rings; separate music/voice audio and optional startup sound.
- In-app update checks and ZIP downloads from this repository's public GitHub Releases.

## Requirements

- Windows, an NVIDIA GPU and current compatible NVIDIA drivers.
- Python **3.10 or newer**, with Tkinter, available as `python` from a command prompt. In the Python installer, enable **Add Python to PATH**.
- A microphone.
- The bundled CUDA-enabled `Engine/whisper-cli.exe`, with its accompanying DLLs.
- A compatible local Whisper **GGML `.bin` model**.

This release uses GGML models for whisper.cpp, **not GGUF files, Hugging Face Transformers folders, or faster-whisper/CTranslate2 models**. A Hugging Face account/token is not needed by LumaScribe. It never downloads models automatically.

## Quick start

1. Download the latest `LumaScribe-vX.Y.Z-Windows.zip` from Releases and extract it completely.
2. Double-click **Open_LumaScribe.bat**. The launcher installs missing Python dependencies on the first run, then opens the app without a persistent command window.
3. Under **Model file**, choose a local `ggml-*.bin` file. If you already have one, reuse it.
4. The bundled **Engine/whisper-cli.exe** is selected automatically for new users. You can choose another engine if needed. Keep the engine's DLLs beside it. `WhisperDesktop.exe` is a separate application and is not a compatible CLI engine.
5. Under **Microphone**, choose the input you want, or leave **System default** selected. Your choice is saved. Use **Refresh** after connecting a microphone.
6. Click the text field in the destination app. Press **Insert** to record; press it again to stop and type.

The current transcription language is fixed to English. Multilingual model files can be selected, but this app currently passes `-l en` to the engine.

## Download a model

Start with **large-v3-turbo** if your hardware can accommodate it. For lighter models, compare the figures below and test accuracy on your own microphone/voice.

- [All compatible model files on Hugging Face](https://huggingface.co/ggerganov/whisper.cpp/tree/main)
- [large-v3-turbo — direct `.bin` download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin?download=true)
- [large-v3-turbo Q5 — direct `.bin` download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin?download=true)
- [small.en — direct `.bin` download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin?download=true)
- [base.en — direct `.bin` download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin?download=true)
- [Upstream model setup documentation](https://github.com/ggml-org/whisper.cpp/blob/master/models/README.md)

Choose the actual `ggml-*.bin` weights, not `for-tests-*` placeholders or Core ML encoder ZIPs. `.en` denotes an English-only model; Q5 files use quantized weights.

### Disk and memory comparison

These values are adapted from [whisper.cpp's memory table](https://github.com/ggml-org/whisper.cpp#memory-usage) and [its model listing](https://github.com/ggml-org/whisper.cpp/blob/master/models/README.md).

| Model | Model file size | whisper.cpp memory estimate |
|---|---:|---:|
| tiny / tiny.en | 75 MiB | ~273 MB |
| base / base.en | 142 MiB | ~388 MB |
| small / small.en | 466 MiB | ~852 MB |
| medium / medium.en | 1.5 GiB | ~2.1 GB |
| large (v1/v2/v3 family) | 2.9 GiB | ~3.9 GB |
| large-v3-turbo | 1.5 GiB | Not separately listed upstream |
| large-v3-turbo-q5_0 | 547 MiB | Not separately listed upstream |

The upstream “memory” column is not a separate RAM/VRAM breakdown. Actual use depends on backend, buffers, quantization, audio length and engine version; these are not measured LumaScribe CUDA requirements.

### Speed and GPU-memory reference

The following figures come from [OpenAI Whisper's model table](https://github.com/openai/whisper#available-models-and-languages). They describe **OpenAI's reference implementation**, not whisper.cpp or LumaScribe.

| Whisper family | Reference VRAM | Reference relative speed |
|---|---:|---:|
| tiny | ~1 GB | ~10× |
| base | ~1 GB | ~7× |
| small | ~2 GB | ~4× |
| medium | ~5 GB | ~2× |
| large | ~10 GB | 1× |
| turbo | ~6 GB | ~8× |

OpenAI measured the relative speeds on English speech using an NVIDIA A100. These are comparison figures, not guaranteed performance on your GPU. There is no universal “best” model: smaller models prioritize resource use; evaluate transcription quality with your own speech. No unverified accuracy scores are claimed here.

## CUDA engine

The Windows release includes your supplied CUDA engine in **Engine**. Keep `whisper-cli.exe` and every bundled DLL together. A valid engine previously selected in your settings is retained. No separate engine download is needed for this package. Compatible NVIDIA drivers and the Microsoft Visual C++ x64 runtime are still required. `whisper.dll` must remain beside `whisper-cli.exe`.

For a replacement engine:

Visit [whisper.cpp Releases](https://github.com/ggml-org/whisper.cpp/releases/latest). Choose a Windows x64 CUDA/cuBLAS build if one is provided for that release, extract the whole archive, and select its `whisper-cli.exe`. Keep all included DLLs together. A CPU-only archive will fail LumaScribe's CUDA confirmation check.

If a suitable prebuilt archive is unavailable, follow the [official NVIDIA GPU build instructions](https://github.com/ggml-org/whisper.cpp#nvidia-gpu-support). The upstream CMake switch is `-DGGML_CUDA=1`; building requires the appropriate compiler, CMake and CUDA Toolkit.

The app checks the engine's log for CUDA model execution and reports an error if it cannot confirm it. This is a CUDA-only workflow at present.

## Change the hotkeys

Open **Hotkey settings**, click the recording or cancel binding, and press the desired key or modifier combination. Release the main key, then click **Apply**. Use **Stop selecting** to abandon a capture, or **Cancel** to discard the dialog's changes.

Recording and cancellation must have different bindings. The main bindings use keys outside the numeric keypad. Enable **Also use numpad 0 / Insert as a trigger** only if you want that additional trigger; while enabled, that key no longer types `0`.

## Updates

Click **Check for updates** in the app. It checks this repository's latest stable public Release. If a newer version exists, it offers the Windows ZIP and lets you choose where to save it, without opening GitHub in a browser.

Downloads use HTTPS, have a 1 GiB size limit and ZIP-content checks, and verify GitHub's SHA-256 digest when provided. The app does not execute the downloaded archive. Quit LumaScribe, extract the update into a new folder, and launch it there. Existing settings are reused.

Updates are **manual checks**, not background polling. No GitHub token is required for public releases. Checks will report that no release is available until a public release has been published.

## Files and settings

Keep this folder structure when extracting or moving the app:

```text
Open_LumaScribe.bat
voice_typing.pyw
Assets/
    lumascribe_portrait.png
    lumascribe_title.png
    title_preview.png
    LumaScribe_Opening_Tune.wav
    LumaScribe_Voice_Op.wav
Model/
Engine/
    whisper-cli.exe
    (accompanying DLLs)
```

Place your downloaded `ggml-*.bin` model in **Model**, then select it with **Choose file…**. The picker opens there by default; models in other folders still work. No model is bundled.

Music and spoken opening are separate WAV files in **Assets**. The music file must be named exactly **LumaScribe_Opening_Tune.wav**.

Settings are stored at `%LOCALAPPDATA%\LocalVoiceTyping\settings.json`. The existing folder name is retained so older settings carry over. History is session-only. Temporary audio/transcript files are deleted when the transcription task finishes.

## Privacy

Microphone audio and transcription stay on your machine. Whisper runs locally through the engine you select. No model download, Hugging Face login or cloud transcription request is made by the app.

Network access is used by the launcher to install missing dependencies and by an explicit update check/download to contact GitHub. Those requests do not contain microphone audio or transcription text.

## Troubleshooting

- **Nothing opens:** extract the whole ZIP, keep its files together and use the included launcher. It displays dependency/startup errors.
- **`python` is not recognized:** install Python with its PATH option enabled, then reopen the launcher.
- **CUDA not confirmed / missing DLL:** use a CUDA-enabled engine archive, retain its DLLs and check your NVIDIA driver/build compatibility.
- **Text goes into the wrong window:** focus the destination field and keep it active until transcription finishes. Do not rely on typing into elevated/admin apps from an unelevated app.
- **Microphone unavailable:** reconnect the selected microphone and click Refresh, or choose another input/System default. A disconnected saved microphone is never silently replaced.
- **Microphone cannot open:** check Windows microphone permissions and close apps using it. If the device rejects mono 16 kHz recording, check the device settings or choose another microphone.
- **Numpad 0 starts recording:** turn off its optional trigger in Hotkey settings.
- **No updates found:** the repository needs a published public stable Release and the correctly named ZIP asset.

## Credits

- Application direction and custom Sachiko artwork: **Reticent Aoi**.
- Speech recognition: [OpenAI Whisper](https://github.com/openai/whisper).
- Local inference engine and model documentation: [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp).
- Pre-converted model distribution: [ggerganov/whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp).
- WhisperDesktop inspired the original workflow, including releasing model memory between transcriptions. LumaScribe currently calls whisper.cpp's CLI engine.

Versions through v0.1.3 used a smaller update-download limit. To upgrade from those versions to an engine-bundled release, download the ZIP manually from Releases once; v0.1.4 supports the larger package.

Model figures above are attributed to their upstream documentation, not original LumaScribe benchmarks. 
