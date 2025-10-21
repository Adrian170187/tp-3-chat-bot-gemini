import sys
from roles import RolesPreset
from config import Settings
from chat_service import ChatService
from dotenv import load_dotenv
import os

load_dotenv()

print(f"appi kay: {Settings.gemini_api_key}")

def escoger_rol()-> RolesPreset:
    print("Seleccione un rol para el chatbot:")
    print("1. Asistente amigable")
    print("2. Experto técnico")
    print("3. Compañero creativo")
    eleccion = input("Ingrese el número correspondiente al rol deseado: ")
    
    mapa={
        "1": RolesPreset.PROFESOR,
        "2": RolesPreset.TRADUCTOR,
        "3": RolesPreset.PROGRAMADOR,
        "4": RolesPreset.ASISTENTE, 
        }
    return mapa.get(eleccion, RolesPreset.ASISTENTE)

def comando_ayuda():
    print("\nComandos disponibles:")
    print(":rol profesor|traductor|programador|asistente - Cambia el rol actual")
    print(":reset - Reinicia la conversación")
    print(":exit - Salir de la aplicación")
    
def main():
    rol = escoger_rol()
    chat=ChatService(rol)
    comando_ayuda()
    while True:
        try:
            entrada = input("\nTú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo de la aplicación. ¡Hasta luego!")
            break   
        if not entrada:
            continue    
        if entrada.lower() in (":exit", "salir"):
            print("Saliendo de la aplicación. ¡Hasta luego!")
            break
        if entrada.lower() in (":reset","reiniciar"):
            chat.reset_conversation()
            print("Conversación reiniciada.")
            continue
        if entrada.lower().startswith(":rol"):
            nuevo_rol_entrada = entrada[5:].strip().upper()
            mapa_roles = {
                "PROFESOR": RolesPreset.PROFESOR,
                "TRADUCTOR": RolesPreset.TRADUCTOR,
                "PROGRAMADOR": RolesPreset.PROGRAMADOR,
                "ASISTENTE": RolesPreset.ASISTENTE,
            }
            if nuevo_rol_entrada in mapa_roles:
                chat.set_role(mapa_roles[nuevo_rol_entrada])
                print(f"Rol cambiado a {nuevo_rol_entrada.lower()}.")
            else:
                print("Rol no reconocido. Los roles disponibles son: profesor, traductor, programador, asistente.")
            continue
        if entrada.lower() in (":help","ayuda"):
            comando_ayuda()
            continue
        try:
            respuesta = chat.enviar_mensaje(entrada)
            print(f"Chatbot: {respuesta}")
        except Exception as e:
            print(f"Error al obtener respuesta del chatbot: {e}")
if __name__ == "__main__":
    main()