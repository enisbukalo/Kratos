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

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ButtonModule, AvatarModule, SidebarModule, PanelModule, DividerModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  cookieService = inject(CookieService);
  router = inject(Router);

  currentUser: UserReply;
  sidebarVisible: boolean = true;

  constructor(private apiService: KratosServiceService) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
    console.log("Current User: \n" + JSON.stringify(this.currentUser));
  }

  ngOnInit(): void { }

  goToDashboard(): void { }

  goToLogin(): void {
    this.router.navigate(['login']);
  }

  goToProfile(): void { }

  goToWorkouts(): void { }
}