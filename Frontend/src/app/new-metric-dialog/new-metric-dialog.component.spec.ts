import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewMetricDialogComponent } from './new-metric-dialog.component';

describe('NewMetricDialogComponent', () => {
  let component: NewMetricDialogComponent;
  let fixture: ComponentFixture<NewMetricDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewMetricDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewMetricDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
