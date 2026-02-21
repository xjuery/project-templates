import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { SelectModule } from 'primeng/select';
import { InputTextModule } from 'primeng/inputtext';
import { DatePickerModule } from 'primeng/datepicker';
import { ToggleSwitchModule } from 'primeng/toggleswitch';
import { TagModule } from 'primeng/tag';
import { TooltipModule } from 'primeng/tooltip';
import {
  FieldDefinition,
  SearchFilter,
  Combinator,
  getOperatorsForType,
  needsValueInput,
  FilterOperator,
} from '../../models/search.models';

@Component({
  selector: 'app-filter-builder',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    SelectModule,
    InputTextModule,
    DatePickerModule,
    ToggleSwitchModule,
    TagModule,
    TooltipModule,
  ],
  templateUrl: './filter-builder.component.html',
  styleUrls: ['./filter-builder.component.scss'],
})
export class FilterBuilderComponent implements OnChanges {
  @Input() fields: FieldDefinition[] = [];
  @Input() filters: SearchFilter[] = [];
  @Input() combinator: Combinator = 'and';

  @Output() filtersChange = new EventEmitter<SearchFilter[]>();
  @Output() combinatorChange = new EventEmitter<Combinator>();

  combinatorOptions = [
    { label: 'AND', value: 'and' },
    { label: 'OR', value: 'or' },
  ];

  fieldOptions: { label: string; value: string }[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['fields']) {
      this.fieldOptions = this.fields.map(f => ({ label: f.label, value: f.field }));
    }
  }

  getOperatorsForFilter(filter: SearchFilter): FilterOperator[] {
    const fieldDef = this.fields.find(f => f.field === filter.field);
    return fieldDef ? getOperatorsForType(fieldDef.type) : [];
  }

  getFieldType(filter: SearchFilter): string {
    const fieldDef = this.fields.find(f => f.field === filter.field);
    return fieldDef?.type ?? 'string';
  }

  needsValue(filter: SearchFilter): boolean {
    return needsValueInput(filter.operator);
  }

  isBooleanFilter(filter: SearchFilter): boolean {
    return this.getFieldType(filter) === 'boolean';
  }

  isDateFilter(filter: SearchFilter): boolean {
    return this.getFieldType(filter) === 'date';
  }

  isNumberFilter(filter: SearchFilter): boolean {
    return this.getFieldType(filter) === 'number';
  }

  isStringFilter(filter: SearchFilter): boolean {
    return this.getFieldType(filter) === 'string';
  }

  addFilter(): void {
    const firstField = this.fields[0];
    const newFilter: SearchFilter = {
      id: crypto.randomUUID(),
      field: firstField?.field ?? '',
      operator: firstField ? getOperatorsForType(firstField.type)[0].value : 'contains',
      value: '',
    };
    this.filtersChange.emit([...this.filters, newFilter]);
  }

  removeFilter(id: string): void {
    this.filtersChange.emit(this.filters.filter(f => f.id !== id));
  }

  onFieldChange(filter: SearchFilter, newField: string): void {
    const fieldDef = this.fields.find(f => f.field === newField);
    const ops = fieldDef ? getOperatorsForType(fieldDef.type) : [];
    const updated = this.filters.map(f =>
      f.id === filter.id
        ? { ...f, field: newField, operator: ops[0]?.value ?? 'contains', value: '' }
        : f
    );
    this.filtersChange.emit(updated);
  }

  onOperatorChange(filter: SearchFilter, newOperator: string): void {
    const updated = this.filters.map(f =>
      f.id === filter.id ? { ...f, operator: newOperator, value: '' } : f
    );
    this.filtersChange.emit(updated);
  }

  onValueChange(filter: SearchFilter, newValue: any): void {
    const updated = this.filters.map(f =>
      f.id === filter.id ? { ...f, value: newValue } : f
    );
    this.filtersChange.emit(updated);
  }

  onCombinatorChange(value: Combinator): void {
    this.combinatorChange.emit(value);
  }

  getFieldLabel(fieldValue: string): string {
    return this.fields.find(f => f.field === fieldValue)?.label ?? fieldValue;
  }

  getBooleanValue(filter: SearchFilter): boolean {
    return filter.value === true || filter.value === 'true';
  }

  onBooleanChange(filter: SearchFilter, value: boolean): void {
    this.onValueChange(filter, value);
  }

  onDateChange(filter: SearchFilter, date: Date | null): void {
    this.onValueChange(filter, date ? date.toISOString() : '');
  }

  getDateValue(filter: SearchFilter): Date | null {
    return filter.value ? new Date(filter.value) : null;
  }
}
