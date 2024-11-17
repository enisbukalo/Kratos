import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { UserReply } from '../kratos-api-types';
import { KratosServiceService } from '../kratos-service.service';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
    providedIn: 'root'
})
export class UserStateService {
    private currentUser = new BehaviorSubject<UserReply | null>(null);
    currentUser$ = this.currentUser.asObservable();

    constructor(
        private apiService: KratosServiceService,
        private cookieService: CookieService
    ) {
        const userString = this.cookieService.get('currentUser');
        if (userString) {
            this.currentUser.next(JSON.parse(userString));
        }
    }

    setCurrentUser(user: UserReply) {
        this.currentUser.next(user);
    }

    getCurrentUserId(): number {
        return this.currentUser.value?.id || 0;
    }

    refreshUserData() {
        const currentUserValue = this.currentUser.value;
        if (currentUserValue?.id) {
            this.apiService.getUser(currentUserValue.id).subscribe(user => {
                this.currentUser.next(user);
                this.cookieService.set('currentUser', JSON.stringify(user));
            });
        }
    }
}