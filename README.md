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


## Notes
- A User can create a workout.
- A Workout consists of a collection of Sets of Exercises.
- A Session is a collection of Sets grouped by Exercise.

## API Endpoints

### Workouts
- `GET /Workout` - Get all workouts (with pagination)
  - Query params:
    - page_size (default: 10)
    - page_number (default: 1)
    - latest (boolean, default: false)
- `GET /Workout/{id}` - Get specific workout
- `POST /Workout` - Create new workout
  - Required fields: name, user_id
- `PUT /Workout/{id}` - Update workout
  - Optional fields: name
- `DELETE /Workout/{id}` - Delete workout

### Sets
- `GET /Set` - Get all sets (with pagination)
- `GET /Set/{id}` - Get specific set
- `POST /Set` - Create new set
  - Required fields: reps, weight, duration, distance, date, exercise_id, workout_id, user_id
- `PUT /Set/{id}` - Update set
  - All fields required
- `DELETE /Set/{id}` - Delete set

### Exercises
- `GET /Exercise` - Get all exercises (with pagination)
- `GET /Exercise/{id}` - Get specific exercise
- `POST /Exercise` - Create new exercise
  - Required fields: name, description
- `PUT /Exercise/{id}` - Update exercise
  - All fields required
- `DELETE /Exercise/{id}` - Delete exercise

### Users
- `GET /User` - Get all users (with pagination)
- `GET /User/{id}` - Get specific user
- `POST /User` - Create new user
  - Required fields: name, email
- `PUT /User/{id}` - Update user
  - All fields required
- `DELETE /User/{id}` - Delete user