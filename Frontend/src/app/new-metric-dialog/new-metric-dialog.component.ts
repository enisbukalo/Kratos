import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { KratosServiceService } from '../kratos-service.service';
import { UserStateService } from '../services/user-state.service';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-new-metric-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule
  ],
  templateUrl: './new-metric-dialog.component.html',
  styleUrl: './new-metric-dialog.component.scss'
})
export class NewMetricDialogComponent {
  weight: number = 0;
  currentUser: any;

  constructor(
    private dialogRef: MatDialogRef<NewMetricDialogComponent>,
    private apiService: KratosServiceService,
    private userState: UserStateService,
    private cookieService: CookieService
  ) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
  }

  onSubmit(): void {
    if (this.weight) {
      const userId = this.userState.getCurrentUserId();
      this.apiService.updateUserMetrics(userId, {
        weight: this.weight,
        height: this.currentUser.height || 0
      }).subscribe({
        next: () => {
          this.dialogRef.close(true);
        },
        error: (error) => {
          console.error('Error updating metrics:', error);
        }
      });
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
