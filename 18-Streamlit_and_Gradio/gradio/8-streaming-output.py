import time

import gradio as gr


def magic_answer(message):
    for i in range(len(message)):
        time.sleep(0.1)
        yield message[: i + 1]


demo = gr.Interface(magic_answer, inputs=["text"], outputs=["text"])
demo.launch()
