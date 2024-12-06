import { Component, OnInit } from '@angular/core';
import { TutorialsService } from './servicios/tutorials.service';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'frontend';
  msg: any;

  constructor(private tService: TutorialsService) {}

  ngOnInit(): void {
    this.showMessage();
  }

  showMessage() {
    this.tService.getMessage().subscribe((data: any) => {
      this.msg = data;
      console.log(this.msg); 
    });
  }
}
