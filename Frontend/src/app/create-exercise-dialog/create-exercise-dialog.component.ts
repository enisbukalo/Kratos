import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { KratosServiceService } from '../kratos-service.service';
import { Exercise } from '../kratos-api-types';
import { UserStateService } from '../services/user-state.service';

@Component({
  selector: 'app-create-exercise-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule
  ],
  templateUrl: './create-exercise-dialog.component.html',
  styleUrl: './create-exercise-dialog.component.scss'
})
export class CreateExerciseDialogComponent {
  exercise: { name: string; description: string; user_id?: number } = {
    name: '',
    description: ''
  };

  constructor(
    private dialogRef: MatDialogRef<CreateExerciseDialogComponent>,
    private apiService: KratosServiceService,
    private userState: UserStateService
  ) { }

  onSubmit() {
    this.exercise.user_id = this.userState.getCurrentUserId();

    this.apiService.createExercise(this.exercise).subscribe({
      next: (newExercise: Exercise) => {
        this.dialogRef.close(newExercise);
      },
      error: (error: any) => {
        console.error('Error creating exercise:', error);
      }
    });
  }

  onCancel() {
    this.dialogRef.close();
  }
}
