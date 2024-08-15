import { TestBed } from '@angular/core/testing';

import { KratosServiceService } from './kratos-service.service';

describe('KratosServiceService', () => {
  let service: KratosServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(KratosServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
