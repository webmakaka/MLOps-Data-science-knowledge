import random

import gradio as gr


def magic_answer(message, history):
    return random.choice(["Yes", "No"])


demo = gr.ChatInterface(magic_answer)
demo.launch()
