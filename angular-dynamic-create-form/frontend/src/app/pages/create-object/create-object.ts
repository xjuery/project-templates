import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Toast } from 'primeng/toast';
import { Card } from 'primeng/card';
import { ProgressSpinner } from 'primeng/progressspinner';
import { ObjectConfigService } from '../../core/services/object-config.service';
import { ObjectDataService } from '../../core/services/object-data.service';
import { ObjectTypeConfig } from '../../core/models/field-config.model';
import { DynamicForm } from '../../shared/components/dynamic-form/dynamic-form';

@Component({
  selector: 'app-create-object',
  imports: [Toast, Card, ProgressSpinner, RouterLink, DynamicForm],
  providers: [MessageService],
  templateUrl: './create-object.html',
  styleUrl: './create-object.scss',
})
export class CreateObject implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private configService = inject(ObjectConfigService);
  private dataService = inject(ObjectDataService);
  private messageService = inject(MessageService);

  config = signal<ObjectTypeConfig | null>(null);
  loading = signal(false);
  configLoading = signal(true);
  objectType = signal('');

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const type = params.get('objectType') ?? '';
      this.objectType.set(type);
      this.loadConfig(type);
    });
  }

  private loadConfig(objectType: string): void {
    this.configLoading.set(true);
    this.config.set(null);
    this.configService.getConfig(objectType).subscribe({
      next: (cfg) => {
        this.config.set(cfg);
        this.configLoading.set(false);
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: `Could not load configuration for "${objectType}"`,
        });
        this.configLoading.set(false);
      },
    });
  }

  onFormSubmit(data: Record<string, unknown>): void {
    const cfg = this.config();
    if (!cfg) return;

    this.loading.set(true);
    this.dataService.create(cfg.apiEndpoint, data).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Created',
          detail: `${cfg.displayName} has been created successfully`,
          life: 3000,
        });
        this.loading.set(false);
        // Navigate to list after a short delay
        setTimeout(() => {
          this.router.navigate(['/objects', this.objectType(), 'list']);
        }, 1500);
      },
      error: (err) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: err?.error?.message ?? 'Failed to create. Please try again.',
        });
        this.loading.set(false);
      },
    });
  }
}
