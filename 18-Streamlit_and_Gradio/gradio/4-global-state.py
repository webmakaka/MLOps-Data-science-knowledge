import gradio as gr

global_list = []


def add_item(item):
    global_list.append(item)
    return global_list


demo = gr.Interface(add_item, gr.Textbox(), gr.JSON(label="All items"))
demo.launch()
