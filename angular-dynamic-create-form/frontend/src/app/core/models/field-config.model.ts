export type FieldType = 'text' | 'email' | 'number' | 'date' | 'boolean' | 'select' | 'textarea';

export interface SelectOption {
  label: string;
  value: string | number;
}

export interface FieldConfig {
  name: string;
  label: string;
  type: FieldType;
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: string;
  default?: unknown;
  options?: SelectOption[];
  placeholder?: string;
  hint?: string;
}

export interface ObjectTypeConfig {
  objectType: string;
  displayName: string;
  apiEndpoint: string;
  fields: FieldConfig[];
}
