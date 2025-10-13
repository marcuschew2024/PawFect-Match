# PawFect Match 🐾

A full-stack pet adoption platform that helps users find their perfect furry companions. Built with Vue.js frontend and Flask Python backend with Supabase database.

![PawFect Match](https://cdn-icons-png.flaticon.com/512/616/616430.png)

## 🚀 Features

- **Browse Pets** - View all available pets with beautiful cards
- **Advanced Filtering** - Filter by size, age, gender, and search
- **Responsive Design** - Mobile-first design that works on all devices
- **Real-time Search** - Instant search with debounced input
- **Lazy Loading** - Optimized image loading with placeholder system
- **RESTful API** - Clean Flask backend API with Supabase database

## 🛠 Tech Stack

**Frontend:**
- Vue 3 + Vue Router
- Bootstrap 5 + Bootstrap Icons
- Axios for API calls

**Backend:**
- **Flask** (Python) - Web framework
- **Supabase** (PostgreSQL) - Database
- **Requests** - HTTP library for API calls
- **Flask-CORS** - Cross-Origin Resource Sharing

**APIs:**
- The Dog API & The Cat API for placeholder images

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js (v16 or higher) for frontend
- Supabase account

### Backend Setup (Flask Python)

1. Navigate to backend directory:
```bash
cd backend

pip install -r requirements.txt

cp .env.example .env

python app.py
```

### Frontend Setup 
```bash
cd frontend

npm install

npm run dev
```