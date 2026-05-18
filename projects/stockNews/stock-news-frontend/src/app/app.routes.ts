import {  Routes } from '@angular/router';
import { LoginSignupComponent } from './login-signup/login-signup.component';
import { PortfolioDashboardComponent } from './portfolio-dashboard/portfolio-dashboard.component';
import { SettingsComponent } from './settings/settings.component';

export const routes: Routes = [
    { path: 'login', redirectTo: '/dashboard', pathMatch: 'full' },
    { path: 'dashboard', component: PortfolioDashboardComponent },
    { path: 'settings', component: SettingsComponent },
    { path: '', redirectTo: '/dashboard', pathMatch: 'full' }
];