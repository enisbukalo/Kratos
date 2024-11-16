import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewSetDialogComponent } from './new-set-dialog.component';

describe('NewSetDialogComponent', () => {
  let component: NewSetDialogComponent;
  let fixture: ComponentFixture<NewSetDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewSetDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewSetDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
