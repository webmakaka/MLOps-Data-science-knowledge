import gradio as gr

with gr.Blocks() as demo:
    singleton = gr.State(set())  # переменная сессии
    with gr.Row() as row:
        with gr.Column():
            input_letter = gr.Textbox(label="Enter word")
            btn = gr.Button("Add word")
        with gr.Column():
            session_words_box = gr.Textbox(label="Current words")

    def add_word(word, session_words):
        session_words.add(word)
        return [session_words, ", ".join(session_words)]

    btn.click(
        add_word,
        [input_letter, singleton],
        [singleton, session_words_box],
    )
demo.launch()
