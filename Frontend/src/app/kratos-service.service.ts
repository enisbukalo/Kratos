import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable, throwError } from 'rxjs';
import { catchError, tap, mergeMap, map, concatMap } from 'rxjs/operators';

import { UserQueryParams, WorkoutQueryParams, SetQueryParams, ExerciseQueryParams } from './kratos-api-types';
import { User, UserReply, Workout, WorkoutReply, Set, SetReply, Exercise } from './kratos-api-types';

import { KratosErrorHandler } from './kratos-error-handler';

@Injectable({
  providedIn: 'root'
})
export class KratosServiceService {
  private readonly backendEndpoint = 'http://localhost:8080';
  private readonly userEndpoint = '/User';
  private readonly workoutEndpoint = '/Workout';
  private readonly setEndpoint = '/Set';
  private readonly exerciseEndpoint = '/Exercise';
  private kratosErrorHandler: KratosErrorHandler = new KratosErrorHandler();

  constructor(private http: HttpClient) { }

  private readonly httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  //#region User
  createUser(user: User): Observable<UserReply> {
    return this.http
      .post<UserReply>(`${this.backendEndpoint}${this.userEndpoint}`, user, this.httpOptions)
      .pipe(
        tap(_ => console.log(`Created User`)),
        catchError((error: HttpErrorResponse) => this.kratosErrorHandler.handleError(error)),
      );
  }
  //#endregion

  //#region Workout
  //#endregion

  //#region Set
  //#endregion

  //#region Exercise
  //#endregion
}
