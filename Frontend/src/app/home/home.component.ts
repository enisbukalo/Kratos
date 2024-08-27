import { Component, inject } from '@angular/core';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';
import { UserReply } from '../kratos-api-types';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  cookieService = inject(CookieService);

  currentUser: UserReply;

  constructor(private apiService: KratosServiceService) {
    this.currentUser = JSON.parse(this.cookieService.get('currentUser'));
    console.log("Current User: \n" + JSON.stringify(this.currentUser));
  }

  ngOnInit(): void { }
}
