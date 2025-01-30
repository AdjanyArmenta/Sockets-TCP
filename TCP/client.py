import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDRESS = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        
        if cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "UPLOAD":
            if len(data) < 2: 
                print("[ERROR]: You must provide a file path.")
                continue

            path = data[1].strip() 

            while not os.path.exists(path):  
                print(f"[ERROR]: The pathname '{path}' does not exist.")
                path = input("> UPLOAD ").strip()
                
                if path.lower() == "cancel":  
                    print("[INFO]: Upload canceled.")
                    break  

            if path.lower() == "cancel":
                continue  

            try:
                with open(path, "r") as f:
                    text = f.read() 

                filename = os.path.basename(path)
                send_data = f"{cmd}@{filename}@{text}"
                client.send(send_data.encode(FORMAT))
                print("[INFO]: File uploaded successfully.")  

            except Exception as e:
                print(f"[ERROR]: Could not read the file. {e}")
        else:
            print("[ERROR]: Invalid command.")

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()