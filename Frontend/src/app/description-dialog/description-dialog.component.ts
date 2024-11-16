import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-description-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule
  ],
  template: `
        <h2 mat-dialog-title>Exercise Description</h2>
        <mat-dialog-content>
            <p>{{data.description}}</p>
        </mat-dialog-content>
        <mat-dialog-actions align="end">
            <button mat-button mat-dialog-close>Close</button>
        </mat-dialog-actions>
    `,
  styles: [`
        :host {
            display: block;
            background: var(--surface-2);
            color: var(--text-primary);
            padding: 1rem;
        }

        p {
            color: var(--text-secondary);
            line-height: 1.5;
            margin: 1rem 0;
        }
    `]
})
export class DescriptionDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { description: string }) { }
}
