import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'search', pathMatch: 'full' },
  {
    path: 'search',
    loadComponent: () =>
      import('./pages/search/search.component').then(m => m.SearchComponent),
  },
  {
    path: 'results',
    loadComponent: () =>
      import('./pages/results/results.component').then(m => m.ResultsComponent),
  },
  { path: '**', redirectTo: 'search' },
];
