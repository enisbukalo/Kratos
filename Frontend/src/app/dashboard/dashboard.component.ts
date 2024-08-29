import { Component, inject } from '@angular/core';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';
import { UserReply, WorkoutReply } from '../kratos-api-types';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { SidebarModule } from 'primeng/sidebar';
import { PanelModule } from 'primeng/panel';
import { DividerModule } from 'primeng/divider';
import { Router } from '@angular/router';
import { ChartModule } from 'primeng/chart';
import { ScrollerModule } from 'primeng/scroller';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ScrollerModule, PanelModule, ChartModule, ButtonModule, AvatarModule, SidebarModule, PanelModule, DividerModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  cookieService = inject(CookieService);
  router = inject(Router);

  currentUser: UserReply;
  currentUsersWorkouts?: WorkoutReply[] = [];
  sidebarVisible: boolean = false;
  data: any;
  options: any;
  workoutOptions: any;

  constructor(private apiService: KratosServiceService) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
    this.currentUsersWorkouts = this.currentUser.workouts;
    console.log("Current User: \n" + JSON.stringify(this.currentUser));

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

  ngOnInit(): void { }

  goToDashboard(): void { }

  goToLogin(): void {
    this.router.navigate(['login']);
  }

  goToProfile(): void { }

  goToWorkouts(): void { }
}
