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

