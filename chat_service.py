from typing import Optional
from config import Settings
from roles import Role, roles_sistemas
from prompts import sistema_prompt, destruir_historial
from memory import Memory
from llm_client import geminiCliente

class ChatService:
    def _init_(self, rol: Role = Role.ASISTENTE):
        self.rol = rol
        self.memoria = Memory(max_messages=Settings.max_history)

        # Validar API key antes de inicializar el cliente
        if not Settings.api_key:
            raise ValueError("API key de Gemini no configurada. Verifica tu archivo .env y config.py.")

        # Crear el cliente Gemini
        self.cliente = geminiCliente(
            api_key=Settings.api_key,
            model_name=Settings.model,
        )

    def preguntar(self, prompt: str) -> str:
        """Envía un mensaje al modelo Gemini con historial y contexto del rol."""
        system_prompt = sistema_prompt(
            roles_sistemas[self.rol]
        )
        historial = destruir_historial(self.memoria.get())

        respuesta = self.cliente.generate(
            system_prompt=system_prompt,
            user_message=prompt,
            history=historial,
            max_retries=Settings.max_retries,
            timeout_seconds=Settings.timeout_seconds,
        )

        self.memoria.add_user_message(prompt)
        self.memoria.add_model(respuesta)
        return respuesta

    def reiniciar(self):
        """Borra el historial de conversación."""
        self.memoria.clear()

    def cambiar_rol(self, nuevo_rol: Role):
        """Actualiza el rol actual del asistente."""
        self.rol = nuevo_rol