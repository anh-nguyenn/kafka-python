# Kafka Python Implementation

A Python implementation of a Kafka-like message broker

## Stage 2: Request Parsing

Parse Kafka request messages to extract correlation_id and use it in responses.

### Request Format

```
message_size (4 bytes) + request_api_key (2 bytes) + request_api_version (2 bytes) + correlation_id (4 bytes) + ...
```

### Response Format

```
message_size (4 bytes) + correlation_id (4 bytes)
```

### Implementation

- Parses request header v2 to extract correlation_id
- Uses extracted correlation_id in response
- Falls back to default correlation_id=7 if parsing fails

### Testing

```bash
# Start server
python3 main.py

# Test with example request
echo -n "00000023001200046f7fc66100096b61666b612d636c69000a6b61666b612d636c6904302e3100" | xxd -r -p | nc localhost 9092 | hexdump -C
```

Expected response: `00 00 00 00 6f 7f c6 61`
