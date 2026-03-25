import os

import gradio as gr
import pandas as pd


def get_sample_dataframe(sample_size):
    return df.sample(sample_size)


df = pd.read_csv(os.environ.get("SALES_FILEPATH"))


demo = gr.Interface(
    fn=get_sample_dataframe,
    inputs=[gr.Number()],  # inputs=["number"],
    outputs=["dataframe"],  # outputs=[gr.DataFrame()],
)
demo.launch()
