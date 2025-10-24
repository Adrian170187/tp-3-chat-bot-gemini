from collections import deque
from typing import Deque, List, Dict

class Memory:
    def __init__(self, max_length: int = 10):
        self.memory: Deque[Dict[str, str]] = deque(maxlen=max_length)

    def add_message(self, contenido: str):
        # El usuario siempre se guarda con role "user"
        self.memory.append({"role": "user", "parts": [contenido]})

    def add_modelo(self, contenido: str):
        # El modelo siempre se guarda con role "model"
        self.memory.append({"role": "model", "parts": [contenido]})

    def get_memory(self) -> List[Dict[str, str]]:
        return list(self.memory)

    def clear_memory(self):
        self.memory.clear()
