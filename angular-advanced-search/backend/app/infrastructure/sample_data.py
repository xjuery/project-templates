"""
Infrastructure Layer — Sample Data

30 employee records used by the in-memory repository.
Adding a new record: append an Employee instance to EMPLOYEES.
Adding a new field: add the attribute to Employee (domain), update to_dict(),
and add a FieldDefinition below.
"""

from app.domain.entities import Employee, FieldDefinition

FIELD_DEFINITIONS: list[FieldDefinition] = [
    FieldDefinition(field="id", label="ID", type="number"),
    FieldDefinition(field="name", label="Name", type="string"),
    FieldDefinition(field="email", label="Email", type="string"),
    FieldDefinition(field="age", label="Age", type="number"),
    FieldDefinition(field="salary", label="Salary", type="number"),
    FieldDefinition(field="score", label="Score", type="number"),
    FieldDefinition(field="status", label="Status", type="string"),
    FieldDefinition(field="department", label="Department", type="string"),
    FieldDefinition(field="description", label="Description", type="string"),
    FieldDefinition(field="isActive", label="Active", type="boolean"),
    FieldDefinition(field="isVerified", label="Verified", type="boolean"),
    FieldDefinition(field="createdAt", label="Created At", type="date"),
    FieldDefinition(field="updatedAt", label="Updated At", type="date"),
    FieldDefinition(field="birthDate", label="Birth Date", type="date"),
]

