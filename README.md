# auth-app

Simple authorization app
##

#### Deploy in your VPS
````bash
git clone https://github.com/sarangsahajan/auth-app.git
cd auth-app
pip3 install -r requirements.txt
python secret_key_gen.py #to generate secret_key
python manage.py migrate
python manage.py runserver
````

````bash
POST http://127.0.0.1:8000/signup HTTP/1.1
{
    "email": "<email>",
    "password": "<Password>"
}
````
````bash
POST http://127.0.0.1:8000/login HTTP/1.1
{
    "email": "<email>",
    "password": "<Password>"
}
````
````bash
GET http://127.0.0.1:8000/test_token HTTP/1.1
Authorization: Bearer <AuthToken>
````