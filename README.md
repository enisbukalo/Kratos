# Kratos
Workout app named after the Greek god of strength, Heracles.

## To Run Locally
- ### Run Dev
    ```fastapi dev app/main.py```
- ### Navigate To Swagger
    ```http://127.0.0.1/docs```

## To Run Docker Env
- ### Build Docker Image & Run Container
    ```docker compose up```
    <br> This Binds The Parent Directory To '/api' In The Container. Any Changed Made On Your Local Machine Will Be Reflected In The Container. Live Updates Are Enabled!
- ### Navigate To Swagger
    ```http://127.0.0.1:8080/docs```