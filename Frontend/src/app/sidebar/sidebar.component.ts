import { Component, Input, Output, EventEmitter, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { MatSidenav } from '@angular/material/sidenav';
import { Router } from '@angular/router';

/**
 * Sidebar navigation component that provides access to main application features.
 * Handles user navigation and displays current user information.
 */
@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, MaterialModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  @ViewChild('sidenav') sidenav!: MatSidenav;
  /**
   * Controls the visibility state of the sidebar
   */
  @Input() isOpen: boolean = false;
  /**
   * Emits when dashboard navigation is requested
   */
  @Output() dashboardClick = new EventEmitter<void>();
  /**
   * Emits when profile navigation is requested
   */
  @Output() profileClick = new EventEmitter<void>();
  /**
   * Emits when login navigation is requested
   */
  @Output() loginClick = new EventEmitter<void>();

  constructor(private router: Router) { }

  onDashboardClick() {
    this.router.navigate(['/dashboard']);
    this.sidenav.close();
  }

  /**
   * Toggles the sidebar visibility state
   */
  toggle() {
    this.sidenav.toggle();
  }
}
