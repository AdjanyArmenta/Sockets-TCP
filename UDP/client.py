import socket
import threading
import hashlib
import time
import os

# Configuración del servidor
IP_SERVIDOR = socket.gethostbyname(socket.gethostname())
PUERTO_SERVIDOR = 5000
DIR_SERVIDOR =  (IP_SERVIDOR, PUERTO_SERVIDOR)
BUFFER_SIZE = 4096

def main() -> None:
    print('''Envío de audio, imagen o video por medio de UPD
          
            Comandos:
          
            UPLOAD
                Comando para enviar archivos
                Uso:
                    UPLOAD <ruta_del_archivo>

            LOGOUT
                Finalizar la ejecución del programa
          ''')
    while True:
        input_usuario = input("> ")
        
        tokens_comando = input_usuario.strip().split(" ")
        
        if tokens_comando[0] == "LOGOUT":
            break
        elif tokens_comando[0] == "UPLOAD":
            if len(tokens_comando) >= 2:
                ruta_del_archivo = tokens_comando[1]

                if ruta_del_archivo_valida(ruta_del_archivo):
                    enviar_archivo_al_servidor(ruta_del_archivo) 
                else:
                    print(f"[ERROR]: No se pudo encontrar el archivo '{ruta_del_archivo}'")  
            else:
                print("[ERROR]: Debes proveer la ruta del archivo a enviar.")          
        
def ruta_del_archivo_valida(ruta_del_archivo: str) -> bool:
    return os.path.exists(ruta_del_archivo)

def enviar_archivo_al_servidor(ruta_del_archivo: str):
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    nombre_del_archivo = os.path.basename(ruta_del_archivo)
    socket_cliente.sendto(nombre_del_archivo.encode(), DIR_SERVIDOR)
    print("Enviando el archivo al servidor")

    with open(ruta_del_archivo, "rb") as archivo_a_enviar:
        while True:
            datos_fragmento = archivo_a_enviar.read(BUFFER_SIZE)
            if datos_fragmento:
                socket_cliente.sendto(datos_fragmento, DIR_SERVIDOR)
                time.sleep(0.2)
            else:
                break
    socket_cliente.sendto(b"EOF", DIR_SERVIDOR)
    socket_cliente.close()

    
if __name__ == "__main__":
    main()