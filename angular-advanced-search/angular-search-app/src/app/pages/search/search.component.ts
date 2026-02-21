import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { CardModule } from 'primeng/card';
import { DividerModule } from 'primeng/divider';
import { BadgeModule } from 'primeng/badge';
import { ToastModule } from 'primeng/toast';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { MessageService } from 'primeng/api';
import { FilterBuilderComponent } from '../../components/filter-builder/filter-builder.component';
import { SearchService } from '../../services/search.service';
import { FieldDefinition, SearchFilter, Combinator, SearchQuery } from '../../models/search.models';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    InputTextModule,
    CardModule,
    DividerModule,
    BadgeModule,
    ToastModule,
    ProgressSpinnerModule,
    FilterBuilderComponent,
  ],
  providers: [MessageService],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit {
  private searchService = inject(SearchService);
  private router = inject(Router);
  private messageService = inject(MessageService);

  fields: FieldDefinition[] = [];
  filters: SearchFilter[] = [];
  combinator: Combinator = 'and';
  searchText = '';
  loading = false;
  fieldsLoading = true;

  ngOnInit(): void {
    // Restore previous query if available
    const prev = this.searchService.getCurrentQuery();
    if (prev) {
      this.searchText = prev.text;
      this.filters = prev.filters;
      this.combinator = prev.combinator;
    }

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
          detail: 'Unable to connect to mock server. Make sure it is running on port 3000.',
          life: 6000,
        });
      },
    });
  }

  onFiltersChange(filters: SearchFilter[]): void {
    this.filters = filters;
  }

  onCombinatorChange(combinator: Combinator): void {
    this.combinator = combinator;
  }

  clearFilters(): void {
    this.filters = [];
    this.searchText = '';
    this.combinator = 'and';
  }

  search(): void {
    const query: SearchQuery = {
      text: this.searchText,
      filters: this.filters,
      combinator: this.combinator,
      page: 1,
      pageSize: 10,
      sortField: 'id',
      sortOrder: 'asc',
    };
    this.searchService.search(query).subscribe({
      next: () => {
        this.router.navigate(['/results']);
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Search Failed',
          detail: 'Unable to reach the mock server. Please ensure it is running.',
          life: 5000,
        });
      },
    });
  }

  get activeFilterCount(): number {
    return this.filters.length;
  }

  get hasSearch(): boolean {
    return this.searchText.trim().length > 0 || this.filters.length > 0;
  }
}
