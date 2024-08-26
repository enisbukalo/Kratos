import { Component, inject } from '@angular/core';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  currentUserId: number;

  cookieService = inject(CookieService);

  constructor(private apiService: KratosServiceService) {
    this.currentUserId = Number(this.cookieService.get('currentUserId'));
  }

  ngOnInit(): void {
    console.log()
    this.apiService.getUser(2).subscribe((users) => {
      this.cookieService.set('currentUserId', String(users.id));
      console.log("Current User Id: " + this.currentUserId);
      console.log(users);
    });
  }
}
