# Kratos Backend API

A FastAPI-based backend service for tracking workouts, exercises, and user fitness metrics.

## Features

- **Workout Management**
  - Create and track workouts
  - Record exercise sets within workouts
  - Get latest workouts by user
  - Filter workouts by name and date

- **Exercise Library**
  - Maintain a database of exercises
  - Track exercise details and descriptions
  - Associate exercises with workout sets

- **User Management**
  - User profiles with height/weight tracking
  - Historical fitness metrics
  - Workout history per user

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

### Users
- `GET /User` - Get paginated list of users
- `GET /User/{id}` - Get user by ID
- `POST /User` - Create new user with initial metrics
- `PUT /User/{id}` - Update user details

## Development

### Prerequisites
- Python 3.10+
- SQLite3
- FastAPI
- SQLAlchemy

### Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run development server: `uvicorn app.main:app --reload`

### Testing
Run tests with pytest: