# 🛒 E-Commerce API with AI Integration

A modular **Django-based RESTful API** for managing core e-commerce functionalities—products, users, orders, and payments—with **AI-assisted product description generation**.  
The system is containerized with **Docker Compose** and deployed to **Render**.

---

## 📌 Project Overview
**Goal:** Build a scalable and extendable e-commerce API that supports CRUD operations, search, authentication, and AI-powered features.  
**Timeline:** 4 weeks (MVP focused).  
**AI Feature:** Integration with **Gemini Flash 2.5 API** to auto-generate product descriptions.

---

## 🚀 Features

### **1. Product Management** (`product-service`)
- Create, Read, Update, Delete products
- Search products by name or category
- AI-assisted product description generation (via `/products/{id}/generate-description`)

### **2. User Management** (`user-service`)
- User registration & JWT authentication
- Profile retrieval
- Role-based access control (Admin / Customer)

### **3. Order & Cart** (`order-service`)
- Add/remove items to cart
- Place orders
- View order history

### **4. Payment Simulation** (`payment-service`)
- Mock payment endpoint
- Asynchronous confirmation via **Celery + Redis**

### **5. AI Integration**
- External AI API: **Gemini Flash 2.5**
- Generates or enhances product descriptions
- Input: product title, category, key features

### **6. Documentation & Testing**
- Swagger/OpenAPI documentation for each service
- Unit tests for core endpoints
- Docker Compose orchestration

---

## 📡 External APIs
### **AI API**
- **Endpoint:** `POST /v1/chat/completions`
- **Purpose:** Generate product descriptions
- **Data:** `{ title, category, features }`

### **Optional: Category Data API**
- Example: *eBay Taxonomy API* for category validation  
- Implemented only if core tasks are completed ahead of time

---

## 🗂 Project Structure

**Services Orchestrated by Docker Compose:**
- `product-service` (Products CRUD, Search, AI generation)
- `user-service` (Auth, Profiles, Roles)
- `order-service` (Cart, Orders)
- `payment-service` (Mock Payments)
- `redis` & `rabbitmq` for async processing

---

### **1. product-service**
**Model:**
Product(id, name, category, price, description, stock)
## 📍 Endpoints & Models

### **1. product-service**
**Endpoints:**
- `GET /products/`
- `GET /products/{id}/`
- `POST /products/`
- `PUT /products/{id}/`
- `DELETE /products/{id}/`
- `GET /products/search/?q=&category=`
- `POST /products/{id}/generate-description/`

---

### **2. user-service**
**Model:**
User(id, username, email, password, role)
**Endpoints:**
- `POST /auth/register/`
- `POST /auth/login/` → returns JWT
- `GET /users/{id}/`

---

### **3. order-service

**Models:**
CartItem(user, product, quantity)
Order(user, items, total, status)
**Endpoints:**
- `GET /cart/`
- `POST /cart/`
- `DELETE /cart/{item_id}/`
- `POST /orders/`
- `GET /orders/`

---

### **4. Payment Service

**Model:**
- **Payment** (`order`, `status`, `timestamp`)

**Endpoints:**
- `POST /payments/` — mock payment request
- `GET /payments/{id}/` — retrieve payment details

---

## 🗄 Database Schema

| Service         | Table       | Key Fields                                             |
|-----------------|-------------|--------------------------------------------------------|
| product-service | Product     | `id` (PK), `name`, `category`, `price`, `description` |
| user-service    | User        | `id` (PK), `username`, `email`, `password_hash`, `role` |
| order-service   | CartItem    | `id` (PK), `user_id` (FK), `product_id` (FK), `qty`    |
| order-service   | Order       | `id` (PK), `user_id` (FK), `total`, `status`          |
| payment-service | Payment     | `id` (PK), `order_id` (FK), `status`, `timestamp`     |

**Relationships:**
- **User ⇄ CartItem** (1:M)
- **User ⇄ Order** (1:M)
- **Order ⇄ CartItem** (M:M via intermediate records)
- **Order ⇄ Payment** (1:1)

---

## 📅 Development Timeline

**Week 1 – Setup & Core Models**
- Initialize Git repo & Docker Compose
- Scaffold Django services
- Define models & migrations for product & user services
- Implement CRUD for products & user authentication

**Week 2 – Search, Orders & Cart**
- Implement search in product-service
- Scaffold order-service
- Write unit tests for products & cart
- Integrate JWT authentication

**Week 3 – Payment & AI**
- Build payment-service mock flow
- Setup Celery + Redis
- Integrate Gemini API for product descriptions
- Add Swagger/OpenAPI documentation

**Week 4 – Testing & Deployment**
- End-to-end testing
- Setup CI/CD via GitHub Actions
- Deploy to Render
- Final documentation & presentation

---

## 🛠 Tech Stack

- **Backend:** Django REST Framework  
- **AI Integration:** Gemini Flash 2.5 API  
- **Authentication:** JWT  
- **Async Processing:** Celery + Redis  
- **Deployment:** Docker Compose, Render  
- **Documentation:** Swagger/OpenAPI  
- **Database:** PostgreSQL

