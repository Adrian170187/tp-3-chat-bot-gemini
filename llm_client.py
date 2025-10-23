import time
from typing import Optional, List, Dict
from config import Settings
import google.generativeai as genai

class geminiCliente:
    def __init__(self,apikey:str,nombre_modelo:str):
        if not apikey:
            raise ValueError("API llaves es requerida")
        genai.configure(api_key=apikey)
        self.nombre_modelo=genai.GenerativeModel(nombre_modelo)
    def generar(
        self,
        prompts:str,
        historial:List[Dict[str,str]],
        mensaje_usuario:str,
        maximo_intentos:int,
        tiempo_restante:int
    ) ->str:
        intentos=0
        ultimo_error:Optional[Exception]=None
        combo=self.nombre_modelo.start_chat(
            historial=[{"role":"usuario","partes":prompts}]+
            [{"role":m["role"],"partes":m["partes"]}for m in historial]
            
        )
        while intentos < maximo_intentos:
            try:
                respuesta=combo.send_message(mensaje_usuario)
                texto= getattr(respuesta,'text',"")
                if not texto:
                    raise ValueError("Respuesta vacia del modelo")
                return texto
            except Exception as e:
                ultimo_error=e
                dormir=2**intentos
                time.sleep(dormir)
                intentos+=1
        raise RuntimeError("fallo maximo numero de intentos") from ultimo_error