import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { KratosServiceService } from '../kratos-service.service';
import { WorkoutReply, Set, Workout, CreateWorkout } from '../kratos-api-types';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { NewSetDialogComponent } from '../new-set-dialog/new-set-dialog.component';
import { MatIconModule } from '@angular/material/icon';
import { UserStateService } from '../services/user-state.service';
import { MatExpansionModule } from '@angular/material/expansion';
import { DescriptionDialogComponent } from '../description-dialog/description-dialog.component';
import { FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { forkJoin } from 'rxjs';

interface GroupedSets {
  [exerciseName: string]: Set[];
}

interface EditableSet extends Set {
  isEditing: boolean;
  originalValues: {
    weight: number;
    reps: number;
    duration: number;
  };
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
    MatExpansionModule,
    FormsModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule
  ],
  templateUrl: './workout.component.html',
  styleUrl: './workout.component.scss'
})
export class WorkoutComponent implements OnInit {
  workout?: WorkoutReply;
  sets: Set[] = [];
  sidebarVisible: boolean = false;
  groupedSets: GroupedSets = {};
  isWorkoutMode: boolean = false;
  workoutSets: EditableSet[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: KratosServiceService,
    private dialog: MatDialog,
    private userState: UserStateService
  ) { }

  goBack(): void {
    this.router.navigate(['/dashboard']).then(() => {
      this.userState.refreshUserData();
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']).then(() => {
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

  showDescriptionDialog(event: MouseEvent, description: string | undefined): void {
    event.stopPropagation();
    if (!description) {
      description = 'No description available';
    }
    this.dialog.open(DescriptionDialogComponent, {
      data: { description },
      width: '400px',
      panelClass: 'modern-dialog'
    });
  }

  startWorkout(): void {
    if (!this.workout) return;

    const newWorkout: CreateWorkout = {
      name: `${this.workout.name}`,
      user_id: this.userState.getCurrentUserId(),
    };

    this.apiService.createWorkout(newWorkout).subscribe(createdWorkout => {
      // Create new sets for the new workout
      const newSets = this.sets.map(set => ({
        exercise_id: set.exercise?.id,
        workout_id: createdWorkout.id,
        user_id: this.userState.getCurrentUserId(),
        weight: set.weight,
        reps: set.reps,
        duration: set.duration,
        date: new Date().toISOString().split('T')[0]
      }));

      const createSetObservables = newSets.map(set =>
        this.apiService.createSet(set)
      );

      forkJoin(createSetObservables).subscribe(createdSets => {
        this.workout = createdWorkout;
        this.sets = createdSets;
        this.workoutSets = createdSets.map(set => ({
          ...set,
          isEditing: false,
          originalValues: {
            weight: set.weight || 0,
            reps: set.reps || 0,
            duration: set.duration || 0
          }
        }));
        this.groupedSets = this.groupSetsByExercise(this.sets);
        this.isWorkoutMode = true;
      });
    });
  }

  saveWorkout(): void {
    if (!this.workout?.id) return;

    const updateSetObservables = this.workoutSets
      .filter(set => set.id !== undefined)
      .map(set =>
        this.apiService.updateSet(set.id!, {
          exercise_id: set.exercise?.id || 0,
          workout_id: this.workout?.id || 0,
          user_id: this.userState.getCurrentUserId(),
          weight: set.weight || 0,
          reps: set.reps || 0,
          duration: set.duration || 0,
          date: set.date || new Date().toISOString().split('T')[0]
        })
      );

    if (updateSetObservables.length === 0) return;

    forkJoin(updateSetObservables).subscribe(updatedSets => {
      this.sets = updatedSets;
      this.groupedSets = this.groupSetsByExercise(this.sets);
    });
  }

  endWorkout(): void {
    this.saveWorkout();
    this.router.navigate(['/dashboard']);
  }

  getSetIndices(): number[] {
    const maxSets = Math.max(...Object.values(this.groupedSets).map(sets => sets.length));
    return Array(maxSets).fill(0).map((_, i) => i);
  }

  getExerciseNames(): string[] {
    return Object.keys(this.groupedSets);
  }

  getSetsForExercise(exerciseName: string): EditableSet[] {
    return this.workoutSets.filter(set =>
      set.exercise?.name === exerciseName
    );
  }
}
