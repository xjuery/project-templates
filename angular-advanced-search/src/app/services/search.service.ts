import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { FieldDefinition, SearchQuery, SearchResponse } from '../models/search.models';

@Injectable({ providedIn: 'root' })
export class SearchService {
  private http = inject(HttpClient);
  private readonly API_URL = 'http://localhost:3000/api';

  private currentQuerySubject = new BehaviorSubject<SearchQuery | null>(null);
  currentQuery$ = this.currentQuerySubject.asObservable();

  getFields(): Observable<FieldDefinition[]> {
    return this.http.get<FieldDefinition[]>(`${this.API_URL}/fields`);
  }

  search(query: SearchQuery): Observable<SearchResponse> {
    this.currentQuerySubject.next(query);
    return this.http.post<SearchResponse>(`${this.API_URL}/search`, query);
  }

  getCurrentQuery(): SearchQuery | null {
    return this.currentQuerySubject.getValue();
  }
}
