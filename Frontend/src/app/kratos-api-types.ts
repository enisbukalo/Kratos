//#region QueryParams
export type GetQueryParams = {
    page_size?: number
    page_number?: number
    sort?: boolean
}

export type UserQueryParams = GetQueryParams & {}
export type ExerciseQueryParams = GetQueryParams & {}
export type SetQueryParams = GetQueryParams & {}
//#endregion

//#region exercise
export type ExerciseBase = {
    id?: number
    name?: string
    description?: string
}

export type Exercise = ExerciseBase & {}

export interface CreateExercise {
    name: string
}
//#endregion

//#region workout
export type WorkoutBase = {
    id?: number
    name?: string
    started_at?: string
}

export type Workout = WorkoutBase & {}

export type WorkoutReply = WorkoutBase & {
    sets?: Set[]
}

export interface CreateWorkout {
    name: string
    user_id: number
}

export interface UpdateWorkout {
    name: string
}
//#endregion

//#region user
export interface UserMetrics {
    weight: number;
    height: number;
}

export interface UserMetricsCreate extends UserMetrics {
    user_id: number;
}

export interface UserMetricsReply extends UserMetrics {
    id: number;
    user_id: number;
    recorded_at: string;
}

export type UserBase = {
    id?: number
    name?: string
    height?: number
    weight?: number
    metrics?: UserMetricsReply[]
}

export type UserReply = UserBase & {
    workouts?: WorkoutReply[]
}

export type User = UserBase & {}

export interface CreateUser {
    name: string
    height: number
    weight: number
}
//#endregion

//#region set
export type SetBase = {
    id?: number
    reps?: number
    weight?: number
    duration?: number
    distance?: number
    exercise?: Exercise
    date?: string
}

export type SetReply = SetBase & {
    workout?: Workout
    exercise?: Exercise
    user?: User
}

export type Set = SetBase & {}

export interface CreateSet {
    reps: number
    weight: number
    duration: number
    distance: number
    date: string
    exercise_id: number
    workout_id: number
    user_id: number
}
//#endregion

