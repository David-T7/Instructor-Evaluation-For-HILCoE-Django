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


```
## 📸 Project Preview
All screenshots are stored in the `screenshots` folder at the root of this repository.

![Home page](<screenshots//Home%20page.png>)
![Login page](<screenshots/login%20page.png>)
![Home page](<screenshots//student%20home%20page.png>)
![Login page](<screenshots/evaluation%20page%20for%20students.png>)
![Login page](<screenshots/student%20evaluation%20sample.png>)
![Login page](<screenshots/student%20evaluation%20sample2.png>)
![Login page](<screenshots/student%20evaluation%20sample4.png>)
![Login page](<screenshots/Academic%20Search%20Evaluation.png>)
![Login page](<screenshots/student%20evaluation%20result%20page.png>)
![Login page](<screenshots/detailed%20student%20evaluation%20result.png>)
![Login page](<screenshots/detailed%20student%20evaluation%20result%203.png>)
![Login page](<screenshots/detailed%20student%20evaluation%20result%20pdf%20download.png>)
![Login page](<screenshots/Generate%20report%20page.png>)
![Login page](<screenshots/excel%20report.png>)
