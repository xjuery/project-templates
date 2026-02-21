import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TableModule, TableLazyLoadEvent } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { CardModule } from 'primeng/card';
import { TagModule } from 'primeng/tag';
import { ToastModule } from 'primeng/toast';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { TooltipModule } from 'primeng/tooltip';
import { SelectModule } from 'primeng/select';
import { DividerModule } from 'primeng/divider';
import { MessageService } from 'primeng/api';
import { SearchService } from '../../services/search.service';
import { FieldDefinition, SearchQuery, SearchResponse } from '../../models/search.models';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    CardModule,
    TagModule,
    ToastModule,
    ProgressSpinnerModule,
    TooltipModule,
    SelectModule,
    DividerModule,
  ],
  providers: [MessageService],
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss'],
})
export class ResultsComponent implements OnInit {
  private searchService = inject(SearchService);
  private router = inject(Router);
  private messageService = inject(MessageService);

  Math = Math;

  results: Record<string, any>[] = [];
  fields: FieldDefinition[] = [];
  loading = true;
  totalRecords = 0;
  currentPage = 1;
  pageSize = 10;
  sortField = 'id';
  sortOrder: 'asc' | 'desc' = 'asc';
  currentQuery: SearchQuery | null = null;

  pageSizeOptions = [
    { label: '10 per page', value: 10 },
    { label: '25 per page', value: 25 },
    { label: '50 per page', value: 50 },
  ];

  ngOnInit(): void {
    this.currentQuery = this.searchService.getCurrentQuery();
    if (!this.currentQuery) {
      this.router.navigate(['/search']);
      return;
    }

    // Restore pagination and sort from query
    this.currentPage = this.currentQuery.page;
    this.pageSize = this.currentQuery.pageSize;
    this.sortField = this.currentQuery.sortField;
    this.sortOrder = this.currentQuery.sortOrder;

    this.loadFields();
    this.loadResults();
  }

  loadFields(): void {
    this.searchService.getFields().subscribe({
      next: (fields) => { this.fields = fields; },
    });
  }

  loadResults(): void {
    if (!this.currentQuery) return;
    this.loading = true;

    const query: SearchQuery = {
      ...this.currentQuery,
      page: this.currentPage,
      pageSize: this.pageSize,
      sortField: this.sortField,
      sortOrder: this.sortOrder,
    };

    this.searchService.search(query).subscribe({
      next: (response: SearchResponse) => {
        this.results = response.data;
        this.totalRecords = response.total;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load results. Please try again.',
          life: 5000,
        });
      },
    });
  }

  onLazyLoad(event: TableLazyLoadEvent): void {
    this.currentPage = Math.floor((event.first ?? 0) / (event.rows ?? this.pageSize)) + 1;
    this.pageSize = event.rows ?? this.pageSize;

    if (event.sortField) {
      this.sortField = Array.isArray(event.sortField) ? event.sortField[0] : event.sortField;
      this.sortOrder = event.sortOrder === -1 ? 'desc' : 'asc';
    }

    this.loadResults();
  }

  onPageSizeChange(): void {
    this.currentPage = 1;
    this.loadResults();
  }

  backToSearch(): void {
    this.router.navigate(['/search']);
  }

  exportCSV(): void {
    if (this.fields.length === 0 || !this.currentQuery) return;

    const exportQuery: SearchQuery = {
      ...this.currentQuery,
      page: 1,
      pageSize: 10000,
    };

    this.searchService.search(exportQuery).subscribe({
      next: (response: SearchResponse) => {
        const allData = response.data;
        const headers = this.fields.map(f => f.label);
        const rows = allData.map(item =>
          this.fields.map(f => {
            const val = item[f.field];
            if (val === null || val === undefined) return '';
            const str = String(val);
            if (str.includes(',') || str.includes('"') || str.includes('\n')) {
              return `"${str.replace(/"/g, '""')}"`;
            }
            return str;
          })
        );

        const csvContent = [
          headers.join(','),
          ...rows.map(r => r.join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `search-results-${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        URL.revokeObjectURL(link.href);

        this.messageService.add({
          severity: 'success',
          summary: 'Export Complete',
          detail: `${allData.length} records exported to CSV`,
          life: 3000,
        });
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Export Failed',
          detail: 'Unable to export results.',
          life: 3000,
        });
      },
    });
  }

  formatCellValue(value: any, fieldType: string): string {
    if (value === null || value === undefined) return '-';
    if (fieldType === 'boolean') return value ? 'Yes' : 'No';
    if (fieldType === 'date') {
      return new Date(value).toLocaleDateString('en-GB', {
        year: 'numeric', month: 'short', day: '2-digit'
      });
    }
    if (fieldType === 'number') return Number(value).toLocaleString();
    return String(value);
  }

  getBooleanSeverity(value: any): 'success' | 'danger' {
    return value === true || value === 'true' ? 'success' : 'danger';
  }

  get queryDescription(): string {
    if (!this.currentQuery) return '';
    const parts: string[] = [];
    if (this.currentQuery.text) {
      parts.push(`text: "${this.currentQuery.text}"`);
    }
    if (this.currentQuery.filters.length > 0) {
      parts.push(`${this.currentQuery.filters.length} filter(s) [${this.currentQuery.combinator.toUpperCase()}]`);
    }
    return parts.join(' + ') || 'All records';
  }
}
