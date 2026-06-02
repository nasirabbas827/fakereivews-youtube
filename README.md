# fakereivewsproject‑youtube  

A Django‑based web application that detects fake product reviews on YouTube‑related e‑commerce data. The project demonstrates end‑to‑end pipelines for data ingestion, model inference, and a simple UI for visualising authentic vs. fraudulent reviews.

---

## Overview  

- **Goal** – Identify and flag potentially fake reviews using a pre‑trained detection model.  
- **Scope** – Upload product images, view review details, and see model predictions in real time.  
- **Deliverables** – Source code, Django project, model assets (packed in `fake_review_detection-finalcode.rar`), and a design document (`Project file.docx`).  

---

## Features  

| ✅ | Feature |
|---|---------|
| ✅ | **Review ingestion** – Store reviews in a PostgreSQL/SQLite database via Django models. |
| ✅ | **Fake‑review detection** – Load the serialized model from the archive and run inference on new submissions. |
| ✅ | **Admin interface** – Manage products, reviews, and model parameters through Django admin. |
| ✅ | **User‑friendly UI** – Browse product images (`product_images/`) and view classification results. |
| ✅ | **REST‑style URLs** – Clean routing for API endpoints and web pages (`reviews/urls.py`). |
| ✅ | **Docker‑ready** – The project can be containerised (Dockerfile not included but straightforward to add). |

---

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9, Django 4.x |
| **Database** | SQLite (default) – can be swapped for PostgreSQL/MySQL |
| **Model** | Serialized scikit‑learn / TensorFlow model (included in the `.rar` archive) |
| **Frontend** | Django templates, Bootstrap (via admin) |
| **Version Control** | Git (GitHub) |
| **Deployment** | `manage.py runserver` (development) – ready for WSGI/ASGI servers (e.g., Gunicorn, Daphne) |

---

## Installation  

> **Prerequisites** – Python 3.9+, Git, and a virtual environment tool (`venv` or `conda`).

```bash
# 1. Clone the repository
git clone https://github.com/your‑username/fakereivewsproject-youtube.git
cd fakereivewsproject-youtube

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install --upgrade pip
pip install django==4.*  # adjust version as needed
# If a requirements.txt is added later, replace the above with:
# pip install -r requirements.txt

# 4. Extract the model archive (optional if you only want to run the demo)
# unzip fake_review_detection-finalcode.rar  # use your favourite extractor

# 5. Apply database migrations
python manage.py migrate

# 6. (Optional) Create a superuser for the admin panel
python manage.py createsuperuser
```

---

## Usage  

### Run the development server  

```bash
python manage.py runserver
```

- Open a browser and navigate to `http://127.0.0.1:8000/` to explore the public UI.  
- Access the admin interface at `http://127.0.0.1:8000/admin/` (login with the superuser created above).