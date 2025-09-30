# FieldOps – Field Service Coordination Platform (Phase 1)

## Overview
FieldOps is a backend platform to manage, assign, and track service tasks between users, field workers, and admins.  
It includes JWT authentication, role-based access control, and APIs for service request management.

---

## Features Implemented

### User Management
- Users can register and edit their profile
- Admin approval required for workers
- Role-based access: `USER / WORKER / ADMIN`

### JWT Authentication
- Secure access to all endpoints

### Service Requests
- Users can create service requests
- Admin can assign requests to workers
- Workers can start tasks

### Dashboard
- View total, pending, and completed requests

### Task History
- Tracks status changes for tasks

### Task Proof Upload
- Endpoint exists (`/api/task-proof/`), file upload pending testing

---

## API Endpoints

### Authentication
**Obtain Token**  
`POST /api/token/`  

Body:
```json
{
  "username": "<your_username>",
  "password": "<your_password>"
}

Refresh Token
POST /api/token/refresh/

Body:

{
  "refresh": "<refresh_token>"
}

Users

List / Retrieve Users
GET /api/users/

Service Requests

List / Create
GET/POST /api/service-requests/

Retrieve / Update / Delete
GET/PUT/DELETE /api/service-requests/<id>/

Assign Request (Admin only)
POST /api/service-requests/<id>/assign/

Start Task (Worker only)
POST /api/service-requests/<id>/start/

Task History

List / Create
GET/POST /api/task-history/

Task Proof

Upload proof (Pending file upload testing)
POST /api/task-proof/

Dashboard

Summary
GET /api/dashboard/

Setup Instructions
# Clone the repository
git clone https://github.com/Vimal-Babu/FieldOps-Back-end.git
cd FieldOps-Back-end

# Create a virtual environment and activate
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser (Admin)
python manage.py createsuperuser

# Run the server
python manage.py runserver


Use Postman to test APIs with JWT authentication.

---

## Workflow Diagram

```mermaid
flowchart TD
    User[User] -->|Create Service Request| Admin[Admin]
    Admin -->|Assign Task| Worker[Worker]
    Worker -->|Start Task| Worker[Worker]
    Worker -->|Upload Proof| Admin
    Admin -->|Verify Completion| Dashboard[Dashboard Summary]

    Dashboard -->|View Stats| User

Explanation:

User reports an issue by creating a service request.

Admin assigns the request to a worker.

Worker starts the task and optionally uploads proof of completion.

Admin verifies the completion.

Dashboard provides stats to Admin and optionally Users.