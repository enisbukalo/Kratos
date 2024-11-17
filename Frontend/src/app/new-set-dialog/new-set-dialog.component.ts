import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Exercise, CreateSet } from '../kratos-api-types';
import { KratosServiceService } from '../kratos-service.service';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { CookieService } from 'ngx-cookie-service';
import { forkJoin } from 'rxjs';

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
  currentUser: any;

  constructor(
    private dialogRef: MatDialogRef<NewSetDialogComponent>,
    private apiService: KratosServiceService,
    private cookieService: CookieService,
    @Inject(MAT_DIALOG_DATA) public data: { workoutId: number }
  ) {
    this.loadExercises();
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
  }

  private createEmptySet(): CreateSet {
    return {
      reps: 0,
      weight: 0,
      duration: 0,
      date: new Date().toISOString().split('T')[0],
      exercise_id: 0,
      workout_id: 0,
      user_id: 0
    };
  }

  addSet() {
    if (this.sets.length > 0) {
      const previousSet = this.sets[this.sets.length - 1];
      const newSet: CreateSet = {
        reps: previousSet.reps,
        weight: previousSet.weight,
        duration: previousSet.duration,
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

  removeSet(index: number) {
    this.sets.splice(index, 1);
  }

  onSubmit() {
    if (this.selectedExercise?.id) {
      const today = new Date().toISOString().split('T')[0];

      const setsToCreate = this.sets.map(set => ({
        exercise_id: this.selectedExercise!.id,
        workout_id: this.data.workoutId,
        user_id: this.currentUser.id,
        reps: set.reps ?? 0,
        weight: set.weight ?? 0,
        duration: set.duration ?? 0,
        date: today
      }));

      const createSetObservables = setsToCreate.map(set =>
        this.apiService.createSet(set)
      );

      forkJoin(createSetObservables).subscribe({
        next: (responses) => {
          this.dialogRef.close(responses);
        },
        error: (error) => {
          console.error('Error creating sets:', error);
        }
      });
    }
  }

  onCancel() {
    this.dialogRef.close();
  }

  loadExercises() {
    this.apiService.getExercises({}).subscribe(exercises => {
      this.exercises = exercises;
    });
  }
}
