import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateExerciseDialogComponent } from './create-exercise-dialog.component';

describe('CreateExerciseDialogComponent', () => {
  let component: CreateExerciseDialogComponent;
  let fixture: ComponentFixture<CreateExerciseDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateExerciseDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateExerciseDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
