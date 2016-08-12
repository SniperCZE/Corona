# v0.1
## Server
- Start and Stop
- Keep list of online agents
- Store agents info in MySQL
- TLS support for Agent - Server communication
- Ping-pong to each agent
## Agent
- Start and Stop
- Registration with Corona server
- TLS support for Agent - Server communication
- Response for ping-pong messages
- Send info about itself to server
## Frontend
- List of online agents
## Protocol
- JSON format
- Agent is online
- Info about agent
-- Agent version
-- Agent IP address
- Ping-Pong Agent-Server