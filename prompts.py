from typing import List, Dict

def sistema_prompt(instruciones: str) -> str:
    base=("Sos un Chatbot de terminal que responde en español latino de forma concisa y clara",
          "si el usuario solicita algo incluir explicaiones breves y ejemplos",)
    
    return  f"{base} contexto de instrucciones: {instruciones}"
def destruir_historial(historial:list[Dict[str,str]])-> list[Dict[str,str]]:
    return historial