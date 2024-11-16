import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { KratosServiceService } from '../kratos-service.service';
import { WorkoutReply, Set } from '../kratos-api-types';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { NewSetDialogComponent } from '../new-set-dialog/new-set-dialog.component';
import { MatIconModule } from '@angular/material/icon';
import { UserStateService } from '../services/user-state.service';
import { MatExpansionModule } from '@angular/material/expansion';

interface GroupedSets {
  [exerciseName: string]: Set[];
}

@Component({
  selector: 'app-workout',
  standalone: true,
  imports: [
    CommonModule,
    MaterialModule,
    SidebarComponent,
    MatDialogModule,
    MatIconModule,
    MatExpansionModule
  ],
  templateUrl: './workout.component.html',
  styleUrl: './workout.component.scss'
})
export class WorkoutComponent implements OnInit {
  workout?: WorkoutReply;
  sets: Set[] = [];
  sidebarVisible: boolean = false;
  groupedSets: GroupedSets = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: KratosServiceService,
    private dialog: MatDialog,
    private userState: UserStateService
  ) { }

  goBack(): void {
    this.router.navigate(['/home']).then(() => {
      this.userState.refreshUserData();
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/home']).then(() => {
      this.userState.refreshUserData();
    });
  }

  goToLogin(): void {
    this.router.navigate(['/login']);
  }

  goToProfile(): void { }

  goToWorkouts(): void { }

  openNewSetDialog(): void {
    if (!this.workout?.id) {
      return;
    }

    const dialogRef = this.dialog.open(NewSetDialogComponent, {
      width: '500px',
      data: { workoutId: this.workout.id }
    });

    dialogRef.afterClosed().subscribe(results => {
      if (results) {
        this.sets = [...this.sets, ...results];
        this.groupedSets = this.groupSetsByExercise(this.sets);
      }
    });
  }

  private groupSetsByExercise(sets: Set[]): GroupedSets {
    return sets.reduce((groups: GroupedSets, set) => {
      const exerciseName = set.exercise?.name || 'Unknown Exercise';
      if (!groups[exerciseName]) {
        groups[exerciseName] = [];
      }
      groups[exerciseName].push(set);
      return groups;
    }, {});
  }

  ngOnInit() {
    const workoutId = Number(this.route.snapshot.paramMap.get('id'));
    if (workoutId) {
      this.apiService.getWorkout(workoutId).subscribe(workout => {
        this.workout = workout;
        this.sets = workout.sets || [];
        this.groupedSets = this.groupSetsByExercise(this.sets);
      });
    }
  }
}
