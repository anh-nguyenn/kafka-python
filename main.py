import socket  
import struct


def parse_request(request_data):
    """
    Parse Kafka request message to extract correlation_id.
    
    Request format:
    - message_size (4 bytes): INT32
    - request_api_key (2 bytes): INT16  
    - request_api_version (2 bytes): INT16
    - correlation_id (4 bytes): INT32
    - client_id (nullable string): variable length
    - TAG_BUFFER (compact array): variable length
    """
    if len(request_data) < 12:  # Minimum: message_size(4) + api_key(2) + api_version(2) + correlation_id(4)
        return None
    
    offset = 0
    
    # Parse message_size (4 bytes)
    message_size = struct.unpack('>i', request_data[offset:offset+4])[0]
    offset += 4
    
    # Parse request_api_key (2 bytes)
    request_api_key = struct.unpack('>h', request_data[offset:offset+2])[0]
    offset += 2
    
    # Parse request_api_version (2 bytes)
    request_api_version = struct.unpack('>h', request_data[offset:offset+2])[0]
    offset += 2
    
    # Parse correlation_id (4 bytes)
    correlation_id = struct.unpack('>i', request_data[offset:offset+4])[0]
    offset += 4
    
    print(f"Parsed request - message_size: {message_size}, api_key: {request_api_key}, api_version: {request_api_version}, correlation_id: {correlation_id}")
    
    return correlation_id


def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    print("Server listening on localhost:9092")
    
    while True:
        client_socket, address = server.accept()
        print(f"Client connected from {address}")
        
        request = client_socket.recv(1024)
        print(f"Received request: {request.hex()}")
        
        # Parse the request to extract correlation_id
        correlation_id = parse_request(request)
        
        if correlation_id is not None:
            message_size = 0  # Any value works for this stage
            response = struct.pack('>ii', message_size, correlation_id)
            print(f"Using correlation_id from request: {correlation_id}")
        else:
            # Fallback to hardcoded value if parsing fails
            message_size = 0
            correlation_id = 7
            response = struct.pack('>ii', message_size, correlation_id)
            print(f"Failed to parse request, using default correlation_id: {correlation_id}")
        
        client_socket.send(response)
        print(f"Sent response: {response.hex()}")
        
        client_socket.close()
        print("Client disconnected")


if __name__ == "__main__":
    main()
