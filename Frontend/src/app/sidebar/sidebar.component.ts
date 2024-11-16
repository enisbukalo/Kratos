import { Component, Input, Output, EventEmitter, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { MatSidenav } from '@angular/material/sidenav';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, MaterialModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  @ViewChild('sidenav') sidenav!: MatSidenav;
  @Input() isOpen: boolean = false;
  @Output() dashboardClick = new EventEmitter<void>();
  @Output() profileClick = new EventEmitter<void>();
  @Output() loginClick = new EventEmitter<void>();

  constructor(private router: Router) { }

  onDashboardClick() {
    this.router.navigate(['/dashboard']);
    this.sidenav.close();
  }

  toggle() {
    this.sidenav.toggle();
  }
}
