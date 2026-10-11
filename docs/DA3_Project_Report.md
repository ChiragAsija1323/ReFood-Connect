# ReFood Connect — Smart Food Waste Redistribution Platform
## Digital Assignment 3 (DA-3 / Review 3) Comprehensive Project Report
**Course:** Software Engineering (`BCSE301L`)  
**Academic Institution:** Vellore Institute of Technology (VIT), Chennai Campus  
**Department:** School of Computer Science and Engineering (SCOPE)  
**Academic Year:** 2025–2026  

**Student Team & Authors:**
* **Chirag Asija** (Registration No: `24BDS1073`) — [@ChiragAsija1323](https://github.com/ChiragAsija1323)
* **Saanvi Gupta** (Registration No: `24BDS1023`)

**Official GitHub Repository:** [https://github.com/ChiragAsija1323/ReFood-Connect](https://github.com/ChiragAsija1323/ReFood-Connect)

---

## 1. Problem Statement & System Objectives

### 1.1 The Domain Problem
Every day, commercial food establishments—including restaurants, hotels, banquet halls, marriage lawns, and university messes—generate large quantities of edible surplus food that ends up discarded in landfills. Concurrently, orphanages, homeless shelters, old-age homes, and economically vulnerable populations suffer from food insecurity.

Traditional redistribution methods rely on informal, fragmented channels (e.g., ad-hoc phone calls or WhatsApp groups). This leads to:
1. **Critical Perishability Failures:** Cooked meals spoil within a 4–6 hour window without organized pickup.
2. **Severe Coordination Friction:** Donors lack transport capabilities, while NGOs lack real-time visibility into available food batches.
3. **Lack of Traceability & Trust:** Absence of authentication and audit trails exposes charities to liability and prevents administrative oversight.

### 1.2 System Objectives
* **Connect Stakeholders via Real-Time Platform:** Unify Food Donors, verified NGOs, civic Volunteers, and Administrators in a single web portal.
* **Streamline the Redistribution Lifecycle:** Automate status transitions from donation creation (`Available`) to NGO request (`Requested`), volunteer pickup (`Accepted` → `Picked Up`), and final handover (`Delivered`).
* **Ensure Operational Integrity:** Implement strict Role-Based Access Control (RBAC), data isolation, and cryptographic security.
* **Provide Governance & Auditing:** Equip system administrators with dynamic metrics, active donation tracking, and user directories.

---

## 2. User Stories & Acceptance Criteria

The system specifies 18 distinct user stories across five defined personas:

```
+---------+-----------------+--------------------------------------------------------------+---------------+
| Story ID| Persona         | User Story Description                                       | MoSCoW Status |
+---------+-----------------+--------------------------------------------------------------+---------------+
| US-01   | Food Donor      | Register with enterprise credentials and specify role        | Must Have     |
| US-02   | Food Donor      | Log in securely and receive stateless JWT bearer token       | Must Have     |
| US-03   | Food Donor      | Post surplus food batch with details, quantity, and expiry   | Must Have     |
| US-04   | Food Donor      | View active listings and track delivery progression in real-time | Must Have  |
| US-05   | NGO / Food Bank | Search and browse available food batches in the locality     | Must Have     |
| US-06   | NGO / Food Bank | Request/claim available donation matched to shelter capacity | Must Have     |
| US-07   | NGO / Food Bank | View assigned requests and track transit updates             | Must Have     |
| US-08   | Volunteer       | View available pickup tasks assigned to verified NGOs        | Must Have     |
| US-09   | Volunteer       | Accept a pending transport task                              | Must Have     |
| US-10   | Volunteer       | Transition transport status from Accepted -> Picked Up       | Must Have     |
| US-11   | Volunteer       | Confirm final delivery handover to NGO (Mark as Delivered)   | Must Have     |
| US-12   | Administrator   | Access protected governance dashboard with platform metrics  | Must Have     |
| US-13   | Administrator   | Audit all global donation records with donor/NGO/volunteer   | Must Have     |
| US-14   | Administrator   | Inspect registered user directory and role designations      | Must Have     |
| US-15   | Beneficiary     | Receive safely transported, unexpired meals via local NGO    | Must Have     |
| US-16   | All Users       | Enforce secure salted password storage (bcrypt)              | Must Have     |
| US-17   | All Users       | Receive informative error notifications on invalid actions   | Should Have   |
| US-18   | Administrator   | Export system-wide sustainability and redistribution logs     | Should Have   |
+---------+-----------------+--------------------------------------------------------------+---------------+
```

---

## 3. System Architecture & High-Level System Design

### 3.1 Architectural Style
ReFood Connect utilizes a **Layered Client-Server Architecture** incorporating the **Service Layer Pattern**:

```
[ PRESENTATION LAYER: React.js 19 + Vite 8 SPA ]
       |
       | RESTful JSON API via Axios (JWT Interceptor)
       v
[ APPLICATION / API LAYER: Express.js 5.2 (Routes + Controllers) ]
       |
       | Business Logic Invocations
       v
[ BUSINESS LOGIC LAYER: Service Layer (authService, donationService, adminService) ]
       |
       | Relational Object Queries
       v
[ DATA ACCESS LAYER: Sequelize ORM v6.37 Models (User, Donation) ]
       |
       +-----------------------+-----------------------+
       | (Production / Dev)    | (Automated Tests)     |
       v                       v                       v
[ DATABASE: MySQL 8.0 ]   [ ISOLATION DB: SQLite in-memory ]
```

### 3.2 Software Engineering Principles Applied
1. **Modularity & High Cohesion:**
   * Controllers (`donationController.js`) parse HTTP payloads and return status codes.
   * Business validation, data sanitization, and state progression logic live exclusively in services (`donationService.js`).
2. **Low Coupling & Abstraction:**
   * Frontend communicates exclusively via decoupled REST endpoints (`api/axios.js`).
   * Database queries are abstracted behind Sequelize ORM, enabling swapping from MySQL to in-memory SQLite during automated testing without modifying business code.
3. **Defense in Depth:**
   * Passwords hashed using `bcryptjs` (10 rounds).
   * Routes guarded by JWT authentication middleware with role-based checks (`admin`, `donor`, `ngo`, `volunteer`).
   * Sequelize parameterizes all queries, preventing SQL injection vulnerabilities.

---

## 4. Design of Tests & Empirical Quality Assurance

### 4.1 Testing Strategy
The quality assurance strategy encompasses three complementary verification layers:
1. **Integration Testing:** Tests end-to-end interactions between HTTP endpoints, middlewares, service layers, and the database.
2. **Regression Testing:** Verifies that new capabilities (such as the Administrator portal and volunteer progression buttons) do not break existing security guards, state machine rules, or schema boundaries.
3. **Mutation Testing (StrykerJS):** Tests the effectiveness of our test suite by systematically injecting code mutations (inverted logic, cleared strings, altered boundary conditions) into `donationService.js` and evaluating whether the tests catch and kill the mutants.

### 4.2 Comprehensive Test Cases Suite Table

```
+-------+-------------------------+----------------------------------+----------------------------------+---------+
| TC-ID | Target Component        | Test Scenario & Execution Step   | Expected Result                  | Status  |
+-------+-------------------------+----------------------------------+----------------------------------+---------+
| IT-01 | POST /api/auth/register | Register valid Food Donor        | 201 Created + JWT token returned | PASS    |
| IT-02 | POST /api/auth/register | Register with duplicate email    | 400 Bad Request + error message  | PASS    |
| IT-03 | POST /api/auth/login    | Authenticate valid user          | 200 OK + JWT token issued        | PASS    |
| IT-04 | POST /api/auth/login    | Submit incorrect password        | 401 Unauthorized + error message | PASS    |
| IT-05 | POST /api/auth/login    | Submit non-existent email        | 401 Unauthorized                 | PASS    |
| IT-06 | POST /api/donations     | Donor creates surplus listing    | 201 Created (Status: Available)  | PASS    |
| IT-07 | GET /api/donations      | NGO fetches available donations  | 200 OK + array with new donation | PASS    |
| IT-08 | PUT /api/donations/:id  | NGO requests available donation  | 200 OK (Status -> Requested)     | PASS    |
| IT-09 | PUT /api/donations/:id  | Volunteer claims transport task  | 200 OK (Status -> Accepted)      | PASS    |
| IT-10 | PUT /api/donations/:id  | Volunteer marks cargo picked up  | 200 OK (Status -> Picked Up)     | PASS    |
| IT-11 | PUT /api/donations/:id  | Volunteer confirms final delivery| 200 OK (Status -> Delivered)     | PASS    |
| IT-12 | Database Persistence    | Query record directly from DB    | Record persisted with Delivered  | PASS    |
| RT-01 | GET /api/admin/dashboard| Non-admin requests admin portal  | 403 Forbidden (RBAC Guard)       | PASS    |
| RT-02 | GET /api/admin/dashboard| Admin requests admin portal      | 200 OK + platform metrics object | PASS    |
| RT-03 | POST /api/donations     | Donor submits empty food details | 400 Bad Request + error message  | PASS    |
| RT-04 | POST /api/donations     | NGO attempts to post donation    | 403 Forbidden (Role Guard)       | PASS    |
| RT-05 | PUT /api/donations/:id  | Jump from Available -> Delivered | 400 Bad Request (Machine Guard)  | PASS    |
| RT-06 | PUT /api/donations/:id  | Submit invalid status string     | 400 Bad Request (Enum Guard)     | PASS    |
| RT-07 | GET /api/donations      | Request without Authorization    | 401 Unauthorized                 | PASS    |
| UT-01 | donationService.create  | Reject null food details         | Throws "Food details required"   | PASS    |
| UT-02 | donationService.create  | Reject whitespace quantity       | Throws "Quantity is required"    | PASS    |
| UT-03 | donationService.create  | Reject null expiry time          | Throws "Expiry time required"    | PASS    |
| UT-04 | donationService.create  | String trimming verification     | Details & quantity whitespace-cut| PASS    |
| UT-05 | donationService.getRole | Role query handling (vol/admin)  | Returns populated model arrays   | PASS    |
| UT-06 | donationService.update  | Non-existent record update       | Throws "Donation not found"      | PASS    |
| UT-07 | donationService.update  | Disallow illegal status values   | Throws "Invalid status"          | PASS    |
| UT-08 | donationService.update  | Strict sequential transition checks| Throws exact machine errors      | PASS    |
+-------+-------------------------+----------------------------------+----------------------------------+---------+
```
**Total Tests:** 27  
**Passed:** 27 (100.0%)  
**Failed:** 0  

### 4.3 Mutation Testing Analysis (StrykerJS)
* **Target:** `server/services/donationService.js`
* **Baseline Score:** 60.31% (79 killed, 15 survived, 37 no coverage)
* **Hardened Score:** **84.73%** (111 killed, 14 survived, 6 no coverage)
* **Covered Mutation Score:** **88.80%**
* **Score Improvement:** **+24.42%** net gain in mutation detection efficacy through targeted unit test hardening.

---

## 5. Implementation Evidence & Operational Traceability

### 5.1 End-to-End Workflow Verification
The core redistribution pipeline was validated across all 5 states:
1. **Food Donor** logs into the portal and posts a batch of surplus meals (`50 Veg Meal Trays`). The system stores the record in `Available` status with `donorId` attached.
2. **NGO** logs into the portal, discovers the listing, and clicks "Request Donation". The status changes to `Requested` with `ngoId` attached.
3. **Volunteer** opens the dashboard, locates the requested task under "Available Pickups", and accepts it. The status transitions to `Accepted` with `volunteerId` attached.
4. **Volunteer** marks the item as "Picked Up" upon collection from the donor, transitioning status to `Picked Up`.
5. **Volunteer** marks "Delivered" upon safe handover to the NGO shelter. The final status is persisted in the database as `Delivered`.
6. **Administrator** verifies live metrics in the Admin Dashboard, observing real-time increments in total donations, delivered meal counts, and audit tables.

---

## 6. Conclusion, Limitations & Future Scope

### 6.1 Conclusion
ReFood Connect successfully demonstrates a secure, modular, layered web application for surplus food redistribution. Through rigorous automated testing (27/27 integration and regression tests passing) and automated mutation testing (84.73% mutation score), the platform exhibits high resilience, verified security boundaries, and strict adherence to software engineering best practices.

### 6.2 Known Limitations
* **Geospatial Proximity:** Distance sorting is currently simulated; real-time GPS route optimization is planned for future milestones.
* **Cold-Chain Sensor Tracking:** IoT temperature verification for perishable food batches is not yet integrated.

### 6.3 Future Scope
* **Native Mobile Applications:** React Native mobile clients for volunteers in transit.
* **Predictive Matching:** Machine learning-based surplus prediction for recurring banquet events.
* **Automated SMS/Push Notifications:** WebSockets and SMS gateways for instant pickup alerts.

---

## 7. Appendices

### Appendix A: Software Requirements Specification (SRS)

#### A.1 Functional Requirements
* **FR-01 (Authentication):** The system shall authenticate users using email and salted bcrypt password hashes, issuing a signed 24-hour JWT.
* **FR-02 (Role Segregation):** The system shall enforce RBAC for four active roles: Donor, NGO, Volunteer, and Administrator.
* **FR-03 (Listing Creation):** Donors shall be able to post food items with non-empty food description, quantity, and expiry timestamp.
* **FR-04 (Claiming Workflow):** NGOs shall be able to claim available food batches, transitioning status from `Available` to `Requested`.
* **FR-05 (Transport Workflow):** Volunteers shall be able to claim transport tasks and update transit status sequentially (`Accepted` → `Picked Up` → `Delivered`).
* **FR-06 (Governance):** Administrators shall have access to aggregated platform analytics and user audit lists.

#### A.2 Non-Functional Requirements
* **NFR-01 (Security):** Plaintext passwords shall never be persisted. All database queries shall be parameterized by the ORM.
* **NFR-02 (Performance):** In-memory test executions shall complete within 10 seconds across all test suites.
* **NFR-03 (Maintainability):** The codebase shall adhere to the Service Layer pattern, decoupling controllers from database models.
* **NFR-04 (Portability):** The application shall support multi-container deployment via Docker Compose.

---

### Appendix B: Data Flow Diagrams (DFD)

#### B.1 Level 0 Context Diagram
```
                     +---------------------------------------+
                     |              FOOD DONOR               |
                     +-------------------+-------------------+
                                         | 1. Food Listing
                                         v
+---------------+    2. Request Claim    +-------------------+    3. Transport Task   +---------------+
|     NGO       | <--------------------> |   REFOOD CONNECT  | <--------------------> |   VOLUNTEER   |
+---------------+                        |   PLATFORM SYSTEM |                        +---------------+
                                         +---------+---------+
                                                   | 4. Governance & Auditing
                                                   v
                                         +-------------------+
                                         |   ADMINISTRATOR   |
                                         +-------------------+
```

#### B.2 Level 1 Process Decomposition Diagram
```
[ Donor ] -----> ( Process 1.0: Authenticate & Validate ) <----- [ User Store ]
                        |
                        v
[ Donor ] -----> ( Process 2.0: Create Food Listing ) ----> [ Donation Store ]
                                                                   |
[ NGO ] --------> ( Process 3.0: Request Donation ) <---------------+
                        |
                        v [ Status: Requested ]
[ Volunteer ] --> ( Process 4.0: Accept & Update Transit ) --------> [ Donation Store ]
                        |
                        v [ Status: Delivered ]
[ Admin ] ------> ( Process 5.0: Platform Aggregation ) <----------- [ All Stores ]
```

---

### Appendix C: Entity-Relationship Diagram (ERD)

```
+------------------------------------+             +------------------------------------+
|               USERS                |             |             DONATIONS              |
+------------------------------------+             +------------------------------------+
| PK  id           INTEGER (AUTO)    | 1         N | PK  id           INTEGER (AUTO)    |
|     name         VARCHAR(255)      |<----------->| FK  donorId      INTEGER (NOT NULL)|
|     email        VARCHAR(255) (UQ) | 1         N | FK  ngoId        INTEGER (NULLABLE)|
|     password     VARCHAR(255)      |<----------->| FK  volunteerId  INTEGER (NULLABLE)|
|     role         ENUM(...)         | 1         N |     foodDetails  VARCHAR(255)      |
|     createdAt    DATETIME          |<----------->|     quantity     VARCHAR(255)      |
|     updatedAt    DATETIME          |             |     expiryTime   DATETIME          |
+------------------------------------+             |     status       ENUM(...)         |
                                                   |     createdAt    DATETIME          |
                                                   |     updatedAt    DATETIME          |
                                                   +------------------------------------+

Relational Constraints:
- User (id) 1 ---- N Donation (donorId)      [Donor publishes multiple donations]
- User (id) 1 ---- N Donation (ngoId)        [NGO requests multiple donations]
- User (id) 1 ---- N Donation (volunteerId)  [Volunteer transports multiple donations]
```

---

### Appendix D: Unified Modeling Language (UML) Diagrams

#### D.1 Use Case Diagram
```
                               +-------------------------------------+
                               |         ReFood Connect System       |
                               +-------------------------------------+
   (Food Donor) -------------> | (UC-01: Register & Login)           |
   (NGO) --------------------> | (UC-02: Browse Available Listings)  |
   (Volunteer) --------------> | (UC-03: Create Food Donation)       |
   (Admin) ------------------> | (UC-04: Request Food Donation)      |
                               | (UC-05: Accept Transport Task)      |
                               | (UC-06: Update Delivery Status)     |
                               | (UC-07: View Governance Dashboard)  |
                               +-------------------------------------+
```

#### D.2 Sequence Diagram: End-to-End Donation Lifecycle
```
Donor            NGO             Volunteer          API Server           Database
  |               |                  |                  |                   |
  |-- Post Meal ->|                  |                  |-- Create Listing->|
  |               |                  |                  |<- Status: Avail --|
  |               |-- Request Meal ->|                  |-- Assign NGO ---->|
  |               |                  |                  |<- Status: Req ----|
  |               |                  |-- Accept Task -->|-- Assign Vol ---->|
  |               |                  |                  |<- Status: Acc ----|
  |               |                  |-- Mark Picked -->|-- Update State -->|
  |               |                  |                  |<- Status: Transit-|
  |               |                  |-- Mark Deliv --->|-- Persist Done -->|
  |               |                  |                  |<- Status: Deliv --|
```

#### D.3 Class Diagram: Backend Architecture
```
+--------------------------------+           +---------------------------------+
|          UserController        |           |       DonationController        |
+--------------------------------+           +---------------------------------+
| + register(req, res)           |           | + createDonation(req, res)      |
| + login(req, res)              |           | + getDonations(req, res)        |
+---------------+----------------+           | + updateDonation(req, res)      |
                |                            +----------------+----------------+
                v                                             v
+--------------------------------+           +---------------------------------+
|          AuthService           |           |         DonationService         |
+--------------------------------+           +---------------------------------+
| + register(name, email, pwd)   |           | + createDonation(donorId, ...)  |
| + login(email, password)       |           | + getDonationsByRole(user)      |
+---------------+----------------+           | + updateDonationStatus(id, ...) |
                |                            +----------------+----------------+
                v                                             v
+--------------------------------+           +---------------------------------+
|           UserModel            | 1       N |          DonationModel          |
+--------------------------------+-----------+---------------------------------+
| id, name, email, password, role|           | id, donorId, ngoId, status...   |
+--------------------------------+           +---------------------------------+
```

---

### Appendix E: Code Listing Excerpts & Repository Information

#### Official GitHub Repository
* **URL:** [https://github.com/ChiragAsija1323/ReFood-Connect](https://github.com/ChiragAsija1323/ReFood-Connect)
* **Default Branch:** `main`

#### Key Code Files
* `server/services/donationService.js`: Finite state machine and business validation.
* `server/controllers/adminController.js`: Role-based platform analytics and governance.
* `server/middleware/authMiddleware.js`: Stateless JWT verification and user decoration.
* `client/src/pages/AdminDashboard.jsx`: React dashboard component with live metrics.
* `server/__tests__/donations.test.js`: Integration test suite for full redistribution lifecycle.
