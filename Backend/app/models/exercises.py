from sqlalchemy import Column, Integer, String

from app.models import BASE


class Exercise(BASE):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


DEFAULT_EXERCISES = [
    {
        "name": "Barbell Bench Press",
        "description": "A chest-focused compound exercise performed by lowering a barbell to your chest and pressing it back up while lying on a flat bench.",
    },
    {
        "name": "Dumbbell Bench Press",
        "description": "A variation of the bench press using dumbbells to improve range of motion and stability, targeting the chest, shoulders, and triceps.",
    },
    {
        "name": "Back Squat",
        "description": "A full-body strength exercise where a barbell is placed across the back of the shoulders, engaging the legs, glutes, and core.",
    },
    {
        "name": "Front Squat",
        "description": "A quad-dominant squat variation where the barbell rests on the front of the shoulders, requiring an upright posture and core stability.",
    },
    {
        "name": "Straight Legged Deadlift",
        "description": "An exercise targeting the hamstrings and lower back by lowering a barbell with a slight knee bend while maintaining a straight back.",
    },
    {
        "name": "Deadlift",
        "description": "A compound movement that works the entire posterior chain by lifting a barbell from the floor to a standing position.",
    },
    {
        "name": "Overhead Press",
        "description": "A shoulder-dominant exercise performed by pressing a barbell or dumbbells overhead from shoulder height.",
    },
    {
        "name": "Barbell Row",
        "description": "A back-building exercise where you pull a barbell towards your lower torso while maintaining a bent-over position.",
    },
    {
        "name": "Dumbbell Row",
        "description": "A unilateral back exercise performed by pulling a dumbbell towards your torso while supporting your body with the opposite hand on a bench.",
    },
    {"name": "Pull Up", "description": "A bodyweight exercise targeting the upper back and biceps by pulling your chin above a horizontal bar."},
    {
        "name": "Push Up",
        "description": "A bodyweight exercise targeting the chest, shoulders, and triceps, performed by lowering and raising your body in a prone position.",
    },
    {"name": "Barbell Curl", "description": "A bicep isolation exercise where you curl a barbell upwards, keeping your elbows stationary."},
    {"name": "Dumbbell Curl", "description": "A bicep exercise using dumbbells to curl each arm individually, promoting balanced development."},
    {
        "name": "Hip Thrusts",
        "description": "A glute-focused exercise performed by thrusting the hips upward while the upper back is supported on a bench.",
    },
    {
        "name": "Dip",
        "description": "A compound bodyweight exercise targeting the triceps and chest, performed by lowering and raising your body on parallel bars.",
    },
    {"name": "Lunge", "description": "A lower-body exercise where you step forward and lower your hips to work the legs and glutes."},
    {"name": "Plank", "description": "A core exercise performed by holding a push-up position with a straight body for an extended period."},
    {
        "name": "Standing Dumbbell Flies",
        "description": "A chest exercise performed by bringing dumbbells together in a wide arc while standing, focusing on the pectoral muscles.",
    },
    {"name": "Dumbbell Front Flies", "description": "An anterior shoulder isolation exercise performed by raising dumbbells in front of the body."},
    {"name": "Dumbbell Back Flies", "description": "An exercise targeting the rear deltoids by extending the arms outward while bent at the waist."},
    {"name": "Run", "description": "A cardiovascular exercise involving sustained jogging or sprinting to improve endurance and overall fitness."},
    {
        "name": "Bike",
        "description": "A low-impact cardio workout performed on a stationary or moving bicycle to build leg strength and improve stamina.",
    },
    {"name": "Swim", "description": "A full-body cardio workout performed in water, engaging muscles while reducing joint strain."},
    {"name": "Walk", "description": "A low-intensity exercise for cardiovascular health and active recovery, involving steady-paced movement."},
    {"name": "Crunches", "description": "An abdominal exercise where you curl your shoulders off the ground to engage the core."},
    {"name": "Sit Ups", "description": "A core workout involving lifting your upper body fully off the ground to strengthen abdominal muscles."},
    {
        "name": "Mountain Climbers",
        "description": "A dynamic bodyweight exercise combining cardio and core work, performed by alternating knees towards the chest in a push-up position.",
    },
    {
        "name": "Pullover",
        "description": "A versatile upper-body exercise performed by lying on a bench and moving a dumbbell or barbell in an arc from above your chest to behind your head, targeting the chest, lats, and core.",
    },
    {
        "name": "Skullcrushers",
        "description": "A tricep-focused exercise performed by lying on a bench and lowering a barbell or dumbbells towards your forehead before extending your arms back to the starting position.",
    },
    {
        "name": "Bent-Over Tricep Extensions",
        "description": "An isolation exercise targeting the triceps, performed by leaning forward with one knee and hand on a bench, and extending a dumbbell backwards from a bent elbow position until the arm is fully straightened.",
    },
]
