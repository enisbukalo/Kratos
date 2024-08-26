import { Component } from '@angular/core';
import { KratosServiceService } from '../kratos-service.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  constructor(private apiService: KratosServiceService) { }

  ngOnInit(): void {
    this.apiService.getUser(1).subscribe((users) => {
      console.log(users);
    });
  }
}
