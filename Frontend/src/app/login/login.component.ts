import { Component, inject, Input } from '@angular/core';
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

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, MessagesModule, MessageModule, ToastModule, CommonModule, AvatarModule, CardModule, ButtonModule, SkeletonModule, InputNumberModule, DividerModule,],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  providers: [MessageService],
})
export class LoginComponent {
  @Input() user!: UserReply;

  msgs: any[] = [
    {
      severity: 'success',
      summary: 'GeeksforGeeks',
      detail: "This is a message"
    },
    {
      severity: 'error',
      summary: 'GeeksforGeeks',
      detail: "This is a message"
    }
  ];
  currentUser: String;
  users: UserReply[] = [];

  newUserName: string = "First Last";
  newUserWeight: number = 0;
  newUserHeight: number = 0;

  cookieService = inject(CookieService);
  messageService: MessageService = inject(MessageService);
  toastModule = inject(ToastModule);
  router = inject(Router);

  constructor(private apiService: KratosServiceService) {
    this.currentUser = this.cookieService.get('currentUser');
    this.hideMessages();
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

  selectUser(user: UserReply): void {
    this.cookieService.set('currentUser', JSON.stringify(user));
    console.log("User Selected: \n" + this.cookieService.get('currentUser'));
    this.router.navigate(['home']);
  }

  createUser(name: string, height: number, weight: number): void {
    const user: CreateUser = { name: name, height: height, weight: weight };
    this.apiService.createUser(user).subscribe((user) => {
      console.log("User Created: \n" + JSON.stringify(user));
    });
    // this.showSuccess();
    window.location.reload();
  }

  showSuccess(): void {
    this.msgs.push({ severity: 'success', summary: 'Success Message', detail: 'User Create Successfully' });
  }

  showError(): void {
    this.msgs.push({ severity: 'error', summary: 'Error Message', detail: 'Failed Creating User' });
  }

  hideMessages() {
    this.msgs = [];
  }
}
