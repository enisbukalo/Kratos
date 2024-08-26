import { Component, inject, Input } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { KratosServiceService } from '../kratos-service.service';
import { GetQueryParams, UserReply } from '../kratos-api-types';
import { CommonModule } from '@angular/common';
import { AvatarModule } from 'primeng/avatar';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, AvatarModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  @Input() user!: UserReply;

  currentUserId: number;
  users: UserReply[] = [];

  cookieService = inject(CookieService);

  constructor(private apiService: KratosServiceService) {
    this.currentUserId = Number(this.cookieService.get('currentUserId'));
  }

  ngOnInit(): void {
    const queryParams: GetQueryParams = { 'page_size': 10, 'page_number': 1, 'sort': false };
    this.apiService.getUsers(queryParams).subscribe((users) => {
      this.users = users;
      console.log(users);
    });
  }

  getFirstLetter(name?: string) {
    return name?.charAt(0) == null ? '' : name.charAt(0).toUpperCase();
  }
}
