const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Sample dataset with various field types
const SAMPLE_DATA = [
  { id: 1, name: 'Alice Martin', email: 'alice.martin@example.com', age: 32, salary: 75000, score: 88.5, status: 'active', department: 'Engineering', description: 'Senior developer with 8 years of experience', isActive: true, isVerified: true, createdAt: '2022-03-15T10:00:00Z', updatedAt: '2024-01-20T14:30:00Z', birthDate: '1992-07-22T00:00:00Z' },
  { id: 2, name: 'Bob Johnson', email: 'bob.johnson@example.com', age: 45, salary: 95000, score: 92.1, status: 'active', department: 'Management', description: 'Project manager with strong leadership skills', isActive: true, isVerified: true, createdAt: '2020-11-01T09:00:00Z', updatedAt: '2024-02-10T11:00:00Z', birthDate: '1979-03-14T00:00:00Z' },
  { id: 3, name: 'Carol Smith', email: 'carol.smith@example.com', age: 28, salary: 62000, score: 79.3, status: 'inactive', department: 'Marketing', description: 'Marketing specialist focused on digital campaigns', isActive: false, isVerified: false, createdAt: '2023-01-10T08:00:00Z', updatedAt: '2023-12-05T16:00:00Z', birthDate: '1996-11-30T00:00:00Z' },
  { id: 4, name: 'David Lee', email: 'david.lee@example.com', age: 38, salary: 82000, score: 85.0, status: 'active', department: 'Engineering', description: 'Full stack developer specializing in cloud architecture', isActive: true, isVerified: true, createdAt: '2021-06-20T07:30:00Z', updatedAt: '2024-01-15T10:00:00Z', birthDate: '1986-04-05T00:00:00Z' },
  { id: 5, name: 'Emma Wilson', email: 'emma.wilson@example.com', age: 25, salary: 55000, score: 73.8, status: 'pending', department: 'HR', description: 'HR coordinator managing onboarding processes', isActive: true, isVerified: false, createdAt: '2023-08-01T09:00:00Z', updatedAt: '2024-02-01T12:00:00Z', birthDate: '1999-09-18T00:00:00Z' },
  { id: 6, name: 'Frank Brown', email: 'frank.brown@example.com', age: 52, salary: 110000, score: 96.4, status: 'active', department: 'Executive', description: 'CTO with 20+ years in technology leadership', isActive: true, isVerified: true, createdAt: '2018-02-14T08:00:00Z', updatedAt: '2024-02-18T09:00:00Z', birthDate: '1972-12-01T00:00:00Z' },
  { id: 7, name: 'Grace Davis', email: 'grace.davis@example.com', age: 31, salary: 71000, score: 82.7, status: 'active', department: 'Design', description: 'UX designer passionate about user-centered design', isActive: true, isVerified: true, createdAt: '2022-07-01T10:00:00Z', updatedAt: '2024-01-25T15:00:00Z', birthDate: '1993-06-08T00:00:00Z' },
  { id: 8, name: 'Henry Taylor', email: 'henry.taylor@example.com', age: 41, salary: 88000, score: 90.2, status: 'active', department: 'Engineering', description: 'DevOps engineer with expertise in Kubernetes and CI/CD', isActive: true, isVerified: true, createdAt: '2020-04-15T09:00:00Z', updatedAt: '2024-02-05T13:00:00Z', birthDate: '1983-02-28T00:00:00Z' },
  { id: 9, name: 'Iris Martinez', email: 'iris.martinez@example.com', age: 29, salary: 67000, score: 77.5, status: 'inactive', department: 'Sales', description: 'Sales representative with excellent communication skills', isActive: false, isVerified: true, createdAt: '2022-09-01T08:00:00Z', updatedAt: '2023-11-10T14:00:00Z', birthDate: '1995-01-17T00:00:00Z' },
  { id: 10, name: 'Jack Anderson', email: 'jack.anderson@example.com', age: 35, salary: 78000, score: 84.1, status: 'active', department: 'Engineering', description: 'Backend engineer specializing in microservices', isActive: true, isVerified: false, createdAt: '2021-11-20T07:00:00Z', updatedAt: '2024-02-12T11:00:00Z', birthDate: '1989-08-23T00:00:00Z' },
  { id: 11, name: 'Karen White', email: 'karen.white@example.com', age: 47, salary: 102000, score: 93.8, status: 'active', department: 'Finance', description: 'CFO overseeing all financial operations', isActive: true, isVerified: true, createdAt: '2017-05-10T09:00:00Z', updatedAt: '2024-01-30T10:00:00Z', birthDate: '1977-10-11T00:00:00Z' },
  { id: 12, name: 'Liam Harris', email: 'liam.harris@example.com', age: 23, salary: 48000, score: 68.9, status: 'pending', department: 'Support', description: 'Customer support specialist helping users resolve issues', isActive: true, isVerified: false, createdAt: '2024-01-05T10:00:00Z', updatedAt: '2024-02-15T09:00:00Z', birthDate: '2001-05-04T00:00:00Z' },
  { id: 13, name: 'Mia Thompson', email: 'mia.thompson@example.com', age: 34, salary: 76000, score: 87.3, status: 'active', department: 'Marketing', description: 'Content strategist creating compelling brand narratives', isActive: true, isVerified: true, createdAt: '2021-03-22T08:00:00Z', updatedAt: '2024-02-08T12:00:00Z', birthDate: '1990-12-16T00:00:00Z' },
  { id: 14, name: 'Noah Garcia', email: 'noah.garcia@example.com', age: 27, salary: 59000, score: 74.6, status: 'active', department: 'Design', description: 'Graphic designer with a focus on brand identity', isActive: false, isVerified: true, createdAt: '2023-04-01T09:00:00Z', updatedAt: '2024-01-10T16:00:00Z', birthDate: '1997-07-25T00:00:00Z' },
  { id: 15, name: 'Olivia Jackson', email: 'olivia.jackson@example.com', age: 39, salary: 91000, score: 89.7, status: 'active', department: 'Engineering', description: 'Machine learning engineer working on AI products', isActive: true, isVerified: true, createdAt: '2020-08-10T07:30:00Z', updatedAt: '2024-02-20T10:00:00Z', birthDate: '1985-03-03T00:00:00Z' },
  { id: 16, name: 'Paul Robinson', email: 'paul.robinson@example.com', age: 43, salary: 84000, score: 86.2, status: 'inactive', department: 'Sales', description: 'Regional sales manager driving revenue growth', isActive: false, isVerified: false, createdAt: '2019-10-15T08:00:00Z', updatedAt: '2023-09-01T14:00:00Z', birthDate: '1981-09-07T00:00:00Z' },
  { id: 17, name: 'Quinn Lewis', email: 'quinn.lewis@example.com', age: 30, salary: 69000, score: 80.4, status: 'active', department: 'HR', description: 'Talent acquisition specialist finding top candidates', isActive: true, isVerified: true, createdAt: '2022-05-01T09:00:00Z', updatedAt: '2024-02-14T11:00:00Z', birthDate: '1994-02-20T00:00:00Z' },
  { id: 18, name: 'Rachel Walker', email: 'rachel.walker@example.com', age: 26, salary: 53000, score: 71.9, status: 'pending', department: 'Support', description: 'Technical support analyst with strong problem-solving skills', isActive: true, isVerified: false, createdAt: '2023-10-01T10:00:00Z', updatedAt: '2024-02-19T13:00:00Z', birthDate: '1998-06-12T00:00:00Z' },
  { id: 19, name: 'Samuel Hall', email: 'samuel.hall@example.com', age: 50, salary: 107000, score: 95.1, status: 'active', department: 'Executive', description: 'VP of Engineering driving technical strategy', isActive: true, isVerified: true, createdAt: '2016-03-01T08:00:00Z', updatedAt: '2024-02-21T09:00:00Z', birthDate: '1974-11-29T00:00:00Z' },
  { id: 20, name: 'Tina Young', email: 'tina.young@example.com', age: 33, salary: 73000, score: 83.6, status: 'active', department: 'Finance', description: 'Financial analyst providing data-driven insights', isActive: true, isVerified: true, createdAt: '2021-09-01T09:00:00Z', updatedAt: '2024-01-28T15:00:00Z', birthDate: '1991-04-14T00:00:00Z' },
  { id: 21, name: 'Uma Scott', email: 'uma.scott@example.com', age: 37, salary: 80000, score: 84.9, status: 'active', department: 'Engineering', description: 'Security engineer ensuring platform safety', isActive: true, isVerified: true, createdAt: '2021-01-15T08:00:00Z', updatedAt: '2024-02-10T10:00:00Z', birthDate: '1987-08-30T00:00:00Z' },
  { id: 22, name: 'Victor Adams', email: 'victor.adams@example.com', age: 44, salary: 97000, score: 91.5, status: 'active', department: 'Management', description: 'Product manager with deep customer empathy', isActive: true, isVerified: true, createdAt: '2019-06-01T07:00:00Z', updatedAt: '2024-02-17T12:00:00Z', birthDate: '1980-01-06T00:00:00Z' },
  { id: 23, name: 'Wendy Nelson', email: 'wendy.nelson@example.com', age: 29, salary: 64000, score: 78.3, status: 'inactive', department: 'Marketing', description: 'Social media manager building online communities', isActive: false, isVerified: true, createdAt: '2022-11-01T09:00:00Z', updatedAt: '2023-10-15T16:00:00Z', birthDate: '1995-10-03T00:00:00Z' },
  { id: 24, name: 'Xavier Carter', email: 'xavier.carter@example.com', age: 36, salary: 79000, score: 85.7, status: 'active', department: 'Engineering', description: 'Mobile developer for iOS and Android platforms', isActive: true, isVerified: false, createdAt: '2021-04-01T08:00:00Z', updatedAt: '2024-02-13T11:00:00Z', birthDate: '1988-05-19T00:00:00Z' },
  { id: 25, name: 'Yara Mitchell', email: 'yara.mitchell@example.com', age: 31, salary: 68000, score: 81.2, status: 'active', department: 'Design', description: 'Product designer bridging user needs and business goals', isActive: true, isVerified: true, createdAt: '2022-02-14T10:00:00Z', updatedAt: '2024-02-11T14:00:00Z', birthDate: '1993-12-27T00:00:00Z' },
  { id: 26, name: 'Zach Perez', email: 'zach.perez@example.com', age: 24, salary: 51000, score: 70.5, status: 'pending', department: 'Sales', description: 'Junior sales associate eager to grow in the role', isActive: true, isVerified: false, createdAt: '2023-11-01T09:00:00Z', updatedAt: '2024-02-16T10:00:00Z', birthDate: '2000-03-08T00:00:00Z' },
  { id: 27, name: 'Anna Roberts', email: 'anna.roberts@example.com', age: 40, salary: 89000, score: 88.9, status: 'active', department: 'Engineering', description: 'Data engineer building scalable data pipelines', isActive: true, isVerified: true, createdAt: '2020-02-28T08:00:00Z', updatedAt: '2024-02-09T13:00:00Z', birthDate: '1984-07-11T00:00:00Z' },
  { id: 28, name: 'Brian Turner', email: 'brian.turner@example.com', age: 46, salary: 99000, score: 92.8, status: 'active', department: 'Finance', description: 'Risk manager with extensive regulatory compliance knowledge', isActive: true, isVerified: true, createdAt: '2018-08-20T07:00:00Z', updatedAt: '2024-01-22T10:00:00Z', birthDate: '1978-02-14T00:00:00Z' },
  { id: 29, name: 'Chloe Phillips', email: 'chloe.phillips@example.com', age: 27, salary: 57000, score: 75.4, status: 'active', department: 'Marketing', description: 'SEO specialist optimizing digital content for search', isActive: true, isVerified: true, createdAt: '2023-02-01T09:00:00Z', updatedAt: '2024-02-07T15:00:00Z', birthDate: '1997-04-22T00:00:00Z' },
  { id: 30, name: 'Derek Campbell', email: 'derek.campbell@example.com', age: 48, salary: 105000, score: 94.3, status: 'active', department: 'Executive', description: 'COO managing all operational aspects of the business', isActive: true, isVerified: true, createdAt: '2015-10-01T08:00:00Z', updatedAt: '2024-02-21T08:00:00Z', birthDate: '1976-06-17T00:00:00Z' },
];

