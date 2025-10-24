from typing import Optional
from config import Settings
from roles import Role, roles_sistemas
from prompts import sistema_prompt, destruir_historial
from memory import Memory
from llm_client import geminiCliente

class ChatService:
    def __init__(self, rol: Role = Role.ASISTENTE):
        self.rol = rol
        self.memoria = Memory(max_length=Settings.max_history)

        # Validar API key antes de inicializar el cliente
        if not Settings.gemini_api_key:
            raise ValueError("API key de Gemini no configurada. Verifica tu archivo .env y config.py.")

        # Crear el cliente Gemini
        self.cliente = geminiCliente(
            apikey=Settings.gemini_api_key,  # 👈 corregido
            nombre_modelo=Settings.model,
        )


    def preguntar(self, prompt: str) -> str:
        """Envía un mensaje al modelo Gemini con historial y contexto del rol."""
        system_prompt = sistema_prompt(roles_sistemas[self.rol])
        historial = destruir_historial(self.memoria.get_memory())

        respuesta = self.cliente.generar(  # 👈 nombre corregido
            prompts=system_prompt,
            historial=historial,
            mensaje_usuario=prompt,
            maximo_intentos=Settings.max_retries,
            tiempo_restante=Settings.timeout_seconds,
        )

        # Guardar los mensajes en memoria
        self.memoria.add_message(prompt)
        self.memoria.add_modelo(respuesta)

        return respuesta


    def reiniciar(self):
        """Borra el historial de conversación."""
        self.memoria.clear_memory()

    def cambiar_rol(self, nuevo_rol: Role):
        """Actualiza el rol actual del asistente."""
        self.rol = nuevo_rol
