# Trading REST API Service

A robust and efficient RESTful API designed to facilitate trading operations, including strategy management and order execution.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Redis](#redis-setup-via-docker)

## Features

- **Strategy Management**: Create, update, and manage trading strategies.
- **Order Execution**: Execute buy and sell orders seamlessly.
- **Real-time Data Processing**: Handle real-time market data for informed decision-making.
- **User Authentication**: Secure user authentication and authorization mechanisms.

## Technologies Used

- **Programming Language**: Python
- **Framework**: Flask
- **Database**: PostgreSQL
- **Message Broker**: RabbitMQ
- **Caching**: Redis
- **Containerization**: Docker

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL
- RabbitMQ
- Redis
- Docker (optional, for containerization)

## Quickstart

1. **Setup Environment Variables**
   - Create a `.env` file in the project root with the following variables:
     ```env
     DB_HOST=localhost
     DB_PORT=5432
     DB_USER=your_user
     DB_PASS=your_password
     DB_NAME=your_database
     SECRET_KEY=your_secret_key
     ```

2. **Install Dependencies**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Start PostgreSQL, RabbitMQ, Redis**
   - Ensure PostgreSQL(don't forget to create DB), RabbitMQ, Redis are running locally or in Docker.

4. **Run the Application**
   ```bash
   python main.py
   ```
   
## Redis setup via Docker

1. **Pull Redis Image**
    ```bash
    docker pull redis
    ```
2. **Run Redis Container**
    ```bash
    docker run -d --name redis -p 6379:6379 redis
    ```
3. **Check connection**
    ```bash
    docker exec -it redis redis-cli
    ```
    Write
    ```bash
    ping
    ```
    Expected response: ```PONG```

