import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule, ButtonModule, DialogModule],
  template: `
    <p-dialog
      [visible]="visible"
      [modal]="true"
      [style]="{width: '450px'}"
      [header]="header"
      (onHide)="closeDialog()">

      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle" style="color: var(--accent-2); font-size: 2rem;"></i>
        <span>{{message}}</span>
      </div>

      <ng-template pTemplate="footer">
        <button pButton label="No" icon="pi pi-times" class="p-button-text" (click)="onReject()"></button>
        <button pButton label="Yes" icon="pi pi-check" class="p-button-danger" (click)="onConfirm()"></button>
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .confirmation-content {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1rem;
      padding: 1rem;
    }
  `]
})
export class ConfirmDialogComponent {
  @Input() visible: boolean = false;
  @Input() header: string = 'Confirmation';
  @Input() message: string = 'Are you sure you want to proceed?';
  @Output() confirm = new EventEmitter<void>();
  @Output() reject = new EventEmitter<void>();
  @Output() hide = new EventEmitter<void>();

  onConfirm() {
    this.confirm.emit();
    this.visible = false;
  }

  onReject() {
    this.reject.emit();
    this.visible = false;
  }

  closeDialog() {
    this.hide.emit();
    this.visible = false;
  }
}
