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
  newSet: CreateSet = {
    reps: 0,
    weight: 0,
    duration: 0,
    date: new Date().toISOString().split('T')[0],
    exercise_id: 0,
    workout_id: 0,
    user_id: 0
  };
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

  loadExercises() {
    this.apiService.getExercises({}).subscribe(exercises => {
      this.exercises = exercises;
    });
  }

  onExerciseSelect() {
    if (this.selectedExercise) {
      this.newSet.duration = 0;
      this.newSet.reps = 0;
      this.newSet.weight = 0;
    }
  }

  onSubmit() {
    if (this.selectedExercise?.id) {
      const today = new Date().toISOString().split('T')[0]; // Gets just the date part: YYYY-MM-DD

      const set: CreateSet = {
        exercise_id: this.selectedExercise.id,
        workout_id: this.data.workoutId,
        user_id: this.currentUser.id,
        reps: this.newSet.reps ?? 0,
        weight: this.newSet.weight ?? 0,
        duration: this.newSet.duration ?? 0,
        date: today
      };

      this.apiService.createSet(set).subscribe(
        (response) => {
          this.dialogRef.close(response);
        }
      );
    }
  }

  onCancel() {
    this.dialogRef.close();
  }
}