// Field type definitions for documentation
const FIELD_DEFINITIONS = [
  { field: 'id', label: 'ID', type: 'number' },
  { field: 'name', label: 'Name', type: 'string' },
  { field: 'email', label: 'Email', type: 'string' },
  { field: 'age', label: 'Age', type: 'number' },
  { field: 'salary', label: 'Salary', type: 'number' },
  { field: 'score', label: 'Score', type: 'number' },
  { field: 'status', label: 'Status', type: 'string' },
  { field: 'department', label: 'Department', type: 'string' },
  { field: 'description', label: 'Description', type: 'string' },
  { field: 'isActive', label: 'Active', type: 'boolean' },
  { field: 'isVerified', label: 'Verified', type: 'boolean' },
  { field: 'createdAt', label: 'Created At', type: 'date' },
  { field: 'updatedAt', label: 'Updated At', type: 'date' },
  { field: 'birthDate', label: 'Birth Date', type: 'date' },
];

function applyFilter(item, filter) {
  const { field, operator, value } = filter;
  const fieldValue = item[field];

  if (fieldValue === undefined || fieldValue === null) return false;

  const fieldDef = FIELD_DEFINITIONS.find(f => f.field === field);
  if (!fieldDef) return false;

  switch (fieldDef.type) {
    case 'string': {
      const strValue = String(fieldValue).toLowerCase();
      const filterVal = String(value).toLowerCase();
      switch (operator) {
        case 'contains': return strValue.includes(filterVal);
        case 'not_contains': return !strValue.includes(filterVal);
        case 'equals': return strValue === filterVal;
        case 'not_equals': return strValue !== filterVal;
        case 'starts_with': return strValue.startsWith(filterVal);
        case 'ends_with': return strValue.endsWith(filterVal);
        case 'is_empty': return strValue.trim() === '';
        case 'is_not_empty': return strValue.trim() !== '';
        default: return true;
      }
    }
    case 'number': {
      const numValue = parseFloat(fieldValue);
      const filterNum = parseFloat(value);
      switch (operator) {
        case 'equals': return numValue === filterNum;
        case 'not_equals': return numValue !== filterNum;
        case 'greater_than': return numValue > filterNum;
        case 'greater_than_or_equal': return numValue >= filterNum;
        case 'less_than': return numValue < filterNum;
        case 'less_than_or_equal': return numValue <= filterNum;
        case 'between': {
          const [min, max] = (value || '').toString().split(',').map(v => parseFloat(v.trim()));
          return numValue >= min && numValue <= max;
        }
        default: return true;
      }
    }
    case 'date': {
      const dateValue = new Date(fieldValue).getTime();
      const filterDate = new Date(value).getTime();
      switch (operator) {
        case 'before': return dateValue < filterDate;
        case 'after': return dateValue > filterDate;
        case 'equals': return new Date(fieldValue).toDateString() === new Date(value).toDateString();
        case 'not_equals': return new Date(fieldValue).toDateString() !== new Date(value).toDateString();
        case 'before_or_equals': return dateValue <= filterDate;
        case 'after_or_equals': return dateValue >= filterDate;
        case 'between': {
          const [startStr, endStr] = (value || '').toString().split(',');
          const start = new Date(startStr.trim()).getTime();
          const end = new Date(endStr.trim()).getTime();
          return dateValue >= start && dateValue <= end;
        }
        default: return true;
      }
    }
    case 'boolean': {
      const boolValue = Boolean(fieldValue);
      const filterBool = value === true || value === 'true';
      switch (operator) {
        case 'equals': return boolValue === filterBool;
        case 'not_equals': return boolValue !== filterBool;
        default: return true;
      }
    }
    default:
      return true;
  }
}

