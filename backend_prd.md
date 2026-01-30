1. Introduction

The HRMS Lite backend is a web-based server application designed to support essential human resource management operations for a small organization. The system focuses on two core functions: employee management and attendance tracking. The backend will be developed using the Django framework along with Django REST Framework to expose RESTful APIs consumable by a modern frontend. The objective is to build a realistically usable internal HR tool rather than a superficial demo. The backend must prioritize data integrity, clarity of API behavior, meaningful error handling, and clean architecture. Authentication, payroll, leave management, and complex reporting are explicitly out of scope. The system assumes a single trusted admin user accessing the APIs via a frontend interface.

2. Goals and Objectives

The primary goal of the backend is to provide a stable, predictable, and well-structured API layer for HRMS Lite. It should allow an admin to manage employee records, mark daily attendance, and retrieve attendance history efficiently. The backend must enforce server-side validation to prevent invalid or inconsistent data from being persisted. It should use proper HTTP status codes, return clear error messages, and remain simple enough to be extended in the future. Performance requirements are modest, but the system should be written in a scalable manner that would support growth if needed.

3. Scope Definition

The backend scope includes employee creation, listing, and deletion, along with attendance marking and retrieval. Each employee is uniquely identified by an employee ID. Attendance is recorded per employee per date with a status of present or absent. The system does not handle user authentication, roles, permissions, payroll calculations, leave balances, holiday calendars, or reporting dashboards. File uploads, document storage, and bulk imports are excluded. The backend will serve as a single-tenant internal API designed for controlled usage.

4. Assumptions and Constraints

The system assumes that only one admin user exists and that all API requests are trusted. No authentication or authorization layers will be implemented. The backend must still validate inputs rigorously to avoid data corruption. The database may initially be SQLite for development but must remain compatible with PostgreSQL for production usage. All dates are assumed to be in ISO format. The backend must remain framework-pure without reliance on unnecessary third-party services. The codebase should follow Django best practices and remain readable for other developers.

5. Technical Stack

The backend will be built using Python and Django. Django REST Framework will be used to implement RESTful APIs. The database layer will use Django ORM with a relational database. Serializers will handle data validation and transformation. Views will be class-based wherever possible to maintain clarity and extensibility. The backend will be structured using multiple Django apps to separate concerns logically. Environment configuration will follow standard Django settings conventions.

6. Data Models

The Employee model represents a single employee in the organization. Fields include an auto-generated primary key, a unique employee ID provided by the admin, full name, email address, department, and timestamps for creation and updates. The email field must be unique and validated for proper format. The employee ID must be unique and immutable once created. The Attendance model represents a single attendance entry. It includes a foreign key to the employee, a date field, a status field constrained to present or absent, and timestamps. A unique constraint must exist on the combination of employee and date to prevent duplicate attendance records.

7. Employee Management Requirements

The backend must provide an API endpoint to create a new employee. Required fields include employee ID, full name, email address, and department. The system must validate that all required fields are present and non-empty. The email must follow a valid email format. Duplicate employee IDs or emails must be rejected with a clear error message. Upon successful creation, the API must return the created employee object with a 201 status code. Another endpoint must list all employees in the system. The list response should be ordered by creation date by default. A delete endpoint must allow the admin to remove an employee permanently. Deleting an employee must also remove associated attendance records to maintain referential integrity.

8. Attendance Management Requirements

The backend must allow the admin to mark attendance for an employee for a specific date. Required fields include employee identifier, date, and status. The system must validate that the employee exists before creating attendance. The date must be valid and not null. The status must be either present or absent. Duplicate attendance entries for the same employee and date must be rejected. On successful creation, the API must return the attendance record with a 201 status code. Another endpoint must allow retrieval of attendance records for a specific employee. The response should include date, status, and basic employee information.

9. API Design Principles

