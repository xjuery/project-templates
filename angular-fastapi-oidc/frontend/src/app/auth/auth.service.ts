import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(private oauthService: OAuthService) {
    // Update authentication state when token is received or cleared
    this.oauthService.events.subscribe(event => {
      this.isAuthenticatedSubject.next(this.oauthService.hasValidAccessToken());
    });
  }

  login(): void {
    this.oauthService.initCodeFlow();
  }

  logout(): void {
    this.oauthService.logOut();
    this.isAuthenticatedSubject.next(false);
  }

  isAuthenticated(): boolean {
    return this.oauthService.hasValidAccessToken();
  }

  getAccessToken(): string {
    return this.oauthService.getAccessToken();
  }

  getAccessTokenAsObservable(): Observable<string> {
    return new Observable(observer => {
      observer.next(this.oauthService.getAccessToken());
      observer.complete();
    });
  }

  getClaims(): any {
    return this.oauthService.getIdentityClaims();
  }
}

