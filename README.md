# 🏥 InsureMate - Insurance Premium Predictor

InsureMate is an intelligent web application designed to predict insurance premium categories based on user health and lifestyle data. It utilizes a machine learning model to classify users into varying premium tiers (Basic, Standard, Premium, Elite), providing instant feedback and risk analysis.

## 🚀 Live Demo
**[Launch InsureMate App]((https://insuremate-live-frontend.onrender.com/)**  
*(Replace with your actual deployed URL if different)*

---

## 🛠️ Tech Stack

### **Frontend**
- **[Streamlit](https://streamlit.io/)**: For building a responsive and interactive user interface.
- **Visuals**: Dynamic charts and real-time feedback.

### **Backend**
- **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance, modern web framework for building APIs.
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation and settings management.

### **Database & Storage**
- **[PostgreSQL](https://www.postgresql.org/)**: Robust relational database for storing prediction history.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: SQL toolkit and ORM.
- **Alembic**: Database migration tool.

### **Machine Learning**
- **[Scikit-Learn](https://scikit-learn.org/)**: Powering the core prediction model (`model.pkl`).

### **DevOps & Deployment**
- **Docker**: For containerized consistency across environments.
- **Render**: Cloud platform for deployment.

---

## 📂 Project Structure

Verified modular architecture for scalability and maintainability:

```text
InsureMate/
├── insuremate/             # Core Backend Package
│   ├── api/                # API Route Handlers (Endpoints)
│   ├── core/               # Configuration & Settings
│   ├── db/                 # Database Layer (Models, Session, CRUD)
│   ├── services/           # Business Logic & ML Inference
│   ├── schemas.py          # Pydantic Data Models
│   └── main.py             # Application Entrypoint
├── data/                   # ML Models & Artifacts
├── scripts/                # Build & Deployment Scripts
├── tests/                  # Automated Tests
├── frontend.py             # Streamlit Frontend Entrypoint
├── docker-compose.yml      # Container Orchestration
└── render.yaml             # Render Deployment Config
```

---

## 💻 How to Run Locally

### Option 1: Using Docker (Recommended)
The easiest way to run the full stack (Frontend + Backend + Database).

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishxesh10/InsureMate-LIve.git
   cd InsureMate-LIve
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the App:**
   - 🖥️ **Frontend**: [http://localhost:8501](http://localhost:8501)
   - 🔌 **Backend API**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

### Option 2: Manual Python Setup

**Prerequisites:** Python 3.11+, PostgreSQL (optional, defaults to SQLite locally)

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend:**
   ```bash
   uvicorn insuremate.main:app --reload
   ```

4. **Run the Frontend (in a new terminal):**
   ```bash
   streamlit run frontend.py
   ```

---

## 🔑 Environment Variables
Create a `.env` file in the root directory if you need to override defaults:

```ini
DATABASE_URL=postgresql://user:pass@localhost/dbname
MODEL_PATH=data/model.pkl
API_BASE_URL=http://localhost:8000
```

---

## 🧪 Running Tests
To ensure everything is working correctly:

```bash
pytest
```
