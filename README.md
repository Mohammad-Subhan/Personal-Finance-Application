# Personal Finance Manager - Web Application

## Overview

The Personal Finance Manager is a web-based application designed to help users track their income, expenses, savings, and financial goals in one convenient place.

## Features

- **Account Dashboard**: Financial overview with key metrics
- **Transaction Tracking**: Record income/expenses with categories
- **Financial Reports**: Visual spending analysis

## Technologies

1. **Frontend**: React JS
2. **Backend**: Django
3. **Database**: PostgreSQL

## Setup

### Prerequisites
- Python
- Javascript

### Installation
Clone the repo:

```bash
git clone https://github.com/Mohammad-Subhan/Personal-Finance-Application.git
cd Personal-Finance-Application
```

#### Project Structure

```bash
Personal-Finance-Application/
│
├── backend/
│   ├── backend/
│   ├── finance/
│   ├── requirements.txt
│   ├── manage.py
│   ├── .venv
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── assets/
│   │   ├── lib/
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── App.jsx
│   │
│   ├── index.html
│   ├── package.json
│   ├── jsconfig.json
│   ├── manage.py
│   └── .gitignore
│
├── README.md
├── LICENSE
└── .gitignore
```

#### Run Backend

1. Move into `backend` directory
    ```bash
    cd backend
    ```

2. Add your PostgreSQL Credentials. Create a .env file and add
    ```bash
    HOST=your_host
    PORT=your_port
    USER=your_user
    PASSWORD=your_password
    NAME=your_name
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ```

3. Create the virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    .venv/Scripts/activate
    pip install -r requirements.txt
    ```

4. Apply migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Run the server
    ```bash
    python manage.py runserver
    ```

#### Run Frontend

1. Move into `frontend` directory:
    ```bash
    cd frontend
    ```

2. install dependencies:
    ```bash
    npm install
    ```

3. Run server:
    ```bash
    npm run dev
    ```


## 📄 License
This project is licensed under the MIT License.