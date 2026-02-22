import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

/** Available object types — add new entries here to extend the app */
export const OBJECT_TYPES = [
  { id: 'person', label: 'Person', icon: 'pi-user' },
  { id: 'product', label: 'Product', icon: 'pi-box' },
];

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  readonly objectTypes = OBJECT_TYPES;
}
