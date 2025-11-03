import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  userInfo: any = null;
  backendData: any = null;
  error: string | null = null;

  constructor(
    private http: HttpClient,
    public authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loadUserInfo();
    this.loadBackendData();
  }

  loadUserInfo(): void {
    this.userInfo = this.authService.getClaims();
  }

  loadBackendData(): void {
    this.http.get(`${environment.apiUrl}/api/user/profile`).subscribe({
      next: (data) => {
        this.backendData = data;
        this.error = null;
      },
      error: (err) => {
        this.error = 'Failed to load backend data. Make sure the backend is running.';
        console.error(err);
      }
    });
  }

  logout(): void {
    this.authService.logout();
  }
}

