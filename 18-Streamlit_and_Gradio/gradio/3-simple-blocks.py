import gradio as gr


def update(name):
    return f"Welcome to Gradio, {name}!"


with gr.Blocks() as demo:
    # Отформатированный текст
    gr.Markdown("Start typing _below_ and then click **Run** to see the output.")

    # Вёрстка: компоновка элементов в строку
    with gr.Row():
        # текстовое поле
        inp = gr.Textbox(placeholder="What is your name?")
        # текстовый ввод
        out = gr.Textbox()

    # Кнопка
    btn = gr.Button("Run")

    # действие при нажатии на кнопку
    btn.click(fn=update, inputs=inp, outputs=out)

demo.launch()
