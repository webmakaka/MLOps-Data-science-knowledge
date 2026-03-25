# libs are required: numpy, torch, torchaudio, transformers

import gradio as gr
import numpy as np
from transformers import pipeline

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")


def transcribe(stream, new_chunk):
    sr, y = new_chunk

    # `[:, 0]`: костыль для получения одноканального аудио
    y = y[:, 0].astype(np.float32)

    y /= np.max(np.abs(y))

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y

    return stream, transcriber({"sampling_rate": sr, "raw": stream})["text"]


demo = gr.Interface(
    transcribe,
    [gr.State(), gr.Audio(sources=["microphone"], streaming=True)],
    [gr.State(), gr.Textbox()],
    live=True,
)

demo.launch()
