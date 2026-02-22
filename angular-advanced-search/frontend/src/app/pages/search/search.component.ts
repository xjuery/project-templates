import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule, TableLazyLoadEvent } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { CardModule } from 'primeng/card';
import { DividerModule } from 'primeng/divider';
import { TagModule } from 'primeng/tag';
import { ToastModule } from 'primeng/toast';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { TooltipModule } from 'primeng/tooltip';
import { SelectModule } from 'primeng/select';
import { MessageService } from 'primeng/api';
import { FilterBuilderComponent } from '../../components/filter-builder/filter-builder.component';
import { SearchService } from '../../services/search.service';
import {
  FieldDefinition,
  SearchFilter,
  Combinator,
  SearchQuery,
  SearchResponse,
} from '../../models/search.models';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    CardModule,
    DividerModule,
    TagModule,
    ToastModule,
    ProgressSpinnerModule,
    TooltipModule,
    SelectModule,
    FilterBuilderComponent,
  ],
  providers: [MessageService],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit {
  private searchService = inject(SearchService);
  private messageService = inject(MessageService);

  Math = Math;

  // Field definitions from the API
  fields: FieldDefinition[] = [];
  fieldsLoading = true;

  // Form state — what the user is currently editing
  searchText = '';
  filters: SearchFilter[] = [];
  combinator: Combinator = 'and';

  // Applied query — the criteria used for the current results
  // (separate from form state so sort/page changes don't re-run the form)
  private appliedText = '';
  private appliedFilters: SearchFilter[] = [];
  private appliedCombinator: Combinator = 'and';

  // Results state
  results: Record<string, any>[] = [];
  totalRecords = 0;
  resultsLoading = false;
  hasSearched = false;

  // Table state
  currentPage = 1;
  pageSize = 10;
  sortField = 'id';
  sortOrder: 'asc' | 'desc' = 'asc';

  pageSizeOptions = [
    { label: '10 per page', value: 10 },
    { label: '25 per page', value: 25 },
    { label: '50 per page', value: 50 },
  ];

  ngOnInit(): void {
    this.searchService.getFields().subscribe({
      next: (fields) => {
        this.fields = fields;
        this.fieldsLoading = false;
      },
      error: () => {
        this.fieldsLoading = false;
        this.messageService.add({
          severity: 'error',
          summary: 'Connection Error',
          detail: 'Unable to connect to the FastAPI backend. Make sure it is running on port 8000.',
          life: 6000,
        });
      },
    });
  }

  // ── Form event handlers ──────────────────────────────────────────────────

  onFiltersChange(filters: SearchFilter[]): void {
    this.filters = filters;
  }

  onCombinatorChange(combinator: Combinator): void {
    this.combinator = combinator;
  }

  // ── Search / reset ───────────────────────────────────────────────────────

  search(): void {
    // Capture the current form state as the applied query and reset pagination
    this.appliedText = this.searchText;
    this.appliedFilters = [...this.filters];
    this.appliedCombinator = this.combinator;
    this.currentPage = 1;
    this.sortField = 'id';
    this.sortOrder = 'asc';
    this.hasSearched = true;
    this.fetchResults();
  }

  reset(): void {
    this.searchText = '';
    this.filters = [];
    this.combinator = 'and';
    this.appliedText = '';
    this.appliedFilters = [];
    this.appliedCombinator = 'and';
    this.results = [];
    this.totalRecords = 0;
    this.hasSearched = false;
    this.currentPage = 1;
    this.sortField = 'id';
    this.sortOrder = 'asc';
  }

  // ── Table event handlers ─────────────────────────────────────────────────

  onLazyLoad(event: TableLazyLoadEvent): void {
    if (!this.hasSearched) return;

    this.currentPage = Math.floor((event.first ?? 0) / (event.rows ?? this.pageSize)) + 1;
    this.pageSize = event.rows ?? this.pageSize;

    if (event.sortField) {
      this.sortField = Array.isArray(event.sortField) ? event.sortField[0] : event.sortField;
      this.sortOrder = event.sortOrder === -1 ? 'desc' : 'asc';
    }

    this.fetchResults();
  }

  onPageSizeChange(): void {
    this.currentPage = 1;
    this.fetchResults();
  }

  // ── Data fetching ────────────────────────────────────────────────────────

  private fetchResults(): void {
    this.resultsLoading = true;

    const query: SearchQuery = {
      text: this.appliedText,
      filters: this.appliedFilters,
      combinator: this.appliedCombinator,
      page: this.currentPage,
      pageSize: this.pageSize,
      sortField: this.sortField,
      sortOrder: this.sortOrder,
    };

    this.searchService.search(query).subscribe({
      next: (response: SearchResponse) => {
        this.results = response.data;
        this.totalRecords = response.total;
        this.resultsLoading = false;
      },
      error: () => {
        this.resultsLoading = false;
        this.messageService.add({
          severity: 'error',
          summary: 'Search Failed',
          detail: 'Unable to reach the FastAPI backend. Please ensure it is running on port 8000.',
          life: 5000,
        });
      },
    });
  }

  // ── CSV export ───────────────────────────────────────────────────────────

  exportCSV(): void {
    if (!this.hasSearched || this.fields.length === 0) return;

    const exportQuery: SearchQuery = {
      text: this.appliedText,
      filters: this.appliedFilters,
      combinator: this.appliedCombinator,
      page: 1,
      pageSize: 10000,
      sortField: this.sortField,
      sortOrder: this.sortOrder,
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

  // ── Cell rendering ───────────────────────────────────────────────────────

  formatCellValue(value: any, fieldType: string): string {
    if (value === null || value === undefined) return '-';
    if (fieldType === 'boolean') return value ? 'Yes' : 'No';
    if (fieldType === 'date') {
      return new Date(value).toLocaleDateString('en-GB', {
        year: 'numeric', month: 'short', day: '2-digit',
      });
    }
    if (fieldType === 'number') return Number(value).toLocaleString();
    return String(value);
  }

  getBooleanSeverity(value: any): 'success' | 'danger' {
    return value === true || value === 'true' ? 'success' : 'danger';
  }

  // ── Computed helpers ─────────────────────────────────────────────────────

  get activeFilterCount(): number {
    return this.filters.length;
  }

  get hasFormInput(): boolean {
    return this.searchText.trim().length > 0 || this.filters.length > 0;
  }

  get isDirty(): boolean {
    return (
      this.searchText !== this.appliedText ||
      this.combinator !== this.appliedCombinator ||
      JSON.stringify(this.filters) !== JSON.stringify(this.appliedFilters)
    );
  }
}
