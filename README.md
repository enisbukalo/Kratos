# Kratos Backend API

A FastAPI-based backend service for tracking workouts, exercises, and user fitness metrics.

## Features

- **Workout Management**
  - Create and track workouts
  - Record exercise sets within workouts
  - Get latest workouts by user
  - Filter workouts by name and date
  - Bulk update exercise sets

- **Exercise Library**
  - Maintain a database of exercises
  - Track exercise details and descriptions
  - Associate exercises with workout sets

- **User Management**
  - User profiles with height/weight tracking
  - Historical fitness metrics
  - Workout history per user
  - Track user metrics over time

## API Endpoints

### Workouts
- `GET /Workout/workouts/` - Get paginated list of workouts
- `GET /Workout/workouts/{user_id}` - Get latest workouts for user
- `GET /Workout/{id}` - Get workout by ID
- `POST /Workout` - Create new workout
- `PUT /Workout/{id}` - Update workout
- `DELETE /Workout/{id}` - Delete workout

### Exercises
- `GET /Exercise` - Get paginated list of exercises
- `GET /Exercise/{id}` - Get exercise by ID
- `POST /Exercise` - Create new exercise
- `PUT /Exercise/{id}` - Update exercise
- `DELETE /Exercise/{id}` - Delete exercise

### Sets
- `POST /Set` - Create new exercise set
- `POST /Set/bulk` - Create multiple exercise sets
- `PUT /Set/{id}` - Update exercise set
- `PUT /Set/bulk` - Bulk update exercise sets
- `DELETE /Set/{id}` - Delete exercise set

### Users
- `GET /User` - Get paginated list of users
- `GET /User/{id}` - Get user by ID
- `POST /User` - Create new user with initial metrics
- `PUT /User/{id}` - Update user details
- `POST /User/{id}/metrics` - Record new user metrics
- `GET /User/{id}/metrics` - Get user metrics history

## Development

### Setup

#### Local
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run Backend: `python app/main.py --port 9599` (From The Backend Directory)
6. Run Frontend: `ng serve --port 9598` (From The Frontend Directory)
7. Navigate to `http://localhost:9598` For The Web App.
8. Navigate to `http://localhost:9599/docs` For The API Documentation.

#### Docker
1. Clone the repository
2. Run `docker compose up --build`
3. Navigate to `http://localhost:9598` For The Web App.
4. Navigate to `http://localhost:9599/docs` For The API Documentation.

## Testing
1. Navigate to the Backend Directory
2. Run `pytest`

