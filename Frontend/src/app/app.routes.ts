import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { WorkoutComponent } from './workout/workout.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full'
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
    },
    {
        path: 'login',
        component: LoginComponent,
    },
    {
        path: 'workout/:id',
        component: WorkoutComponent,
    }
];
