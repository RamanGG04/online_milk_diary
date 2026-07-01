# Online Milk Diary

Django web application for dairy cooperative milk collection, billing, and reporting — built as a college project.

## Features

- User roles: Admin, Operator, Accountant, Farmer
- Farmer registration and collection center management
- Daily milk entry (morning/evening shift, fat %, auto rate calculation)
- Rate chart management
- Monthly billing with deductions and payments
- Dashboard with charts
- Daily reports with PDF and Excel export

## Demo Login (after setup_demo_data)

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Operator | operator | operator123 |
| Accountant | accountant | accountant123 |
| Farmer | farmer1 | farmer123 |

## Local Setup

```bash
cd online_milk_diary
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py setup_demo_data
python manage.py runserver
```

Open http://127.0.0.1:8000 to view the new landing page with separate admin and user login options.

## Deploy Free on Render (Recommended)

**Render** is the best free option for Django college projects:
- Free web service + free PostgreSQL database
- Easy GitHub deploy
- Public URL like `https://online-milk-diary.onrender.com`
- Ready-to-use config included: `render.yaml` and `build.sh`
- Note: Free tier sleeps after 15 min inactivity (first load may take ~30 sec)

### Steps

1. Push this project to **GitHub**
2. Go to [render.com](https://render.com) and sign up (free)
3. Click **New → Blueprint** and connect your GitHub repo
4. Render reads `render.yaml` and creates web service + database automatically
5. Wait for deploy to finish (~5-10 min)
6. Open your live URL and login with demo credentials above

### Manual Render Deploy (alternative)

1. **New → PostgreSQL** (free plan) — copy Internal Database URL
2. **New → Web Service** → connect repo
3. Settings:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
4. Environment variables:
   - `DATABASE_URL` = your PostgreSQL URL
   - `SECRET_KEY` = random secret string
   - `DEBUG` = False
   - `ALLOWED_HOSTS` = your-app.onrender.com
   - `CREATE_SUPERUSER` = true (loads demo data on first deploy)

## Other Free Deployment Options

| Platform | Pros | Cons |
|----------|------|------|
| **Render** (Best) | Free PostgreSQL, easy Django setup | Sleeps when idle |
| **PythonAnywhere** | Django-friendly, always on (limited) | Manual setup, restricted outbound |
| **Railway** | Fast deploy | Limited free credits (~$5/month) |
| **Fly.io** | Good performance | Requires credit card, more complex |

**Recommendation:** Use **Render** for your college project submission — free, reliable, and gives a real public URL.

## Project Structure

```
online_milk_diary/
├── accounts/       # Login, roles, users
├── farmers/        # Farmer & center management
├── collection/     # Milk entries & rates
├── billing/        # Payments & deductions
├── reports/        # Dashboard & exports
├── templates/      # HTML templates
├── static/         # CSS
├── config/         # Django settings
├── build.sh        # Render build script
├── render.yaml     # Render blueprint
└── requirements.txt
```

## For College Report

Include: Introduction, Objectives, System Analysis, Modules, Database Design, Screenshots, Testing, Conclusion.

## License

Educational use — college project.
