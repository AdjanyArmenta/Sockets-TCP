import socket
import threading
import hashlib
import os

# Configuración del servidor
IP_SERVIDOR = socket.gethostbyname(socket.gethostname())
PUERTO_SERVIDOR = 5000
DIR_SERVIDOR =  (IP_SERVIDOR, PUERTO_SERVIDOR)
BUFFER_SIZE = 4096
SERVER_DATA_PATH = "server_files"

# Función para calcular checksum
def calcular_checksum(data):
    return hashlib.md5(data).hexdigest()

# Función para manejar la recepción de archivos de un cliente
def manejar_cliente(nombre_archivo, socket_del_servidor, direccion_origen):
    try:
        ruta_destino_archivo = os.path.join(SERVER_DATA_PATH, nombre_archivo)
        
        with open(ruta_destino_archivo, 'wb') as archivo_en_transferencia:
            while True:
                data, _ = socket_del_servidor.recvfrom(BUFFER_SIZE)
               
                if not data or data == b"EOF":
                    break
                archivo_en_transferencia.write(data)
        
        print(f"{nombre_archivo} de {direccion_origen} recibido con éxito.")
    except Exception as e:
        print(f"Error con {direccion_origen}: {e}")

# Crear socket UDP
def main():
    socket_del_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_del_servidor.bind(DIR_SERVIDOR) 
    print(f"Servidor escuchando en {IP_SERVIDOR}:{PUERTO_SERVIDOR}")

    while True:
        try:
            data, dir_cliente = socket_del_servidor.recvfrom(BUFFER_SIZE)
            
            nombre_archivo = data.decode('utf-8', errors='ignore').strip()
            print(f"[INFO]: Recibiendo archivo: {nombre_archivo} de {dir_cliente}")
                
            manejar_cliente(nombre_archivo, socket_del_servidor, dir_cliente)
            

        except Exception as e:
            print(f"Error con {dir_cliente}: {e}")
        
        

if __name__ == "__main__":
    main()