uwsgi --socket 127.0.0.1:8080 --wsgi-file app.py --callable app --master --processes 8 --threads 4

