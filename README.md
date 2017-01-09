# Corona
Central management tool for HAProxy infrastructures

## Basic overview of Corona

Corona project is central management tool for cluster of HAProxy nodes. It compounds from 3 separated parts - Agents, Server and Frontend.

### Agent
Corona uses Agents, which communicates with server. Agent takes status info from HAProxy and perform commands sended by Server. Every HAProxy node must have deployed Agent on itself in basic setup. Agent must be properly configured, at least path to HAProxy management socket and address of Corona server. Is possible to setup Agent-less enviroment, but it's not recommended!

### Server
Server is central part of Corona enviroment. Server has internal database with all active Agents and its state, is preparing data from Frontend and sends commands to Agents.

### Frontend
Frontend is PHP-based application, which shows data from Corona server and allow to perform management commands on Agents.

## Instalation of Corona enviroment

### Preinstall requirments

#### Agent
* Python 3
* HAProxy with enabled admin unix socket (see https://cbonte.github.io/haproxy-dconv/configuration-1.5.html#9.2)

#### Server
* Python 3
* MySQL

#### Frontend
* Webserver
* PHP 7.0
* Pdo driver for MySQL

### How to install
#### Install from debian package
#### Install from source

## Troubleshooting
