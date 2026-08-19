import os
import gradio as gr

try:
    import spaces
except ImportError:
    spaces = None


BUILD_MARKER = "space-build-2026-07-27-1538"


def _respond_impl(message, history):
    response = f"You said: {message}\nAnd I say I love learning AI Engineering!"
    return response


if spaces is not None:
    @spaces.GPU
    def respond(message, history):
        return _respond_impl(message, history)
else:
    def respond(message, history):
        return _respond_impl(message, history)

chatbot = gr.Chatbot(type="messages")

demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    chatbot=chatbot,
    title="My First Space",
    description="This is my first space using Gradio.",
)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    print(f"Build marker: {BUILD_MARKER}")
    print(f"Gradio version: {gr.__version__}")
    print(f"App file: {__file__}")
    print(f"spaces module loaded: {spaces is not None}")
    print(f"Starting Gradio on 0.0.0.0:{port}")
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        show_error=True,
        ssr_mode=False,
)
"""import gradio as gr

def respond(message, history):
    response = f"You said: {message}\
        \n And I say I love learning AI Engineering with SuperDataScience!"
    return response

gr.ChatInterface(fn=respond).launch"""