All APIs must follow RESTful conventions. Resource-based URLs should be used consistently. HTTP methods must align with their semantic meaning. POST is used for creation, GET for retrieval, and DELETE for deletion. Responses must be JSON formatted. Error responses must include a clear message and, when applicable, field-level validation errors. The API must not expose internal implementation details. Pagination is optional but recommended for employee listing to support future scaling.

10. Validation and Error Handling

Server-side validation is mandatory for all write operations. Missing required fields must result in a 400 Bad Request response. Invalid email formats must be rejected explicitly. Duplicate employee IDs or emails must return a 409 Conflict or 400 error with a descriptive message. Attempting to mark attendance for a non-existent employee must return a 404 Not Found response. Attempting to create duplicate attendance must return a clear validation error. All unexpected server errors must return a 500 Internal Server Error with a generic message.

11. HTTP Status Codes

The backend must consistently use appropriate HTTP status codes. Successful creation operations must return 201 Created. Successful retrieval operations must return 200 OK. Successful deletion must return 204 No Content. Client-side validation errors must return 400 Bad Request. Resource-not-found scenarios must return 404 Not Found. Duplicate resource conflicts may return 409 Conflict. Server errors must return 500 Internal Server Error. Status code usage must remain consistent across all endpoints.

12. Response Structure

Successful responses must return structured JSON objects. Employee objects must include id, employee_id, full_name, email, department, and created_at. Attendance objects must include id, employee, date, and status. Error responses must include a top-level message and optional field-specific errors. The frontend must be able to rely on predictable response formats to display meaningful UI states such as loading, empty results, and errors.

13. Code Structure and Modularity

The backend codebase must be modular and readable. Separate Django apps should be created for employees and attendance. Models, serializers, views, and URLs must be organized logically. Business logic should not be embedded directly in views when it can be abstracted cleanly. Naming conventions must be consistent and descriptive. Comments should explain intent rather than restating obvious code behavior. The project should be structured to allow easy extension without refactoring core components.

14. Database Considerations

The database schema must enforce constraints at the database level where possible. Unique constraints must be defined explicitly. Foreign key relationships must use cascading deletes to maintain integrity. Indexing should be applied to frequently queried fields such as employee ID and attendance date. Migrations must be clean and reproducible. The backend should avoid raw SQL and rely on Django ORM for maintainability.

15. Security Considerations

Although authentication is out of scope, the backend must not expose sensitive internal information. Error messages should not leak stack traces or database details. Debug mode must be disabled in production environments. Input data must be sanitized through serializers. CORS configuration must allow only intended frontend origins. The system must follow general secure coding practices despite its simplified scope.

16. Testing Strategy

The backend must be manually testable using tools such as Postman or Thunder Client. Each endpoint must be tested for success paths and failure scenarios. Validation errors must be verified explicitly. Edge cases such as duplicate creation, missing fields, and invalid dates must be tested. While automated tests are not mandatory, the code should be written in a test-friendly manner to allow future test coverage.

17. Deployment Readiness

The backend must be deployment-ready with minimal configuration changes. Environment variables should be used for sensitive settings. The project must run reliably on a standard WSGI server. Database migrations must be applied cleanly. The system should be compatible with containerization if needed. Logging should be minimal but sufficient to diagnose issues in production.

18. Future Extensibility

The backend should be designed with future enhancements in mind. Adding authentication, roles, or additional HR features should not require rewriting core logic. The API structure should allow versioning if breaking changes are introduced later. The data models should be flexible enough to support extensions such as attendance remarks or employee status without schema redesign.

19. Non-Functional Requirements

The backend must be stable, predictable, and easy to understand. Response times should be acceptable for small to medium datasets. The system should handle invalid requests gracefully without crashing. Code readability and maintainability are considered first-class requirements. The backend must support a professional frontend experience through consistent behavior and reliable data delivery.

20. Conclusion

The HRMS Lite backend is a focused Django-based system designed to simulate a real internal HR tool. By limiting scope and emphasizing correctness, validation, and clean design, the backend provides a strong foundation for a professional frontend application. The system balances simplicity with realism, ensuring it is usable in practice and valuable as a portfolio-grade project.