import { Component, inject } from '@angular/core';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';
import { UserReply } from '../kratos-api-types';
import { ButtonModule } from 'primeng/button';
import { AvatarModule } from 'primeng/avatar';
import { SidebarModule } from 'primeng/sidebar';
import { PanelModule } from 'primeng/panel';
import { DividerModule } from 'primeng/divider';
import { Router } from '@angular/router';
import { ChartModule } from 'primeng/chart';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [PanelModule, ChartModule, ButtonModule, AvatarModule, SidebarModule, PanelModule, DividerModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  cookieService = inject(CookieService);
  router = inject(Router);

  currentUser: UserReply;
  sidebarVisible: boolean = false;
  data: any;
  options: any;

  constructor(private apiService: KratosServiceService) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
    console.log("Current User: \n" + JSON.stringify(this.currentUser));
    this.data = {
      labels: ['January', 'February', 'March'],
      datasets: [
        {
          label: 'Test Weight',
          data: [298, 297, 296],
        }
      ]
    };
    this.options = {
      title: {
        display: true,
        text: 'Weight Chart',
        fontSize: 16
      },
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
