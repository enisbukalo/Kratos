import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { KratosServiceService } from '../kratos-service.service';
import { UserStateService } from '../services/user-state.service';
import { UserMetricsReply } from '../kratos-api-types';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-user-metrics',
  templateUrl: './user-metrics.component.html',
  styleUrls: ['./user-metrics.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ]
})
export class UserMetricsComponent implements OnInit {
  metricsForm: FormGroup;
  metricsHistory: UserMetricsReply[] = [];
  displayedColumns = ['date', 'weight', 'height'];

  constructor(
    private fb: FormBuilder,
    private apiService: KratosServiceService,
    private userState: UserStateService
  ) {
    this.metricsForm = this.fb.group({
      weight: ['', Validators.required],
      height: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.loadMetricsHistory();
  }

  loadMetricsHistory() {
    const userId = this.userState.getCurrentUserId();
    this.apiService.getUserMetricsHistory(userId).subscribe(metrics => {
      this.metricsHistory = metrics;
    });
  }

  onSubmit() {
    if (this.metricsForm.valid) {
      const userId = this.userState.getCurrentUserId();
      this.apiService.updateUserMetrics(userId, this.metricsForm.value).subscribe(() => {
        this.loadMetricsHistory();
        this.metricsForm.reset();
      });
    }
  }
}
