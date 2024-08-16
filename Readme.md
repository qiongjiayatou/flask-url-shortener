# Flask URL Shortener
This is a simple URL shortener web application built with Flask, SQLAlchemy, and PostgreSQL, styled with Tailwind CSS. The application is Dockerized for easy development and deployment.


## Installation

### Clone the Repository
```sh
git clone https://github.com/qiongjiayatou/flask-url-shortener.git
cd flask-url-shortener
```

### Build and Run the Application
```sh
docker-compose up --build
```

### Initialize the Database
Run migrations:
```sh
docker-compose exec web flask db upgrade
```

### Open the browser and navigate to 
```sh
http://localhost:5000
```

### Access the Flask Shell
```sh
docker-compose exec web flask shell 
```