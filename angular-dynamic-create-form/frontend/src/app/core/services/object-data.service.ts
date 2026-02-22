import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ObjectDataService {
  private http = inject(HttpClient);

  getAll(endpoint: string): Observable<Record<string, unknown>[]> {
    return this.http.get<Record<string, unknown>[]>(endpoint);
  }

  create(endpoint: string, data: Record<string, unknown>): Observable<Record<string, unknown>> {
    return this.http.post<Record<string, unknown>>(endpoint, data);
  }

  delete(endpoint: string, id: string | number): Observable<void> {
    return this.http.delete<void>(`${endpoint}/${id}`);
  }
}
