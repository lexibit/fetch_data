# fetch_data

1. create virtual env
    source venv/bin/activate
2. pip install -r requirements.txt

3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver

OPEN POSTMAN

7. http://localhost:8000/login/
    Body -> JSON 
        example: {"username":"korisnik", "password":"123456789"}
    got the <TOKEN>

8. http://localhost:8000/fetch-data/
    example: POST {"chain" : "bsc",
            "address" : "0x2FA5dAF6Fe0708fBD63b1A7D1592577284f52256"}

9. Authorization -> Bearer <token> 
    GET http://localhost:8000/api/transactions/
