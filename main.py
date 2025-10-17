import socket  
import struct


def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    print("Server listening on localhost:9092")
    
    while True:
        client_socket, address = server.accept()
        print(f"Client connected from {address}")
        
        request = client_socket.recv(1024)
        print(f"Received request: {request}")
        
        message_size = 0  
        correlation_id = 7  
        
        response = struct.pack('>ii', message_size, correlation_id)
        
        client_socket.send(response)
        print(f"Sent response: {response.hex()}")
        
        client_socket.close()
        print("Client disconnected")


if __name__ == "__main__":
    main()
