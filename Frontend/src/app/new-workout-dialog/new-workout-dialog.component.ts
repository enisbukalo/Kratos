import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';
import { CreateWorkout } from '../kratos-api-types';

/**
 * Dialog component for creating new workout templates.
 * Allows users to specify workout names and initial configuration.
 */
@Component({
  selector: 'app-new-workout-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule
  ],
  templateUrl: './new-workout-dialog.component.html',
  styleUrl: './new-workout-dialog.component.scss'
})
export class NewWorkoutDialogComponent {
  workoutName: string = '';
  currentUser: any;

  constructor(
    private dialogRef: MatDialogRef<NewWorkoutDialogComponent>,
    private apiService: KratosServiceService,
    private cookieService: CookieService
  ) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
  }

  /**
   * Submits the form and creates a new workout
   */
  onSubmit() {
    const workout: CreateWorkout = {
      name: this.workoutName,
      user_id: this.currentUser.id,
    };

    this.apiService.createWorkout(workout).subscribe(
      (response) => {
        this.dialogRef.close(response);
      }
    );
  }

  /**
   * Closes the dialog without creating a workout
   */
  onCancel() {
    this.dialogRef.close();
  }
}
