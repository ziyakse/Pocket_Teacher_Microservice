## Distributed Architecture & Communication Design

This project has been upgraded to a distributed microservice architecture:

1. **API Gateway (Nginx):** Acts as the single entry point for all clients. It routes `/api/auth` requests to the Auth Service and all other `/api/*` (learning, AI, finance) requests to the Core Service.
2. **Auth Service (FastAPI):** A dedicated service handling user authentication. It issues **JWT (JSON Web Tokens)** for stateless authorization.
3. **Core Service (Flask):** The main learning engine containing curriculum logic, AI quiz generation (Gemini API), and financial transactions.
4. **Notification Service:** A background worker service.
5. **Service-to-Service Communication:**
   * **REST (Synchronous):** Handled via the API Gateway routing requests directly to the respective services.
   * **Asynchronous Messaging (RabbitMQ):** Used to decouple heavy or external tasks. For example, when a user makes a purchase that supports another student (`finance.py`), the Core Service publishes a `SOCIAL_IMPACT` event to RabbitMQ. The Notification Service consumes this event asynchronously to send emails, ensuring the Core Service remains fast and non-blocking.


   graph TD
    Client((Mobil / Web İstemci)) -->|REST API İstekleri| Gateway[API Gateway - Nginx]
    
    Gateway -->|/api/auth/*| Auth[Auth Service - FastAPI]
    Gateway -->|/api/*| Core[Core Service - Flask]
    
    Auth -->|1. JWT Token Üretir| Auth
    Auth -.->|2. Async Event: USER_LOGIN| RMQ[(RabbitMQ)]
    
    Core -->|1. AI Soru Üretimi / Sosyal Etki| Core
    Core -.->|2. Async Event: SOCIAL_IMPACT| RMQ
    
    RMQ -.->|Mesajları Tüketir| Notify[Notification Service - Python]
    Notify -->|E-posta / Push Gönderir| User((Kullanıcı))


    ## Distributed System & Communication Design

To ensure scalability and maintainability, Pocket Teacher has been refactored from a monolithic application into a microservice-based distributed system.

### Services Designed
1. **API Gateway (Nginx):** Acts as the single entry point. It uses path-based routing (`/api/auth/` -> Auth Service, `/api/` -> Core Service).
2. **Auth Service (FastAPI):** A dedicated microservice for user identity. It handles authentication and issues JWTs (JSON Web Tokens) for stateless authorization. It provides out-of-the-box OpenAPI documentation.
3. **Core Service (Flask):** The main learning engine containing curriculum logic, Gemini AI integration, and transaction management.
4. **Notification Service (Python):** An asynchronous background worker that handles email simulations and logging.

### Service-to-Service Communication
* **Synchronous (REST):** The API Gateway communicates with the backend services synchronously over HTTP/REST. External clients receive immediate responses for queries like login or AI quiz generation.
* **Asynchronous Messaging (RabbitMQ):** Used to decouple non-blocking operations. 
  - *Example 1:* When a user logs in via the Auth Service, a `USER_LOGIN` event is published to RabbitMQ.
  - *Example 2:* When a student purchases a premium tier that supports a disadvantaged student (Social Impact feature in Core Service), a `SOCIAL_IMPACT` event is published. 
  - The **Notification Service** consumes these events from the message broker and processes them in the background, ensuring the main application threads are never blocked by email or notification dispatching.