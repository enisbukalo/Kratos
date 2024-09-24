//#region QueryParams
export type GetQueryParams = {
    page_size?: number
    page_number?: number
    sort?: boolean
}

export type UserQueryParams = GetQueryParams & {}
export type WorkoutQueryParams = GetQueryParams & {}
export type ExerciseQueryParams = GetQueryParams & {}
export type SetQueryParams = GetQueryParams & {}
//#endregion

//#region exercise
export type ExerciseBase = {
    id?: number
    name?: string
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
}

export type Workout = WorkoutBase & {}

export type WorkoutReply = WorkoutBase & {
    sets?: Set[]
}

export interface CreateWorkout {
    name: string
    user_id: number
}
//#endregion

//#region user
export type UserBase = {
    id?: number
    name?: string
    height?: number
    weight?: number
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
    exercise?: Exercise
    date?: Date
}

export type SetReply = SetBase & {
    workout?: Workout
    exercise?: Exercise
    user?: User
}

export type Set = SetBase & {}

export interface CreateSet {
    reps: number
    date: Date
    exercise_id: number
    workout_id: number
    user_id: number
}
//#endregion
