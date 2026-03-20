🎓 Institutional ERP System (IQAC & Academic Records)

A full-stack web application built using Django to manage institutional data including students, faculty, departments, and academic records.

🚀 Features

👨‍🎓 Student Management
- Add, view, and manage student records
- Store academic, personal, and contact details
- Dynamic department assignment
- Extended student data fields

👨‍🏫 Faculty Management
- Add and manage faculty members
- Teaching & non-teaching classification
- Department-wise organization

🏢 Department Overview
- View department-wise statistics
- Total students, boys, girls
- Faculty distribution

📊 Export System
- Export student/faculty data to Excel
- Select specific fields dynamically
- Filter by department

🔐 Authentication System
- Admin login system
- Auto-generated student login accounts
- Password management

🎨 UI Features
- Modern dashboard UI
- Responsive design (Bootstrap)
- Interactive elements (toggle, filters, select-all)


 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Libraries:**
  - OpenPyXL (Excel export)



📁 Project Structure

college_erp_final/ │ ├── core/                  # Main app (models, views, logic) ├── templates/             # HTML templates ├── static/                # CSS, JS, images (logo etc.) ├── db.sqlite3             # Local database (ignored in Git) ├── manage.py              # Django entry point └── requirements.txt       # Dependencies

---

⚙️ Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/your-username/your-repo-name.git cd your-repo-name



2️⃣ Create Virtual Environment

Windows:

python -m venv venv venv\Scripts\activate

Linux:

python3 -m venv venv source venv/bin/activate


3️⃣ Install Dependencies

pip install -r requirements.txt


4️⃣ Apply Migrations

python manage.py migrate


5️⃣ Create Admin User

python manage.py createsuperuser


6️⃣ Run Server

python manage.py runserver


🌐 Access App

http://127.0.0.1:8000/


🔑 Default Login Info

- **Admin:** Created via `createsuperuser`
- **Student Login:**
  - Username = Roll Number
  - Default Password = `1234`

---

📤 Export Feature

- Navigate to **Export Page**
- Choose:
  - Student / Faculty
  - Fields to include
  - Department filter
- Download Excel file instantly

---

⚠️ Notes

- `db.sqlite3` is ignored in Git (auto-generated via migrations)
- Always run `migrate` before starting
- Static files must be configured properly for production


🔮 Future Improvements

- Role-based access control (RBAC)
- REST API integration
- Deployment (AWS / Render)
- Advanced analytics dashboard
- File uploads (documents, certificates)



👨‍💻 Author

MSS
(Developed as part of an academic project.)



📜 License

This project is for educational purposes only.
