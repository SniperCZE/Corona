# Corona
Central management tool for HAProxy infrastructuries

## Basic overview of Corona

Corona project is central management tool for cluster of HAProxy nodes. It compounds from 3 separated parts - Agents, Server and Frontend.

### Agent
Corona uses Agents, which communicates with server. Agent takes status info from HAProxy and perform commands sended by Server. Every HAProxy node must have deployed Agent on itself. Agent must be properly configured, at least path to HAProxy management socket and address of Corona server.

### Server
Server is central part of Corona enviroment. Server has internal database with all active Agents and its state, is preparing data from Frontend and sends commands to Agents.

### Frontend
Frontend is PHP-based application, which shows data from Corona server and allow to perform management commands on Agents.

## Instalation of Corona enviroment

### Preinstall requirments

### How to install
#### Install from debian package
#### Install from source

## Troubleshooting
