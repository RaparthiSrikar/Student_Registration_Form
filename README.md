# Student Registration Project (Django)

A fully validated student enrollment system, built to match every module in the
Form Validation KT document: HTML + CSS + Bootstrap frontend, JavaScript client-side
validation, and a Django + SQLite backend with server-side validation.

## What's included

- **Professional, custom-designed form** (not default Bootstrap look) — navy/gold
  academic theme, two-column layout, sectioned fields, live choice highlighting,
  and an image preview.
- **Client-side validation** (JavaScript) for every field: name, age, phone,
  email, gender, course, image — matches Module 5.
- **Server-side validation** (Django forms) as the authoritative source of truth —
  matches Modules 11, 12, 13.
- **Unique phone number & email** enforced at both form and database level —
  Module 13.
- **10 seeded courses**, selected via styled radio cards — Module 15.
- **Image upload validation**: file type (JPG/PNG) and 2MB size limit — Module 16.
- **Student list page** to view all registrations — Module 19.
- **SQLite database** via Django ORM — Modules 8–9.

## Project structure

```
student_registration/
├── manage.py
├── requirements.txt
├── studentproject/          # Django project (settings, urls)
├── registration/            # Django app
│   ├── models.py            # Student, Course models
│   ├── forms.py             # StudentRegistrationForm with full validation
│   ├── views.py             # register, success, student_list views
│   ├── urls.py
│   ├── admin.py
│   └── templates/registration/
│       ├── base.html
│       ├── register.html    # the enrollment form
│       ├── success.html
│       └── student_list.html
├── static/css/enrollment.css  # custom professional styling
└── db.sqlite3                # SQLite database (courses pre-seeded)
```

## Run it locally

```bash
cd student_registration
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate        # database already included, but safe to re-run
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** to see the registration form.

- `/` — registration form
- `/success/` — confirmation page after submitting
- `/students/` — list of all registered students
- `/admin/` — Django admin (run `python manage.py createsuperuser` first)

## Notes

- The database (`db.sqlite3`) already has the 10 required courses seeded, so the
  form is ready to use immediately.
- Uploaded profile images are stored in `media/student_images/`.
- To reset test data: delete `db.sqlite3`, run `python manage.py migrate` again,
  then re-seed courses (see `registration/models.py` for the `Course` model —
  add them via `/admin/` or the Django shell).
