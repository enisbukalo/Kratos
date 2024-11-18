import { Component, inject, Input, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { KratosServiceService } from '../kratos-service.service';
import { CreateUser, GetQueryParams, UserReply } from '../kratos-api-types';
import { CommonModule } from '@angular/common';
import { AvatarModule } from 'primeng/avatar';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { SkeletonModule } from 'primeng/skeleton';
import { InputNumberModule } from 'primeng/inputnumber';
import { DividerModule } from 'primeng/divider';
import { FormsModule } from '@angular/forms';
import { ToastModule } from 'primeng/toast';
import { MessageModule } from 'primeng/message';
import { MessagesModule } from 'primeng/messages';
import { MessageService } from 'primeng/api';
import { UserStateService } from '../services/user-state.service';

/**
 * Login component that handles user authentication.
 * Manages user login state and redirects to appropriate pages based on authentication status.
 */
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, MessagesModule, MessageModule, ToastModule, CommonModule, AvatarModule, CardModule, ButtonModule, SkeletonModule, InputNumberModule, DividerModule,],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  providers: [MessageService],
})
export class LoginComponent implements OnInit {
  @Input() user!: UserReply;

  currentUser: String;
  users: UserReply[] = [];

  newUserName: string = "First Last";
  newUserWeight: number = 0;
  newUserHeight: number = 0;

  cookieService = inject(CookieService);
  toastModule = inject(ToastModule);
  router = inject(Router);

  constructor(
    private apiService: KratosServiceService,
    private messageService: MessageService,
    private userState: UserStateService
  ) {
    this.currentUser = this.cookieService.get('currentUser');
    this.messageService.clear();
  }

  /**
   * Initializes the component and checks for existing authentication
   */
  ngOnInit(): void {
    this.getAllUsers();
  }

  getAllUsers(): void {
    const queryParams: GetQueryParams = { 'page_size': 10, 'page_number': 1, 'sort': false };
    this.apiService.getUsers(queryParams).subscribe((users) => {
      this.users = users;
      console.log(users);
    });
  }

  getFirstLetter(name?: string) {
    return name?.charAt(0) == null ? '' : name.charAt(0).toUpperCase();
  }

  selectUser(user: UserReply): void {
    this.cookieService.set('currentUser', JSON.stringify(user));
    this.userState.setCurrentUser(user);
    this.router.navigate(['dashboard']);
  }

  createUser(name: string, height: number, weight: number): void {
    const user: CreateUser = { name: name, height: height, weight: weight };
    this.apiService.createUser(user).subscribe({
      next: (user) => {
        console.log("User Created: \n" + JSON.stringify(user));
        this.showSuccess();
        this.getAllUsers();
      },
      error: (error) => {
        console.log(error);
        this.showError();
      }
    });
  }

  showSuccess(): void {
    this.messageService.add({ severity: 'success', summary: 'Success Message', detail: 'User Create Successfully' });
  }

  showError(): void {
    this.messageService.add({ severity: 'error', summary: 'Error Message', detail: 'Failed Creating User' });
  }

  hideMessages() {
    this.messageService.clear();
  }

  /**
   * Handles the login form submission
   * @param event Form submission event
   */
  onSubmit(event: Event): void {
    // implementation
  }

  /**
   * Navigates to the registration page
   */
  goToRegister(): void {
    // implementation
  }

  /**
   * Handles successful login response
   * @param response Login response from the API
   */
  private handleLoginSuccess(response: any): void {
    // implementation
  }

  /**
   * Handles login error
   * @param error Error from the API
   */
  private handleLoginError(error: any): void {
    // implementation
  }
}
