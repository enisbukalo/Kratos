import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Exercise, CreateSet, CreateSets } from '../kratos-api-types';
import { KratosServiceService } from '../kratos-service.service';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { UserStateService } from '../services/user-state.service';
import { CreateExerciseDialogComponent } from '../create-exercise-dialog/create-exercise-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

/**
 * Dialog component for adding new sets to a workout.
 * Allows users to select exercises and create multiple sets with specified parameters.
 */
@Component({
  selector: 'app-new-set-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatIconModule
  ],
  templateUrl: './new-set-dialog.component.html',
  styleUrl: './new-set-dialog.component.scss'
})
export class NewSetDialogComponent {
  exercises: Exercise[] = [];
  selectedExercise?: Exercise;
  sets: CreateSet[] = [this.createEmptySet()];

  constructor(
    private dialogRef: MatDialogRef<NewSetDialogComponent>,
    private dialog: MatDialog,
    private apiService: KratosServiceService,
    private userState: UserStateService,
    @Inject(MAT_DIALOG_DATA) public data: { workoutId: number },
    private snackBar: MatSnackBar
  ) {
    this.loadExercises();
  }

  /**
   * Creates an empty set with default values
   * @returns New CreateSet object with initialized values
   */
  private createEmptySet(): CreateSet {
    return {
      reps: 0,
      weight: 0,
      duration: 0,
      distance: 0,
      date: new Date().toISOString().split('T')[0],
      exercise_id: 0,
      workout_id: 0,
      user_id: 0
    };
  }

  /**
   * Adds a new set based on the previous set's values or creates an empty set
   */
  addSet() {
    if (this.sets.length > 0) {
      const previousSet = this.sets[this.sets.length - 1];
      const newSet: CreateSet = {
        reps: previousSet.reps,
        weight: previousSet.weight + 5,
        duration: previousSet.duration,
        distance: previousSet.distance,
        date: new Date().toISOString().split('T')[0],
        exercise_id: previousSet.exercise_id,
        workout_id: previousSet.workout_id,
        user_id: previousSet.user_id
      };
      this.sets.push(newSet);
    } else {
      this.sets.push(this.createEmptySet());
    }
  }

  /**
   * Removes a set at the specified index
   * @param index Index of the set to remove
   */
  removeSet(index: number) {
    this.sets.splice(index, 1);
  }

  /**
   * Submits the form and creates new sets in the database
   */
  onSubmit() {
    if (this.selectedExercise?.id) {
      const today = new Date().toISOString().split('T')[0];
      const userId = this.userState.getCurrentUserId();

      const createSetsPayload: CreateSets = {
        exercise_id: this.selectedExercise.id,
        workout_id: this.data.workoutId,
        user_id: userId,
        sets: this.sets.map(set => ({
          reps: set.reps ?? 0,
          weight: set.weight ?? 0,
          duration: set.duration ?? 0,
          distance: set.distance ?? 0,
          date: today
        }))
      };

      this.apiService.createSets(createSetsPayload).subscribe({
        next: (response) => {
          this.snackBar.open('Sets created successfully!', 'Close', {
            duration: 3000,
            panelClass: ['success-snackbar']
          });
          this.dialogRef.close(response);
        },
        error: (error) => {
          console.error('Error creating sets:', error);
          this.snackBar.open('Failed to create sets', 'Close', {
            duration: 3000,
            panelClass: ['error-snackbar']
          });
        }
      });
    }
  }

  /**
   * Loads available exercises from the API
   */
  loadExercises() {
    this.apiService.getExercises({}).subscribe(exercises => {
      this.exercises = exercises;
    });
  }

  onCancel() {
    this.dialogRef.close();
  }

  openCreateExerciseDialog() {
    const dialogRef = this.dialog.open(CreateExerciseDialogComponent, {
      width: '400px',
      panelClass: 'modern-dialog'
    });

    dialogRef.afterClosed().subscribe((result: Exercise | undefined) => {
      if (result) {
        this.loadExercises();
        this.selectedExercise = result;
      }
    });
  }
}
