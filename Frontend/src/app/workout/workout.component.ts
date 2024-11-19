import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { KratosServiceService } from '../kratos-service.service';
import { WorkoutReply, Set, Workout, CreateWorkout, CreateSet } from '../kratos-api-types';
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
import { ConfirmDialogComponent } from '../confirm-dialog/confirm-dialog.component';

interface GroupedSets {
  [exerciseName: string]: Set[];
}

interface EditableSet extends Set {
  isEditing: boolean;
  originalValues: {
    weight: number;
    reps: number;
    duration: number;
    distance: number;
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
    MatInputModule,
    ConfirmDialogComponent
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
  showDeleteDialog = false;
  exerciseToDelete?: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: KratosServiceService,
    private dialog: MatDialog,
    private userState: UserStateService
  ) { }

  /**
   * Navigates back to the dashboard and refreshes user data
   */
  goBack(): void {
    this.router.navigate(['/dashboard']).then(() => {
      this.userState.refreshUserData();
    });
  }

  /**
   * Navigates to the dashboard and refreshes user data
   */
  goToDashboard(): void {
    this.router.navigate(['/dashboard']).then(() => {
      this.userState.refreshUserData();
    });
  }

  /**
   * Navigates to the login page
   */
  goToLogin(): void {
    this.router.navigate(['/login']);
  }

  /**
   * Opens dialog for adding new sets to the current workout
   */
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

  /**
   * Groups sets by their exercise name
   * @param sets Array of sets to group
   * @returns Object with exercise names as keys and arrays of sets as values
   */
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

  /**
   * Initializes the component by loading workout data
   */
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

  /**
   * Shows dialog with exercise description
   * @param event Mouse event that triggered the dialog
   * @param description Exercise description to display
   */
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

  /**
   * Starts a new workout based on the current workout template
   */
  startWorkout(): void {
    if (!this.workout || this.isWorkoutMode) return;

    const newWorkout: CreateWorkout = {
      name: `${this.workout.name}`,
      user_id: this.userState.getCurrentUserId(),
    };

    this.apiService.createWorkout(newWorkout).subscribe(createdWorkout => {
      const newSets = this.sets.map(set => ({
        exercise_id: set.exercise?.id,
        workout_id: createdWorkout.id,
        user_id: this.userState.getCurrentUserId(),
        weight: set.weight,
        reps: set.reps,
        duration: set.duration,
        distance: set.distance,
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
            duration: set.duration || 0,
            distance: set.distance || 0
          }
        }));
        this.groupedSets = this.groupSetsByExercise(this.sets);
        this.isWorkoutMode = true;
      });
    });
  }

  /**
   * Saves the current workout progress by updating all sets
   */
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
          distance: set.distance || 0,
          date: set.date || new Date().toISOString().split('T')[0]
        })
      );

    if (updateSetObservables.length === 0) return;

    forkJoin(updateSetObservables).subscribe(updatedSets => {
      this.sets = updatedSets;
      this.groupedSets = this.groupSetsByExercise(this.sets);
    });
  }

  /**
   * Ends the current workout and navigates back to dashboard
   */
  endWorkout(): void {
    this.saveWorkout();
    this.router.navigate(['/dashboard']);
  }

  /**
   * Gets array of indices for the maximum number of sets across all exercises
   * @returns Array of sequential numbers from 0 to max sets
   */
  getSetIndices(): number[] {
    const maxSets = Math.max(...Object.values(this.groupedSets).map(sets => sets.length));
    return Array(maxSets).fill(0).map((_, i) => i);
  }

  /**
   * Gets list of exercise names from grouped sets
   * @returns Array of exercise names
   */
  getExerciseNames(): string[] {
    return Object.keys(this.groupedSets);
  }

  /**
   * Gets editable sets for a specific exercise
   * @param exerciseName Name of the exercise to get sets for
   * @returns Array of editable sets for the exercise
   */
  getSetsForExercise(exerciseName: string): EditableSet[] {
    return this.workoutSets.filter(set =>
      set.exercise?.name === exerciseName
    );
  }

  /**
   * Adds a new set to a specific exercise during an active workout
   * @param exerciseName Name of the exercise to add a set to
   */
  addSetToExercise(exerciseName: string): void {
    if (!this.workout?.id) return;

    const exercise = this.workoutSets.find(set => set.exercise?.name === exerciseName)?.exercise;
    if (!exercise) return;

    const newSet: CreateSet = {
      exercise_id: exercise.id!,
      workout_id: this.workout.id,
      user_id: this.userState.getCurrentUserId(),
      reps: 0,
      weight: 0,
      duration: 0,
      distance: 0,
      date: new Date().toISOString().split('T')[0]
    };

    this.apiService.createSet(newSet).subscribe(createdSet => {
      const editableSet: EditableSet = {
        ...createdSet,
        isEditing: false,
        originalValues: {
          weight: 0,
          reps: 0,
          duration: 0,
          distance: 0
        }
      };
      this.workoutSets.push(editableSet);
      this.sets = [...this.sets, createdSet];
      this.groupedSets = this.groupSetsByExercise(this.sets);
    });
  }

  /**
   * Initiates the delete exercise flow
   * @param exerciseName Name of the exercise to delete
   */
  deleteExercise(exerciseName: string): void {
    this.exerciseToDelete = exerciseName;
    this.showDeleteDialog = true;
  }

  /**
   * Confirms and executes the exercise deletion
   */
  confirmDeleteExercise(): void {
    if (!this.exerciseToDelete) return;

    const exerciseName = this.exerciseToDelete;
    let setsToDelete: any[] = [];

    if (this.isWorkoutMode) {
      setsToDelete = this.workoutSets.filter(set =>
        set.exercise?.name === exerciseName && set.id
      );
    } else {
      setsToDelete = this.sets.filter(set =>
        set.exercise?.name === exerciseName && set.id
      );
    }

    const deleteObservables = setsToDelete.map(set =>
      this.apiService.deleteSet(set.id!)
    );

    if (deleteObservables.length > 0) {
      forkJoin(deleteObservables).subscribe({
        next: () => {
          if (this.isWorkoutMode) {
            this.workoutSets = this.workoutSets.filter(set =>
              set.exercise?.name !== exerciseName
            );
          }
          this.sets = this.sets.filter(set =>
            set.exercise?.name !== exerciseName
          );
          this.groupedSets = this.groupSetsByExercise(this.sets);
          this.showDeleteDialog = false;
          this.exerciseToDelete = undefined;
        },
        error: (error) => {
          console.error('Error deleting exercise:', error);
        }
      });
    }
  }
}
