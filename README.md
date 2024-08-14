# Kratos
Workout app named after the Greek god of strength, Kratos.

# To Run Locally
## Backend
- ### Run Dev
    ```fastapi dev Backend/app/main.py```
- ### Navigate To Backend
    ```http://127.0.0.1:8000/docs```
## Frontend
- ### Install Angular
    ```npm install -g @angular/cli```
    <br>```npm install```
    <br>```npm run build```
- ### Run Server
    ```ng serve```
- ### Navigate To Frontend
    ```http://localhost:4200/```

## To Run Docker Env
- ### Build Docker Image & Run Container
    ```docker compose up```
    <br><b><i>This Binds The `/Backend' In The Project Directory To '/Backend' In The Container. Any Changed Made On Your Local Machine Will Be Reflected In The Container. Live Updates Are Enabled!
- ### Navigate To Backend
    ```http://127.0.0.1:8080/docs```
- ### Navigate To Frontend
    ```http://127.0.0.1:3030/```
