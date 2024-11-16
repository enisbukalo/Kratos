import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewWorkoutDialogComponent } from './new-workout-dialog.component';

describe('NewWorkoutDialogComponent', () => {
  let component: NewWorkoutDialogComponent;
  let fixture: ComponentFixture<NewWorkoutDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewWorkoutDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewWorkoutDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
