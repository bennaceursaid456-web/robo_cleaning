import requests
import threading

class OllamaService:
    def __init__(self, model="llama3"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def ask_async(self, label, callback):
        """
        Starts a background thread to ask Ollama for advice.
        calls `callback(advice_text)` when done.
        """
        thread = threading.Thread(target=self._run_request, args=(label, callback))
        thread.daemon = True
        thread.start()

    def _run_request(self, label, callback):
        prompt = (
            f"You are AquaMind, an advanced water cleaning robot. "
            f"You just detected a '{label}' in the water. "
            f"Provide a 1-sentence scientific suggestion on how to handle it or why it is dangerous. "
            f"Do not use markdown. Keep it scientific but urgent."
        )

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            # Timeout of 10s to not hang forever
            response = requests.post(self.api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                text = response.json().get("response", "").strip()
                callback(text)
            else:
                callback(f"Error: AI unavailable (Status {response.status_code})")
                
        except Exception as e:
            print(f"⚠️ Ollama Error: {e}")
            callback("Error: active AI connection failed.")
