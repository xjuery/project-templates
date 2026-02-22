import { Routes } from '@angular/router';
import { CreateObject } from './pages/create-object/create-object';
import { ListObjects } from './pages/list-objects/list-objects';

export const routes: Routes = [
  { path: '', redirectTo: '/objects/person/create', pathMatch: 'full' },
  { path: 'objects/:objectType/create', component: CreateObject },
  { path: 'objects/:objectType/list', component: ListObjects },
  { path: '**', redirectTo: '/objects/person/create' },
];
