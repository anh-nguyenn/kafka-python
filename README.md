# Kafka Python Implementation

A Python implementation of a Kafka-like message broker, built as part of the [CodeCrafters "Build Your Own Kafka" Challenge](https://codecrafters.io/challenges/kafka).

## Overview

This project implements a toy Kafka clone capable of accepting and responding to Kafka protocol requests. It demonstrates understanding of:

- Network programming with TCP sockets
- Binary data encoding/decoding using struct
- Kafka wire protocol basics
- Event loops and client-server communication

## Project Structure

```
kafka-python/
├── main.py          # Main Kafka broker implementation
├── README.md        # This file
└── .gitignore       # Git ignore rules
```

## Challenge Progress

### ✅ Stage 1: Basic Server Response

**Goal**: Create a server that listens on port 9092 and responds to any client request with a specific binary response.

**Implementation Details**:

The server implements the following behavior:
1. **Listen on port 9092**: Uses `socket.create_server()` to create a TCP server
2. **Accept client connections**: Handles incoming connections in a loop
3. **Read client requests**: Receives up to 1024 bytes from each client
4. **Send binary response**: Responds with an 8-byte binary message containing:
   - `message_size` (4 bytes): Set to 0 for this stage
   - `correlation_id` (4 bytes): Set to 7 (required by challenge)

**Response Format**:
```
Bytes 0-3:   message_size = 0    (big-endian 32-bit integer)
Bytes 4-7:   correlation_id = 7  (big-endian 32-bit integer)
```

**Binary Response**: `00 00 00 00 00 00 00 07`

## How to Run

### Prerequisites
- Python 3.8+ (required for `socket.create_server()`)
- netcat (nc) for testing

### Running the Server

1. Start the Kafka broker:
   ```bash
   python3 main.py
   ```

   You should see:
   ```
   Logs from your program will appear here!
   Server listening on localhost:9092
   ```

2. In another terminal, test the connection:
   ```bash
   # Basic test (no visible output)
   echo -n "test" | nc localhost 9092
   
   # Test with hex dump to see the response
   echo -n "test" | nc localhost 9092 | hexdump -C
   ```

### Expected Output

When a client connects, the server logs:
```
Client connected from ('127.0.0.1', 54321)
Received request: b'test'
Sent response: 0000000000000007
Client disconnected
```

The client receives the binary response: `00 00 00 00 00 00 00 07`

## Technical Implementation

### Socket Programming
- Uses Python's `socket` module for TCP communication
- `socket.create_server()` creates a server socket bound to localhost:9092
- `reuse_port=True` allows port reuse for testing

### Binary Data Handling
- Uses `struct.pack('>ii', message_size, correlation_id)` for big-endian encoding
- `'>ii'` format: two 32-bit signed integers in big-endian byte order
- Response is exactly 8 bytes as required by Kafka protocol

### Error Handling
- Basic exception handling for socket operations
- Graceful handling of client disconnections
- Server continues running after each client connection

## Testing

### Manual Testing
```bash
# Test 1: Basic connection
echo -n "hello" | nc localhost 9092

# Test 2: View binary response
echo -n "hello" | nc localhost 9092 | hexdump -C

# Test 3: Multiple connections
for i in {1..3}; do echo -n "test$i" | nc localhost 9092 & done
```

### Expected Test Results
- All connections should succeed
- Server should log each connection
- Each client should receive the same 8-byte response
- Response should be: `00 00 00 00 00 00 00 07`

## Code Explanation

### Key Components

1. **Server Setup**:
   ```python
   server = socket.create_server(("localhost", 9092), reuse_port=True)
   ```

2. **Client Handling Loop**:
   ```python
   while True:
       client_socket, address = server.accept()
       # Process client...
       client_socket.close()
   ```

3. **Binary Response Creation**:
   ```python
   message_size = 0
   correlation_id = 7
   response = struct.pack('>ii', message_size, correlation_id)
   ```

### Why This Works

- **TCP Socket**: Reliable, connection-oriented communication
- **Big-endian Format**: Matches Kafka protocol specification
- **Fixed Response**: Stage 1 only requires a simple acknowledgment
- **Sequential Processing**: Handles one client at a time (sufficient for Stage 1)

## Next Steps

Future stages will implement:
- ApiVersions request handling
- Fetch API requests
- Message storage and retrieval
- Topic management
- Producer/Consumer functionality

## Learning Outcomes

This implementation demonstrates:
- **Network Programming**: TCP socket server creation and management
- **Binary Protocols**: Understanding of byte-level data encoding
- **Client-Server Architecture**: Basic request-response pattern
- **Protocol Design**: Following established wire protocol standards

## References

- [CodeCrafters Kafka Challenge](https://codecrafters.io/challenges/kafka)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Python Struct Module](https://docs.python.org/3/library/struct.html)
- [Kafka Protocol Reference](https://kafka.apache.org/protocol.html)
