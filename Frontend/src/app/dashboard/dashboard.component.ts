import { Component, inject, Output, EventEmitter } from '@angular/core';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';
import { UserReply, WorkoutReply, Workout, Set } from '../kratos-api-types';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { SidebarModule } from 'primeng/sidebar';
import { Router } from '@angular/router';
import { ChartModule } from 'primeng/chart';
import { CommonModule } from '@angular/common';
import { CardModule } from 'primeng/card';
import { MaterialModule } from '../material.module';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MatDialog } from '@angular/material/dialog';
import { NewWorkoutDialogComponent } from '../new-workout-dialog/new-workout-dialog.component';
import { UserStateService } from '../services/user-state.service';

/**
 * Main dashboard component that displays workout summaries and statistics.
 * Provides access to create new workouts and view workout history.
 */
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    ButtonModule,
    AvatarModule,
    SidebarModule,
    ChartModule,
    CardModule,
    MaterialModule,
    SidebarComponent,
    NewWorkoutDialogComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  cookieService = inject(CookieService);
  router = inject(Router);
  dialog = inject(MatDialog);

  currentUser: UserReply;
  currentUsersWorkouts?: WorkoutReply[] = [];
  currentUsersExercises?: Set[] = [];
  sidebarVisible: boolean = false;
  data: any;
  options: any;
  workoutOptions: any;
  workouts: Workout[] = [];
  weightChart: any;

  constructor(
    private apiService: KratosServiceService,
    private userState: UserStateService,
  ) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
    this.currentUsersWorkouts = this.currentUser?.workouts || [];
    const allSets = this.currentUser?.workouts
      ? this.currentUser.workouts.flatMap(workout => workout.sets || [])
      : [];
    this.currentUsersExercises = this.getUniqueExercises(allSets);
    console.log("Current Exercises: ", this.currentUsersExercises);

    this.data = {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [
        {
          label: 'Test Weight',
          data: [298, 296, 295, 295, 294.8, 293, 291],
        }
      ]
    };

    this.options = {
      responsive: true,
      legend: {
        position: 'bottom'
      }
    }

    this.weightChart = {
      type: 'line',
      data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [
          {
            label: 'Test Weight',
            data: [298, 296, 295, 295, 294.8, 293, 291],
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: false
          }
        }
      }
    };
  }

  ngOnInit(): void {
    this.userState.currentUser$.subscribe(user => {
      if (user) {
        this.currentUser = user;
        this.apiService.getLatestWorkout().subscribe(latestWorkouts => {
          this.currentUsersWorkouts = latestWorkouts;
          const allSets = latestWorkouts
            ? latestWorkouts.flatMap(workout => workout.sets || [])
            : [];
          this.currentUsersExercises = this.getUniqueExercises(allSets);
        });
      }
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }

  goToLogin(): void {
    this.router.navigate(['login']);
  }

  goToProfile(): void { }

  goToWorkouts(): void {
    this.router.navigate(['/workouts']);
  }

  goToWorkout(workout: WorkoutReply): void {
    this.router.navigate(['workout', workout.id]);
  }

  openNewWorkoutDialog(): void {
    const dialogRef = this.dialog.open(NewWorkoutDialogComponent, {
      width: '500px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.currentUsersWorkouts = [...this.currentUsersWorkouts!, result];
      }
    });
  }

  refreshData(): void {
    const currentUserString = this.cookieService.get('currentUser');
    if (currentUserString) {
      const parsedUser = JSON.parse(currentUserString);
      if (parsedUser?.id) {
        this.apiService.getUser(parsedUser.id).subscribe(user => {
          this.currentUser = user;
          this.cookieService.set('currentUser', JSON.stringify(user));

          // Get latest workouts
          this.apiService.getLatestWorkout().subscribe(latestWorkouts => {
            this.currentUsersWorkouts = latestWorkouts;
            const allSets = latestWorkouts
              ? latestWorkouts.flatMap(workout => workout.sets || [])
              : [];
            this.currentUsersExercises = this.getUniqueExercises(allSets);
          });
        });
      }
    }
  }

  private getUniqueExercises(sets: Set[]): Set[] {
    const uniqueExercises = new Map<number, Set>();
    sets.forEach(set => {
      if (set.exercise?.id) {
        if (!uniqueExercises.has(set.exercise.id)) {
          uniqueExercises.set(set.exercise.id, set);
        }
      }
    });
    return Array.from(uniqueExercises.values());
  }
}
