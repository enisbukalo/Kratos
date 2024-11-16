import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { KratosServiceService } from '../kratos-service.service';
import { WorkoutReply, Set } from '../kratos-api-types';
import { SidebarComponent } from '../sidebar/sidebar.component';

@Component({
  selector: 'app-workout',
  standalone: true,
  imports: [CommonModule, MaterialModule, SidebarComponent],
  templateUrl: './workout.component.html',
  styleUrl: './workout.component.scss'
})
export class WorkoutComponent implements OnInit {
  workout?: WorkoutReply;
  sets: Set[] = [];
  sidebarVisible: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: KratosServiceService
  ) { }

  goBack(): void {
    this.router.navigate(['/home']);
  }

  goToDashboard(): void {
    this.router.navigate(['/home']);
  }

  goToLogin(): void {
    this.router.navigate(['/login']);
  }

  goToProfile(): void { }

  goToWorkouts(): void { }

  ngOnInit() {
    const workoutId = Number(this.route.snapshot.paramMap.get('id'));
    if (workoutId) {
      this.apiService.getWorkout(workoutId).subscribe(workout => {
        this.workout = workout;
        this.sets = workout.sets || [];
      });
    }
  }
}
