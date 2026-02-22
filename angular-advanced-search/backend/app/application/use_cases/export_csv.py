"""
Application Layer — Export CSV Use Case

Fetches all employees matching a query (no pagination) and serialises them
to RFC 4180 CSV format. CSV generation is an application-level concern
because it combines domain data with a presentation format — it doesn't
belong in the domain (which has no I/O concept) or in the exposition layer
(which should only translate HTTP, not format data).
"""

import csv
import io

from app.domain.ports.employee_repository import EmployeeRepository
from app.domain.value_objects import SearchQuery


class ExportCsvUseCase:
    def __init__(self, repository: EmployeeRepository) -> None:
        self._repository = repository

    def execute(self, query: SearchQuery) -> str:
        """Return a UTF-8 CSV string of all employees matching the query."""
        employees = self._repository.get_all_matching(query)
        if not employees:
            return ""

        output = io.StringIO()
        fieldnames = list(employees[0].to_dict().keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for employee in employees:
            writer.writerow(employee.to_dict())
        return output.getvalue()
