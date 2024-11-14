import { Component, inject } from '@angular/core';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';
import { UserReply, Workout, WorkoutReply, Set } from '../kratos-api-types';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { SidebarModule } from 'primeng/sidebar';
import { PanelModule } from 'primeng/panel';
import { DividerModule } from 'primeng/divider';
import { Router } from '@angular/router';
import { ChartModule } from 'primeng/chart';
import { ScrollerModule } from 'primeng/scroller';
import { CommonModule } from '@angular/common';
import { CardModule } from 'primeng/card';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    ScrollerModule,
    PanelModule,
    ChartModule,
    ButtonModule,
    AvatarModule,
    SidebarModule,
    PanelModule,
    DividerModule,
    CardModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  cookieService = inject(CookieService);
  router = inject(Router);

  currentUser: UserReply;
  currentUsersWorkouts?: WorkoutReply[] = [];
  currentUsersExercises?: Set[] = [];
  sidebarVisible: boolean = false;
  data: any;
  options: any;
  workoutOptions: any;
  workouts: Workout[] = [];

  constructor(private apiService: KratosServiceService) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
    this.currentUsersWorkouts = this.currentUser?.workouts || [];
    this.currentUsersExercises = this.currentUser?.workouts
      ? this.currentUser.workouts.flatMap(workout => workout.sets || [])
      : [];
    console.log("Current Exercises: ", this.currentUsersExercises);

    this.data = {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [
        {
          label: 'Test Weight',
          data: [298, 296, 295, 295, 294.8, 293, 291],
        }
      ]
    };

    this.options = {
      responsive: true,
      legend: {
        position: 'bottom'
      }
    }
  }

  ngOnInit(): void {

  }

  goToDashboard(): void { }

  goToLogin(): void {
    this.router.navigate(['login']);
  }

  goToProfile(): void { }

  goToWorkouts(): void { }
}
