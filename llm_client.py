import time
from typing import Optional, List, Dict
import google.generativeai as genai

class geminiCliente:
    def __init__(self, apikey: str, nombre_modelo: str):
        if not apikey:
            raise ValueError("API key es requerida para usar Gemini.")
        genai.configure(api_key=apikey)
        self.modelo = genai.GenerativeModel(nombre_modelo)

    def generar(
        self,
        prompts: str,
        historial: List[Dict[str, str]],
        mensaje_usuario: str,
        maximo_intentos: int,
        tiempo_restante: int
    ) -> str:
        intentos = 0
        ultimo_error: Optional[Exception] = None

        # 🧩 Construcción correcta del historial
        chat_historial = [{"role": "user", "parts": [prompts]}]
        for m in historial:
            role = m.get("role", "user")
            if role not in ["user", "model"]:  # 🔒 seguridad
                role = "user"
            parts = m.get("parts", [m.get("content", "")])
            chat_historial.append({"role": role, "parts": parts})

        # 🧠 Iniciar el chat con historial válido
        chat = self.modelo.start_chat(history=chat_historial)

        while intentos < maximo_intentos:
            try:
                respuesta = chat.send_message(mensaje_usuario)
                texto = getattr(respuesta, "text", "")
                if not texto:
                    raise ValueError("Respuesta vacía del modelo.")
                return texto
            except Exception as e:
                ultimo_error = e
                print(f"Intento {intentos+1} fallido: {e}")
                time.sleep(2 ** intentos)
                intentos += 1

        raise RuntimeError("Falló el número máximo de intentos") from ultimo_error
