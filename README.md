
# Django E-Commerce API

This project is a complete e-commerce RESTful API built with Django and Django REST Framework. It provides a full suite of features from user management and product listings to a complete cart, order, and asynchronous payment workflow.

## Features

-   **User Management**: JWT-based registration and login for Customers, Merchants, and Admins.
-   **Role-Based Permissions**: Granular access control for creating and managing resources.
-   **Product Catalog**: Full CRUD operations for products.
-   **AI Integration**: An endpoint to automatically generate product descriptions using the Gemini API.
-   **Shopping Cart**: Add, view, and remove items from a persistent user cart.
-   **Order System**: Convert a cart into a formal order with a price and item snapshot.
-   **Asynchronous Payments**: A mock payment system that simulates a real-world webhook confirmation flow.
-   **API Documentation**: Auto-generated interactive Swagger/OpenAPI documentation.
-   **Dockerized**: Fully containerized for consistent development and easy deployment to services like Render.

## Tech Stack

-   **Backend**: Django, Django REST Framework
-   **Database**: PostgreSQL
-   **Authentication**: Simple JWT (JSON Web Tokens)
-   **API Documentation**: drf-spectacular (Swagger/OpenAPI)
-   **Containerization**: Docker & Docker Compose
-   **Application Server**: Gunicorn

## Getting Started

### Local Development (without Docker)

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd ecommerce_project
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    -   Copy the `.env.example` to `.env` (or create it from scratch).
    -   Fill in your `SECRET_KEY`, `DATABASE_URL`,`JWT_KEY`, `DEBUG`,and `GEMINI_API_KEY`.
5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    -   API is available at `http://127.0.0.1:8000/`
    -   Swagger Docs are at `http://127.0.0.1:8000/docs/`

### Deployment to Render

1.  Push your code to a GitHub or GitLab repository.
2.  On the Render dashboard, create a new **Web Service**.
3.  Connect your repository.
4.  Render will automatically detect the `Dockerfile` and use it for the build.
5.  Under **Environment**, add your environment variables (`SECRET_KEY`, `GEMINI_API_KEY`, and `DATABASE_URL`).
    > **Important:** For `DATABASE_URL`, create a PostgreSQL database on Render and use the "Internal Connection String" that Render provides.
6.  Click **Create Web Service**. Render will build and deploy your application.