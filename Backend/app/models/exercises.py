from sqlalchemy import Column, Integer, String

from app.models import BASE


class Exercise(BASE):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


DEFAULT_EXERCISES = [
    {"name": "Bench Press", "description": "A compound upper body exercise that targets the chest, shoulders, and triceps"},
    {"name": "Squat", "description": "A compound lower body exercise that targets the quadriceps, hamstrings, and glutes"},
    {"name": "Deadlift", "description": "A compound full body exercise that targets the back, legs, and core"},
    {"name": "Overhead Press", "description": "A compound upper body exercise that targets the shoulders and triceps"},
    {"name": "Barbell Row", "description": "A compound back exercise that targets the lats and upper back"},
    {"name": "Pull Up", "description": "A bodyweight exercise that targets the back and biceps"},
    {"name": "Push Up", "description": "A bodyweight exercise that targets the chest, shoulders, and triceps"},
    {"name": "Dip", "description": "A bodyweight exercise that targets the chest, shoulders, and triceps"},
    {"name": "Lunge", "description": "A unilateral lower body exercise that targets the legs and improves balance"},
    {"name": "Plank", "description": "An isometric core exercise that improves stability"},
    {"name": "Run", "description": "A cardiovascular exercise that improves endurance and burns calories"},
    {"name": "Bike", "description": "A low-impact cardiovascular exercise that targets the legs"},
    {"name": "Swim", "description": "A full-body cardiovascular exercise that improves endurance"},
    {"name": "Walk", "description": "A low-intensity cardiovascular exercise suitable for all fitness levels"},
    {"name": "Crunches", "description": "An isolation exercise that targets the abdominal muscles"},
    {"name": "Sit Ups", "description": "A core exercise that targets the abdominal muscles and hip flexors"},
    {"name": "Mountain Climbers", "description": "A dynamic exercise that targets the core and improves cardiovascular fitness"},
]
