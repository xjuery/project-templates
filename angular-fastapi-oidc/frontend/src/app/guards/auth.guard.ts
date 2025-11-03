import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Router, RouterStateSnapshot } from '@angular/router';
import { OAuthService } from 'angular-oauth2-oidc';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard {

  constructor(
    private oauthService: OAuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): boolean {
    
    const hasValidToken = this.oauthService.hasValidAccessToken();
    
    if (!hasValidToken) {
      this.oauthService.initCodeFlow();
      return false;
    }
    
    return true;
  }
}

