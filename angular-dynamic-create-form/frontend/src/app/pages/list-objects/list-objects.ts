import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MessageService, ConfirmationService } from 'primeng/api';
import { Toast } from 'primeng/toast';
import { Card } from 'primeng/card';
import { Button } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { Tag } from 'primeng/tag';
import { ProgressSpinner } from 'primeng/progressspinner';
import { ConfirmDialog } from 'primeng/confirmdialog';
import { DatePipe } from '@angular/common';
import { ObjectConfigService } from '../../core/services/object-config.service';
import { ObjectDataService } from '../../core/services/object-data.service';
import { ObjectTypeConfig, FieldConfig } from '../../core/models/field-config.model';

@Component({
  selector: 'app-list-objects',
  imports: [
    Toast,
    Card,
    Button,
    TableModule,
    Tag,
    ProgressSpinner,
    ConfirmDialog,
    RouterLink,
    DatePipe,
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './list-objects.html',
  styleUrl: './list-objects.scss',
})
export class ListObjects implements OnInit {
  private route = inject(ActivatedRoute);
  private configService = inject(ObjectConfigService);
  private dataService = inject(ObjectDataService);
  private messageService = inject(MessageService);
  private confirmationService = inject(ConfirmationService);

  config = signal<ObjectTypeConfig | null>(null);
  objects = signal<Record<string, unknown>[]>([]);
  loading = signal(true);
  objectType = signal('');

  columns = computed<FieldConfig[]>(() => {
    return this.config()?.fields ?? [];
  });

  filterableFieldNames = computed<string[]>(() =>
    this.columns()
      .filter((f) => f.type !== 'textarea' && f.type !== 'boolean')
      .map((f) => f.name)
  );

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const type = params.get('objectType') ?? '';
      this.objectType.set(type);
      this.loadConfig(type);
    });
  }

  private loadConfig(objectType: string): void {
    this.loading.set(true);
    this.configService.getConfig(objectType).subscribe({
      next: (cfg) => {
        this.config.set(cfg);
        this.loadObjects(cfg.apiEndpoint);
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: `Could not load configuration for "${objectType}"`,
        });
        this.loading.set(false);
      },
    });
  }

  private loadObjects(endpoint: string): void {
    this.dataService.getAll(endpoint).subscribe({
      next: (data) => {
        this.objects.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Could not load objects',
        });
        this.loading.set(false);
      },
    });
  }

  refresh(): void {
    const cfg = this.config();
    if (cfg) {
      this.loading.set(true);
      this.loadObjects(cfg.apiEndpoint);
    }
  }

  confirmDelete(obj: Record<string, unknown>): void {
    this.confirmationService.confirm({
      message: 'Are you sure you want to delete this item?',
      header: 'Confirm Deletion',
      icon: 'pi pi-exclamation-triangle',
      accept: () => this.deleteObject(obj),
    });
  }

  private deleteObject(obj: Record<string, unknown>): void {
    const cfg = this.config();
    if (!cfg) return;
    const id = obj['id'] as string | number;
    this.dataService.delete(cfg.apiEndpoint, id).subscribe({
      next: () => {
        this.objects.update((items) => items.filter((item) => item['id'] !== id));
        this.messageService.add({
          severity: 'success',
          summary: 'Deleted',
          detail: 'Item deleted successfully',
          life: 3000,
        });
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to delete item',
        });
      },
    });
  }

  formatValue(value: unknown, field: FieldConfig): string {
    if (value === null || value === undefined) return '—';
    if (field.type === 'date' && value) {
      return new Date(value as string).toLocaleDateString();
    }
    return String(value);
  }

  isBoolean(field: FieldConfig): boolean {
    return field.type === 'boolean';
  }

  isDate(field: FieldConfig): boolean {
    return field.type === 'date';
  }
}
