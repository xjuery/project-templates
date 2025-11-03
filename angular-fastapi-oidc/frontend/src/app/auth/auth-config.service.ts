import { Injectable } from '@angular/core';
import { AuthConfig, OAuthService } from 'angular-oauth2-oidc';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthConfigService {

  constructor(private oauthService: OAuthService) {}

  configure(): void {
    const authConfig: AuthConfig = {
      issuer: environment.oidcIssuer,
      redirectUri: environment.redirectUri,
      clientId: environment.clientId,
      scope: environment.scope,
      responseType: 'code', // Authorization Code Flow - PKCE is automatically enabled
      requireHttps: false, // Disable for development
      showDebugInformation: true,
      skipIssuerCheck: true, // Skip issuer check for development
      strictDiscoveryDocumentValidation: false
    };

    this.oauthService.configure(authConfig);
    this.oauthService.loadDiscoveryDocumentAndTryLogin();
  }
}

