import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, tap } from 'rxjs';
import { ObjectTypeConfig } from '../models/field-config.model';

@Injectable({ providedIn: 'root' })
export class ObjectConfigService {
  private http = inject(HttpClient);
  private cache = new Map<string, ObjectTypeConfig>();

  getConfig(objectType: string): Observable<ObjectTypeConfig> {
    if (this.cache.has(objectType)) {
      return of(this.cache.get(objectType)!);
    }
    return this.http
      .get<ObjectTypeConfig>(`assets/object-types/${objectType}.json`)
      .pipe(tap((config) => this.cache.set(objectType, config)));
  }
}
