import {
  Component,
  input,
  output,
  OnInit,
  OnChanges,
  SimpleChanges,
} from '@angular/core';
import {
  FormGroup,
  FormControl,
  Validators,
  ValidatorFn,
  ReactiveFormsModule,
} from '@angular/forms';
import { CommonModule } from '@angular/common';
import { InputText } from 'primeng/inputtext';
import { InputNumber } from 'primeng/inputnumber';
import { DatePicker } from 'primeng/datepicker';
import { Checkbox } from 'primeng/checkbox';
import { Select } from 'primeng/select';
import { Textarea } from 'primeng/textarea';
import { Button } from 'primeng/button';
import { Message } from 'primeng/message';
import { FieldConfig, ObjectTypeConfig } from '../.././../core/models/field-config.model';

@Component({
  selector: 'app-dynamic-form',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    InputText,
    InputNumber,
    DatePicker,
    Checkbox,
    Select,
    Textarea,
    Button,
    Message,
  ],
  templateUrl: './dynamic-form.html',
  styleUrl: './dynamic-form.scss',
})
export class DynamicForm implements OnInit, OnChanges {
  config = input.required<ObjectTypeConfig>();
  submitted = output<Record<string, unknown>>();
  loading = input<boolean>(false);

  form!: FormGroup;

  ngOnInit(): void {
    this.buildForm();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['config'] && !changes['config'].firstChange) {
      this.buildForm();
    }
  }

  private buildForm(): void {
    const controls: Record<string, FormControl> = {};
    for (const field of this.config().fields) {
      const validators: ValidatorFn[] = [];

      if (field.required) validators.push(Validators.required);
      if (field.minLength) validators.push(Validators.minLength(field.minLength));
      if (field.maxLength) validators.push(Validators.maxLength(field.maxLength));
      if (field.min !== undefined) validators.push(Validators.min(field.min));
      if (field.max !== undefined) validators.push(Validators.max(field.max));
      if (field.type === 'email') validators.push(Validators.email);
      if (field.pattern) validators.push(Validators.pattern(field.pattern));

      const defaultValue =
        field.default !== undefined
          ? field.default
          : field.type === 'boolean'
            ? false
            : null;

      controls[field.name] = new FormControl(defaultValue, validators);
    }
    this.form = new FormGroup(controls);
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.submitted.emit(this.form.value);
  }

  onReset(): void {
    this.form.reset();
    // Restore boolean defaults
    for (const field of this.config().fields) {
      if (field.type === 'boolean' && field.default !== undefined) {
        this.form.get(field.name)?.setValue(field.default);
      }
    }
  }

  isInvalid(field: FieldConfig): boolean {
    const ctrl = this.form.get(field.name);
    return !!(ctrl?.invalid && ctrl?.touched);
  }

  getError(fieldName: string, error: string): boolean {
    return !!this.form.get(fieldName)?.errors?.[error];
  }
}
