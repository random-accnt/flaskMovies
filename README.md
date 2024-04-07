# flaskMovies
Simple project used to practice working with Flask.

Init virtual environment and install requirements.

Setup database:
```
flask --app movieApp db init
flask --app movieApp db migrate
flask --app movieApp db upgrade
```

Run the app:
```
flask --app movieApp run
```

Access the app on: [127.0.0.1:5000](127.0.0.1:5000)
