from roles import Role
from config import Settings
from chat_service import ChatService
from dotenv import load_dotenv

load_dotenv()

print(f"appi kay: {Settings.gemini_api_key}")

def escoger_rol()-> Role:
    print("Seleccione un rol para el chatbot:")
    print("1. Asistente amigable")
    print("2. Experto técnico")
    print("3. Compañero creativo")
    eleccion = input("Ingrese el número correspondiente al rol deseado: ")
    
    mapa={
        "1": Role.PROFESOR,
        "2": Role.TRADUCTOR,
        "3": Role.PROGRAMADOR,
        "4": Role.ASISTENTE, 
        }
    return mapa.get(eleccion, Role.ASISTENTE)

def comando_ayuda():
    print("\nComandos disponibles:")
    print(":rol profesor|traductor|programador|asistente - Cambia el rol actual")
    print(":reset - Reinicia la conversación")
    print(":exit - Salir de la aplicación")
    
def main():
    rol = escoger_rol()
    chat=ChatService()
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
            chat.reiniciar()
            print("Conversación reiniciada.")
            continue
        if entrada.lower().startswith(":rol"):
            nuevo_rol_entrada = entrada[5:].strip().upper()
            mapa_roles = {
                "PROFESOR": Role.PROFESOR,
                "TRADUCTOR": Role.TRADUCTOR,
                "PROGRAMADOR": Role.PROGRAMADOR,
                "ASISTENTE": Role.ASISTENTE,
            }
            if nuevo_rol_entrada in mapa_roles:
                chat.cambiar_rol(mapa_roles[nuevo_rol_entrada])
                print(f"Rol cambiado a {nuevo_rol_entrada.lower()}.")
            else:
                print("Rol no reconocido. Los roles disponibles son: profesor, traductor, programador, asistente.")
            continue
        if entrada.lower() in (":help","ayuda"):
            comando_ayuda()
            continue
        
        respuesta = chat.preguntar(entrada)
        print(f"Chatbot: {respuesta}")

if __name__ == "__main__":
    main()
    