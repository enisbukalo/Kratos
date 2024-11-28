import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { UserQueryParams, SetQueryParams, ExerciseQueryParams, CreateSet, UpdateWorkout, UserMetrics, UserMetricsReply, GetQueryParams, BulkUpdateSets } from './kratos-api-types';
import { User, UserReply, Workout, WorkoutReply, CreateSets, Set, SetReply, Exercise } from './kratos-api-types';

import { KratosErrorHandler } from './kratos-error-handler';

@Injectable({ providedIn: 'root' })
export class KratosServiceService {
  private readonly backendEndpoint: string;
  private readonly userEndpoint = '/User';
  private readonly workoutEndpoint = '/Workout';
  private readonly setEndpoint = '/Set';
  private readonly exerciseEndpoint = '/Exercise';
  private kratosErrorHandler: KratosErrorHandler = new KratosErrorHandler();

  constructor(private http: HttpClient) {
    // Use the actual host machine's IP or hostname when accessing from browser
    const hostname = window.location.hostname;
    this.backendEndpoint = `http://${hostname}:9599`;
    console.log('Backend endpoint:', this.backendEndpoint);
  }

  private readonly httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };

  //#region User
  createUser(user: User): Observable<UserReply> {
    return this.http
      .post<UserReply>(`${this.backendEndpoint}${this.userEndpoint}`, user, this.httpOptions)
      .pipe(
        tap(_ => console.log(`User Created`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getUser(id: number): Observable<UserReply> {
    return this.http
      .get<UserReply>(`${this.backendEndpoint}${this.userEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`User Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getUsers(queryParams: UserQueryParams): Observable<UserReply[]> {
    const params = new HttpParams({ fromObject: queryParams });
    var config = {
      headers: this.httpOptions.headers,
      params: params
    }
    return this.http.get<UserReply[]>(`${this.backendEndpoint}${this.userEndpoint}`, config)
      .pipe(
        tap(_ => console.log(`Users Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  updateUser(id: number, user: User): Observable<User> {
    return this.http
      .put<UserReply>(`${this.backendEndpoint}${this.userEndpoint}/${id}`, user, this.httpOptions)
      .pipe(
        tap(_ => console.log(`User Updated`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  deleteUser(id: number): Observable<User> {
    return this.http
      .delete<User>(`${this.backendEndpoint}${this.userEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`User Deleted`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  updateUserMetrics(userId: number, metrics: UserMetrics): Observable<UserMetricsReply> {
    return this.http
      .post<UserMetricsReply>(`${this.backendEndpoint}${this.userEndpoint}/${userId}/metrics`, metrics)
      .pipe(
        tap(_ => console.log(`User Metrics Updated`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getUserMetricsHistory(userId: number): Observable<UserMetricsReply[]> {
    return this.http
      .get<UserMetricsReply[]>(`${this.backendEndpoint}${this.userEndpoint}/${userId}/metrics`)
      .pipe(
        tap(_ => console.log(`User Metrics Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }
  //#endregion

  //#region Workout
  createWorkout(workout: Workout): Observable<WorkoutReply> {
    return this.http
      .post<WorkoutReply>(`${this.backendEndpoint}${this.workoutEndpoint}`, workout, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Workout Created`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getWorkout(id: number): Observable<WorkoutReply> {
    return this.http
      .get<WorkoutReply>(`${this.backendEndpoint}${this.workoutEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Workout Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getWorkouts(queryParams: GetQueryParams): Observable<WorkoutReply[]> {
    const params = new HttpParams({ fromObject: queryParams });
    var config = {
      headers: this.httpOptions.headers,
      params: params
    }
    return this.http.get<WorkoutReply[]>(`${this.backendEndpoint}${this.workoutEndpoint}/workouts/`, config)
      .pipe(
        tap(_ => console.log(`Workouts Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getLatestWorkouts(userId: number): Observable<WorkoutReply[]> {
    return this.http.get<WorkoutReply[]>(`${this.backendEndpoint}${this.workoutEndpoint}/workouts/${userId}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Latest Workouts Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  updateWorkout(id: number, workout: UpdateWorkout): Observable<WorkoutReply> {
    return this.http
      .put<WorkoutReply>(`${this.backendEndpoint}${this.workoutEndpoint}/${id}`, workout, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Workout Updated`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  deleteWorkout(id: number): Observable<WorkoutReply> {
    return this.http
      .delete<WorkoutReply>(`${this.backendEndpoint}${this.workoutEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Workout Deleted`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }
  //#endregion

  //#region Set
  createSet(set: Set): Observable<SetReply> {
    return this.http
      .post<SetReply>(`${this.backendEndpoint}${this.setEndpoint}`, set, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Set Created`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  createSets(sets: CreateSets): Observable<SetReply[]> {
    return this.http
      .post<SetReply[]>(`${this.backendEndpoint}${this.setEndpoint}/bulk`, sets, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Sets Created`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getSet(id: number): Observable<SetReply> {
    return this.http
      .get<SetReply>(`${this.backendEndpoint}${this.setEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Set Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getSets(queryParams: SetQueryParams): Observable<SetReply[]> {
    const params = new HttpParams({ fromObject: queryParams });
    var config = {
      headers: this.httpOptions.headers,
      params: params
    }
    return this.http.get<SetReply[]>(`${this.backendEndpoint}${this.setEndpoint}`, config)
      .pipe(
        tap(_ => console.log(`Sets Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  updateSet(id: number, set: CreateSet): Observable<Set> {
    return this.http
      .put<SetReply>(`${this.backendEndpoint}${this.setEndpoint}/${id}`, set, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Set Updated`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  deleteSet(id: number): Observable<SetReply> {
    return this.http
      .delete<SetReply>(`${this.backendEndpoint}${this.setEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Set Deleted`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  updateSets(bulkUpdate: BulkUpdateSets): Observable<SetReply[]> {
    return this.http
      .put<SetReply[]>(`${this.backendEndpoint}${this.setEndpoint}/bulk`, bulkUpdate, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Sets Bulk Updated`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }
  //#endregion

  //#region Exercise
  createExercise(exercise: Exercise): Observable<Exercise> {
    return this.http
      .post<Exercise>(`${this.backendEndpoint}${this.exerciseEndpoint}`, exercise, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Exercise Created`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getExercise(id: number): Observable<Exercise> {
    return this.http
      .get<Exercise>(`${this.backendEndpoint}${this.exerciseEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Exercise Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  getExercises(queryParams: ExerciseQueryParams): Observable<Exercise[]> {
    const params = new HttpParams({ fromObject: queryParams });
    var config = {
      headers: this.httpOptions.headers,
      params: params
    }
    return this.http.get<Exercise[]>(`${this.backendEndpoint}${this.exerciseEndpoint}`, config)
      .pipe(
        tap(_ => console.log(`Exercises Retrieved`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  updateExercise(id: number, exercise: Exercise): Observable<Exercise> {
    return this.http
      .put<Exercise>(`${this.backendEndpoint}${this.exerciseEndpoint}/${id}`, exercise, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Exercise Updated`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }

  deleteExercise(id: number): Observable<Exercise> {
    return this.http
      .delete<Exercise>(`${this.backendEndpoint}${this.exerciseEndpoint}/${id}`, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Exercise Deleted`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }
  //#endregion
}
