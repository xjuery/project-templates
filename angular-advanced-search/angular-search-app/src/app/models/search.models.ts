export type FieldType = 'string' | 'number' | 'date' | 'boolean';

export interface FieldDefinition {
  field: string;
  label: string;
  type: FieldType;
}

export interface FilterOperator {
  value: string;
  label: string;
}

export const STRING_OPERATORS: FilterOperator[] = [
  { value: 'contains', label: 'contains' },
  { value: 'not_contains', label: 'does not contain' },
  { value: 'equals', label: 'equals' },
  { value: 'not_equals', label: 'does not equal' },
  { value: 'starts_with', label: 'starts with' },
  { value: 'ends_with', label: 'ends with' },
  { value: 'is_empty', label: 'is empty' },
  { value: 'is_not_empty', label: 'is not empty' },
];

export const NUMBER_OPERATORS: FilterOperator[] = [
  { value: 'equals', label: '= equals' },
  { value: 'not_equals', label: '≠ not equals' },
  { value: 'greater_than', label: '> greater than' },
  { value: 'greater_than_or_equal', label: '≥ greater than or equal' },
  { value: 'less_than', label: '< less than' },
  { value: 'less_than_or_equal', label: '≤ less than or equal' },
  { value: 'between', label: 'between (min,max)' },
];

export const DATE_OPERATORS: FilterOperator[] = [
  { value: 'before', label: 'before' },
  { value: 'after', label: 'after' },
  { value: 'equals', label: 'on date' },
  { value: 'not_equals', label: 'not on date' },
  { value: 'before_or_equals', label: 'on or before' },
  { value: 'after_or_equals', label: 'on or after' },
  { value: 'between', label: 'between (date1,date2)' },
];

export const BOOLEAN_OPERATORS: FilterOperator[] = [
  { value: 'equals', label: 'is' },
  { value: 'not_equals', label: 'is not' },
];

export function getOperatorsForType(type: FieldType): FilterOperator[] {
  switch (type) {
    case 'string': return STRING_OPERATORS;
    case 'number': return NUMBER_OPERATORS;
    case 'date': return DATE_OPERATORS;
    case 'boolean': return BOOLEAN_OPERATORS;
    default: return STRING_OPERATORS;
  }
}

export function needsValueInput(operator: string): boolean {
  return !['is_empty', 'is_not_empty'].includes(operator);
}

export interface SearchFilter {
  id: string;
  field: string;
  operator: string;
  value: any;
}

export type Combinator = 'and' | 'or';

export interface SearchQuery {
  text: string;
  filters: SearchFilter[];
  combinator: Combinator;
  page: number;
  pageSize: number;
  sortField: string;
  sortOrder: 'asc' | 'desc';
}

export interface SearchResponse {
  data: Record<string, any>[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
