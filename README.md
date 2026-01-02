# 🎓 Instructor Evaluation System (HILCoE)

A Django-based web platform built for academic institutions to manage instructor evaluations efficiently.  
Students can evaluate instructors securely, and the Academic Head can analyze feedback through reports.

---

## 🧭 Overview

This system allows students to log in using institutional credentials and complete instructor evaluation forms.  
The Academic Head can access summarized results and export performance reports in PDF and Excel formats.

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Django |
| **Frontend** | HTML, CSS, Bootstrap |
| **Database** | MySQL (production) / SQLite (local dev) |
| **Authentication** | Django Auth |
| **Reporting** | PDF and Excel report generation |
| **Version Control** | Git & GitHub |

---

## ⚙️ Key Features

- 👩‍🎓 Student login with role-based authentication  
- 🧑‍🏫 Instructor evaluation forms with dynamic questions  
- 📊 Academic Head dashboard with performance summaries  
- 🗂 Department and course-level filtering  
- 🧾 PDF export of evaluation results (Academic Head only)  
- 🧾 Excel report generation of evaluation results (Academic Head only)

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/David-T7/Instructor-Evaluation-For-HILCoE-Django.git
cd Instructor-Evaluation-For-HILCoE-Django

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (Admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver

## 📸 Project Preview
<img width="959" height="512" alt="Home page" src="https://github.com/user-attachments/assets/48cf701f-02d8-4b26-9cd2-4d4f93ef874c" />
