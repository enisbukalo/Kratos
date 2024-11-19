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
import { ConfirmDialogComponent } from '../confirm-dialog/confirm-dialog.component';

/**
 * Login component that handles user authentication.
 * Manages user login state and redirects to appropriate pages based on authentication status.
 */
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, MessagesModule, MessageModule, ToastModule, CommonModule, AvatarModule, CardModule, ButtonModule, SkeletonModule, InputNumberModule, DividerModule, ConfirmDialogComponent],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  providers: [MessageService],
})
export class LoginComponent implements OnInit {
  @Input() user!: UserReply;

  alertLifetime: number = 3000;

  currentUser: String;
  users: UserReply[] = [];

  newUserName: string = "First Last";
  newUserWeight: number = 0;
  newUserHeight: number = 0;

  cookieService = inject(CookieService);
  toastModule = inject(ToastModule);
  router = inject(Router);

  showDeleteDialog: boolean = false;
  userToDelete?: UserReply;

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
    this.messageService.add({ severity: 'success', summary: 'Success Message', detail: 'User Created Successfully', life: this.alertLifetime });
  }

  showError(): void {
    this.messageService.add({ severity: 'error', summary: 'Error Message', detail: 'Failed Creating User', life: this.alertLifetime });
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

  /**
   * Deletes a user from the system
   * @param event Mouse event to prevent event bubbling
   * @param user User to be deleted
   */
  deleteUser(event: Event, user: UserReply): void {
    event.stopPropagation();
    this.userToDelete = user;
    this.showDeleteDialog = true;
  }

  confirmDelete(): void {
    if (!this.userToDelete?.id) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Invalid user ID',
        life: this.alertLifetime
      });
      return;
    }

    this.apiService.deleteUser(this.userToDelete.id).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'User Deleted Successfully',
          life: this.alertLifetime
        });
        this.getAllUsers();
      },
      error: (error) => {
        console.error('Error Deleting User:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to delete user',
          life: this.alertLifetime
        });
      }
    });
  }
}