EMPLOYEES: list[Employee] = [
    Employee(1, "Alice Martin", "alice.martin@example.com", 32, 75000, 88.5, "active", "Engineering", "Senior developer with 8 years of experience", True, True, "2022-03-15T10:00:00Z", "2024-01-20T14:30:00Z", "1992-07-22T00:00:00Z"),
    Employee(2, "Bob Johnson", "bob.johnson@example.com", 45, 95000, 92.1, "active", "Management", "Project manager with strong leadership skills", True, True, "2020-11-01T09:00:00Z", "2024-02-10T11:00:00Z", "1979-03-14T00:00:00Z"),
    Employee(3, "Carol Smith", "carol.smith@example.com", 28, 62000, 79.3, "inactive", "Marketing", "Marketing specialist focused on digital campaigns", False, False, "2023-01-10T08:00:00Z", "2023-12-05T16:00:00Z", "1996-11-30T00:00:00Z"),
    Employee(4, "David Lee", "david.lee@example.com", 38, 82000, 85.0, "active", "Engineering", "Full stack developer specializing in cloud architecture", True, True, "2021-06-20T07:30:00Z", "2024-01-15T10:00:00Z", "1986-04-05T00:00:00Z"),
    Employee(5, "Emma Wilson", "emma.wilson@example.com", 25, 55000, 73.8, "pending", "HR", "HR coordinator managing onboarding processes", True, False, "2023-08-01T09:00:00Z", "2024-02-01T12:00:00Z", "1999-09-18T00:00:00Z"),
    Employee(6, "Frank Brown", "frank.brown@example.com", 52, 110000, 96.4, "active", "Executive", "CTO with 20+ years in technology leadership", True, True, "2018-02-14T08:00:00Z", "2024-02-18T09:00:00Z", "1972-12-01T00:00:00Z"),
    Employee(7, "Grace Davis", "grace.davis@example.com", 31, 71000, 82.7, "active", "Design", "UX designer passionate about user-centered design", True, True, "2022-07-01T10:00:00Z", "2024-01-25T15:00:00Z", "1993-06-08T00:00:00Z"),
    Employee(8, "Henry Taylor", "henry.taylor@example.com", 41, 88000, 90.2, "active", "Engineering", "DevOps engineer with expertise in Kubernetes and CI/CD", True, True, "2020-04-15T09:00:00Z", "2024-02-05T13:00:00Z", "1983-02-28T00:00:00Z"),
    Employee(9, "Iris Martinez", "iris.martinez@example.com", 29, 67000, 77.5, "inactive", "Sales", "Sales representative with excellent communication skills", False, True, "2022-09-01T08:00:00Z", "2023-11-10T14:00:00Z", "1995-01-17T00:00:00Z"),
    Employee(10, "Jack Anderson", "jack.anderson@example.com", 35, 78000, 84.1, "active", "Engineering", "Backend engineer specializing in microservices", True, False, "2021-11-20T07:00:00Z", "2024-02-12T11:00:00Z", "1989-08-23T00:00:00Z"),
    Employee(11, "Karen White", "karen.white@example.com", 47, 102000, 93.8, "active", "Finance", "CFO overseeing all financial operations", True, True, "2017-05-10T09:00:00Z", "2024-01-30T10:00:00Z", "1977-10-11T00:00:00Z"),
    Employee(12, "Liam Harris", "liam.harris@example.com", 23, 48000, 68.9, "pending", "Support", "Customer support specialist helping users resolve issues", True, False, "2024-01-05T10:00:00Z", "2024-02-15T09:00:00Z", "2001-05-04T00:00:00Z"),
    Employee(13, "Mia Thompson", "mia.thompson@example.com", 34, 76000, 87.3, "active", "Marketing", "Content strategist creating compelling brand narratives", True, True, "2021-03-22T08:00:00Z", "2024-02-08T12:00:00Z", "1990-12-16T00:00:00Z"),
    Employee(14, "Noah Garcia", "noah.garcia@example.com", 27, 59000, 74.6, "active", "Design", "Graphic designer with a focus on brand identity", False, True, "2023-04-01T09:00:00Z", "2024-01-10T16:00:00Z", "1997-07-25T00:00:00Z"),
    Employee(15, "Olivia Jackson", "olivia.jackson@example.com", 39, 91000, 89.7, "active", "Engineering", "Machine learning engineer working on AI products", True, True, "2020-08-10T07:30:00Z", "2024-02-20T10:00:00Z", "1985-03-03T00:00:00Z"),
    Employee(16, "Paul Robinson", "paul.robinson@example.com", 43, 84000, 86.2, "inactive", "Sales", "Regional sales manager driving revenue growth", False, False, "2019-10-15T08:00:00Z", "2023-09-01T14:00:00Z", "1981-09-07T00:00:00Z"),
    Employee(17, "Quinn Lewis", "quinn.lewis@example.com", 30, 69000, 80.4, "active", "HR", "Talent acquisition specialist finding top candidates", True, True, "2022-05-01T09:00:00Z", "2024-02-14T11:00:00Z", "1994-02-20T00:00:00Z"),
    Employee(18, "Rachel Walker", "rachel.walker@example.com", 26, 53000, 71.9, "pending", "Support", "Technical support analyst with strong problem-solving skills", True, False, "2023-10-01T10:00:00Z", "2024-02-19T13:00:00Z", "1998-06-12T00:00:00Z"),
    Employee(19, "Samuel Hall", "samuel.hall@example.com", 50, 107000, 95.1, "active", "Executive", "VP of Engineering driving technical strategy", True, True, "2016-03-01T08:00:00Z", "2024-02-21T09:00:00Z", "1974-11-29T00:00:00Z"),
    Employee(20, "Tina Young", "tina.young@example.com", 33, 73000, 83.6, "active", "Finance", "Financial analyst providing data-driven insights", True, True, "2021-09-01T09:00:00Z", "2024-01-28T15:00:00Z", "1991-04-14T00:00:00Z"),
    Employee(21, "Uma Scott", "uma.scott@example.com", 37, 80000, 84.9, "active", "Engineering", "Security engineer ensuring platform safety", True, True, "2021-01-15T08:00:00Z", "2024-02-10T10:00:00Z", "1987-08-30T00:00:00Z"),
    Employee(22, "Victor Adams", "victor.adams@example.com", 44, 97000, 91.5, "active", "Management", "Product manager with deep customer empathy", True, True, "2019-06-01T07:00:00Z", "2024-02-17T12:00:00Z", "1980-01-06T00:00:00Z"),
    Employee(23, "Wendy Nelson", "wendy.nelson@example.com", 29, 64000, 78.3, "inactive", "Marketing", "Social media manager building online communities", False, True, "2022-11-01T09:00:00Z", "2023-10-15T16:00:00Z", "1995-10-03T00:00:00Z"),
    Employee(24, "Xavier Carter", "xavier.carter@example.com", 36, 79000, 85.7, "active", "Engineering", "Mobile developer for iOS and Android platforms", True, False, "2021-04-01T08:00:00Z", "2024-02-13T11:00:00Z", "1988-05-19T00:00:00Z"),
    Employee(25, "Yara Mitchell", "yara.mitchell@example.com", 31, 68000, 81.2, "active", "Design", "Product designer bridging user needs and business goals", True, True, "2022-02-14T10:00:00Z", "2024-02-11T14:00:00Z", "1993-12-27T00:00:00Z"),
    Employee(26, "Zach Perez", "zach.perez@example.com", 24, 51000, 70.5, "pending", "Sales", "Junior sales associate eager to grow in the role", True, False, "2023-11-01T09:00:00Z", "2024-02-16T10:00:00Z", "2000-03-08T00:00:00Z"),
    Employee(27, "Anna Roberts", "anna.roberts@example.com", 40, 89000, 88.9, "active", "Engineering", "Data engineer building scalable data pipelines", True, True, "2020-02-28T08:00:00Z", "2024-02-09T13:00:00Z", "1984-07-11T00:00:00Z"),
    Employee(28, "Brian Turner", "brian.turner@example.com", 46, 99000, 92.8, "active", "Finance", "Risk manager with extensive regulatory compliance knowledge", True, True, "2018-08-20T07:00:00Z", "2024-01-22T10:00:00Z", "1978-02-14T00:00:00Z"),
    Employee(29, "Chloe Phillips", "chloe.phillips@example.com", 27, 57000, 75.4, "active", "Marketing", "SEO specialist optimizing digital content for search", True, True, "2023-02-01T09:00:00Z", "2024-02-07T15:00:00Z", "1997-04-22T00:00:00Z"),
    Employee(30, "Derek Campbell", "derek.campbell@example.com", 48, 105000, 94.3, "active", "Executive", "COO managing all operational aspects of the business", True, True, "2015-10-01T08:00:00Z", "2024-02-21T08:00:00Z", "1976-06-17T00:00:00Z"),
]
