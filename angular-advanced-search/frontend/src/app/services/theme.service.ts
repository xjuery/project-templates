import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly STORAGE_KEY = 'theme';

  isDark = signal(false);

  constructor() {
    const saved = localStorage.getItem(this.STORAGE_KEY);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    // Saved preference wins; fall back to OS preference
    const dark = saved === 'dark' || (saved === null && prefersDark);
    this.isDark.set(dark);
    this.apply(dark);
  }

  toggle(): void {
    const next = !this.isDark();
    this.isDark.set(next);
    this.apply(next);
    localStorage.setItem(this.STORAGE_KEY, next ? 'dark' : 'light');
  }

  private apply(dark: boolean): void {
    const html = document.documentElement;
    html.classList.toggle('dark-mode', dark);
    // Tells the browser to switch native controls (inputs, scrollbars, etc.) to dark
    html.style.colorScheme = dark ? 'dark' : 'light';
  }
}
