import gradio as gr
import cfg
from hyperscalers.claude import ClaudeImageAnalyzer
from hyperscalers.gemini import GeminiImageAnalyzer
from hyperscalers.oai import LocalImageAnalyzer
from prompt import prompt_trash
import hashlib
import webbrowser
import threading
import time


def analyze_image(image_path, selected_model):
    # prompt = spaghetti_analysis_final_prompt()
    prompt = prompt_trash()

    if selected_model == "OpenAI GPT-4":
        analyzer = LocalImageAnalyzer()
        result = analyzer.analyze_image(
            image_path=image_path,
            prompt=prompt,
            model="gpt-4o-mini",
        )
        return result

    elif selected_model == "Google Gemini":
        analyzer = GeminiImageAnalyzer(api_key=cfg.gugol_key)
        result, tokens = analyzer.analyze_image(image_path=image_path, prompt=prompt)
        return f"""
        Token input: {tokens['input_tokens']}
        Token output: {tokens['output_tokens']}
        Token totali: {tokens['total_tokens']}

        Risposta: {result}
        """

    elif selected_model == "Anthropic Claude":
        analyzer = ClaudeImageAnalyzer(api_key=cfg.anthropic_key)
        result, token_usage = analyzer.analyze_image(image_paths=image_path, prompt=prompt)
        return f"""
        Token Usage: {token_usage}

        {result}
        """

    return "Errore: Modello non valido"


def open_browser():
    """Function to open the browser after a short delay"""
    time.sleep(2)  # Wait for 2 seconds to ensure the server is running
    webbrowser.open('http://127.0.0.1:7860')  # Default Gradio port


# Creazione dell'interfaccia Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Analizzatore di Immagini con AI")

    with gr.Group(visible=True) as main_interface:
        with gr.Row():
            with gr.Column():
                # Input immagine
                image_input = gr.Image(type="filepath", label="Carica un'immagine")

                # Selezione del modello
                model_selector = gr.Dropdown(
                    choices=["OpenAI GPT-4", "Google Gemini", "Anthropic Claude"],
                    label="Seleziona il modello di AI",
                    value="Google Gemini"
                )

                # Pulsante di invio
                submit_btn = gr.Button("Analizza Immagine")

                # Pulsante logout
                logout_btn = gr.Button("Logout", variant="secondary")

            with gr.Column():
                # Output della risposta
                output_text = gr.Textbox(label="Risultato dell'analisi", lines=10)

        # Collegamento analisi immagine
        submit_btn.click(
            fn=analyze_image,
            inputs=[image_input, model_selector],
            outputs=output_text
        )



# Avvio dell'applicazione
if __name__ == "__main__":
    # Start the browser opening function in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    # Launch the Gradio app
    demo.launch()
