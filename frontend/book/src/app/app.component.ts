import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <!-- routes to other pages -->
    <router-outlet></router-outlet>
  `,
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'book';
}