function applyTextSearch(item, text) {
  if (!text || text.trim() === '') return true;
  const searchText = text.toLowerCase();
  return Object.values(item).some(val =>
    String(val).toLowerCase().includes(searchText)
  );
}

// GET /api/fields - Returns field definitions
app.get('/api/fields', (req, res) => {
  res.json(FIELD_DEFINITIONS);
});

// POST /api/search - Search with filters
app.post('/api/search', (req, res) => {
  const {
    text = '',
    filters = [],
    combinator = 'and',
    page = 1,
    pageSize = 10,
    sortField = 'id',
    sortOrder = 'asc'
  } = req.body;

  let results = [...SAMPLE_DATA];

  // Apply text search
  results = results.filter(item => applyTextSearch(item, text));

  // Apply filters
  if (filters && filters.length > 0) {
    results = results.filter(item => {
      if (combinator === 'and') {
        return filters.every(filter => applyFilter(item, filter));
      } else {
        return filters.some(filter => applyFilter(item, filter));
      }
    });
  }

  // Sort
  results.sort((a, b) => {
    const aVal = a[sortField];
    const bVal = b[sortField];
    let comparison = 0;
    if (typeof aVal === 'string' && typeof bVal === 'string') {
      comparison = aVal.localeCompare(bVal);
    } else {
      comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
    }
    return sortOrder === 'asc' ? comparison : -comparison;
  });

  const total = results.length;
  const start = (page - 1) * pageSize;
  const paginatedResults = results.slice(start, start + pageSize);

  // Simulate network delay
  setTimeout(() => {
    res.json({
      data: paginatedResults,
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize)
    });
  }, 300);
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Mock server running on http://localhost:${PORT}`);
  console.log(`  GET  /api/fields  - Get available search fields`);
  console.log(`  POST /api/search  - Search with filters`);
});
