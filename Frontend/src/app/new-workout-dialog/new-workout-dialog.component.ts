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

  onSubmit() {
    const workout = {
      name: this.workoutName,
      user_id: this.currentUser.id,
      started_at: new Date().toISOString()
    };

    this.apiService.createWorkout(workout).subscribe(
      (response) => {
        this.dialogRef.close(response);
      }
    );
  }

  onCancel() {
    this.dialogRef.close();
  }
}
