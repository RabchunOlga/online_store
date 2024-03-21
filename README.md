ONLINE STORE APP

Used:
- Python
- PostgreSQL
- Redis
- OAuth 2.0
- Stripe
- Django Rest Framework

Local Developing
    
1. Create and activate a new virtual environment:
    
        python3 -m venv ../venv
        source ../venv/bin/activate

2. Install packages:

       pip install --upgrade pip
       pip install -r requirements.txt

3. Create your own .env file. Run project dependencies, migrations, fill the database with the fixture data

       cp .env.template .env
       
       ./manage.py migrate
       ./manage.py loaddata products/fixtures/categories.json
       ./manage.py loaddata products/fixtures/products.json
       ./manage.py runserver 
4. Run Redis Server:

       redis-server