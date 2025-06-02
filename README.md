# Aqua API Test Automation Infrastructure

A REST API server and Python client for automated testing infrastructure, built with FastAPI. This system allows test engineers to create and manage user data through a simulated server environment with in-memory storage.

## 📋 Table of Contents

* [Overview](#overview)
* [Project Structure](#project-structure)
* [Requirements](#requirements)
* [Installation](#installation)
* [Running the Application](#running-the-application)
* [API Endpoints](#api-endpoints)
* [Client Usage](#client-usage)
* [Testing](#testing)
* [Docker Support](#docker-support)
* [Design Decisions](#design-decisions)
* [Potential Improvements](#potential-improvements)

## 🌟 Overview

This project implements:

* **REST API Server**: FastAPI-based server with in-memory user storage
* **Python Client**: Easy-to-use client interface for test automation
* **Comprehensive Testing**: Full test suite with pytest
* **Docker Support**: Containerized deployment option

## 📁 Project Structure

```
aqua-api/
├── api/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── auth.py             # Basic authentication logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_model.py       # User data model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── public_router.py    # Health endpoint
│   │   └── user_routes.py      # API endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py      # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── user_service.py     # Business logic
├── client.py                  # Client demo script
├── client/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Client configuration
│   │   └── logger.py           # Client logging
│   └── services/
│       ├── __init__.py
│       └── client_service.py   # API client functions
├── tests/
│   ├── __init__.py
│   └── test_api.py             # API test suite
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
└── README.md                   # This file
```

## 🔧 Requirements

* Python 3.11+
* pip (Python package manager)
* Docker (optional, for containerization)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd aqua-api
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
requests==2.31.0
pytest==7.4.3
httpx==0.25.2
```

## 🏃 Running the Application

### Start the Server

```bash
# From project root
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

### API Documentation

FastAPI automatically generates interactive API documentation:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

### Run the Client Demo

In a new terminal:

```bash
python client.py
```

## 📡 API Endpoints

### Health Check

* **GET** `/health`
* Returns: `{"status": "healthy", "service": "aqua-api"}`

### Create User

* **POST** `/users`
* Body:

  ```json
  {
    "israel_id": "123456789",
    "name": "John Doe",
    "phone_number": "+972501234567",
    "address": "123 Main St, Tel Aviv"
  }
  ```
* Returns: Created user with assigned `user_id`

### Get User by ID

* **GET** `/users/{user_id}`
* Returns: User details or 404 if not found

### List All User IDs

* **GET** `/users`
* Returns: Array of user IDs

## 💻 Client Usage

### Basic Usage

```python
from client.services.client_service import create_user, get_user, list_users, health_check

# Health check
status = health_check()
print(status)

# Create user
new_user = create_user(
    israel_id="123456789",
    name="Test User",
    phone_number="+972501234567",
    address="123 Test St"
)
print(new_user)

# Get user
user = get_user(1)
print(user)

# List all users
user_ids = list_users()
print(user_ids)
```

### Configuration

The client reads configuration from environment variables:

```bash
# Set custom server URL (default: http://127.0.0.1:8000)
export SERVER_URL=http://your-server:8000
```

## 🫖 Testing

Run the test suite:

```bash
pytest
```

## 🐳 Docker Support

### Build the Image

```bash
docker build -t aqua-api .
```

### Run the Container

```bash
docker run -p 8000:8000 aqua-api
```

## 🎨 Design Decisions

* FastAPI and Pydantic for fast development and validation
* Modular design: clear separation of API, business logic, and data models
* Logging in both server and client using custom logger
* Docker support for consistent deployment

## 🚀 Potential Improvements

* Migrate from in-memory storage to a persistent DB (PostgreSQL, MongoDB)
* Add Redis caching for performance
* Add proper authentication (OAuth2, API key, JWT)
* Integrate CI/CD for testing and linting
* Add tests for edge cases and error paths
* Enable request/response logging middleware
* Introduce HTTPS/SSL in production
* Provide update/delete endpoints and pagination/filtering