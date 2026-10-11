# ReFood Connect — Live Demonstration & Viva Guide (DA-3)
**Course:** Software Engineering (`BCSE301L`) | VIT Chennai  
**Authors:** Chirag Asija (`24BDS1073`) & Saanvi Gupta (`24BDS1023`)

---

## 1. Quick Launch Instructions

Open two terminal windows:

### Terminal 1: Backend API Server
```bash
cd server
npm start
```
*Backend starts on `http://localhost:8000` with connected database.*

### Terminal 2: Frontend Web Client
```bash
cd client
npm run dev
```
*Frontend opens at `http://localhost:5173`.*

---

## 2. Recommended Live Demonstration Sequence

Follow these 8 steps during the viva to showcase the complete workflow in under 3 minutes:

### Step 1: Donor Registration & Surplus Creation
1. Navigate to `http://localhost:5173/register`.
2. Register as a **Food Donor**:
   * Name: `Grand Banquet Chennai`
   * Email: `donor@demo.com`
   * Password: `password123`
   * Role: `Food Donor`
3. Click **Register** → redirected to `/login`.
4. Log in as `donor@demo.com` → auto-redirected to `/donor` dashboard.
5. Create a food listing:
   * Food Details: `50 Trays of Paneer Butter Masala & Rotis`
   * Quantity: `50 meals`
   * Expiry Time: *Select a future date/time*
6. Click **Create Donation**.
7. Point out to professor: The donation listing appears in the table with status **Available**.

### Step 2: NGO Discovery & Request
1. Click **Logout**.
2. Navigate to `/register` and create an **NGO account**:
   * Name: `Hope Shelter Foundation`
   * Email: `ngo@demo.com`
   * Password: `password123`
   * Role: `NGO`
3. Log in as `ngo@demo.com` → redirected to `/ngo` dashboard.
4. Point out to professor: Under "Available Donations", the 50 meals listing created by Grand Banquet is visible.
5. Click **Request Donation**.
6. Point out to professor: Status changes to **Requested**, and the NGO ID is attached.

### Step 3: Volunteer Task Acceptance & Transport
1. Click **Logout**.
2. Navigate to `/register` and create a **Volunteer account**:
   * Name: `Ravi Volunteer Runner`
   * Email: `volunteer@demo.com`
   * Password: `password123`
   * Role: `Volunteer`
3. Log in as `volunteer@demo.com` → redirected to `/volunteer` dashboard.
4. Under "Available Pickups", locate the task from Grand Banquet to Hope Shelter.
5. Click **Accept Pickup**.
6. Point out to professor: The task moves into "My Deliveries" with status **Accepted**.
7. Click **Mark as Picked Up** → status updates to **Picked Up**.
8. Click **Mark as Delivered** → status updates to **Delivered**.

### Step 4: Administrator Governance & Metrics Verification
1. Click **Logout**.
2. Navigate to `/register` and register an **Administrator account**:
   * Name: `Prof / Admin Controller`
   * Email: `admin@demo.com`
   * Password: `password123`
   * Role: `Administrator`
3. Log in as `admin@demo.com` → auto-redirected to `/admin` dashboard.
4. Point out to professor:
   * **Total Users:** Dynamically reflects registered users.
   * **Total Donations & Delivered Donations:** Accurately reflects the completed delivery.
   * **All Food Donations Table:** Shows the full audit trail with donor name, assigned NGO, and assigned volunteer.
   * **Registered Users Table:** Lists all platform accounts with role badges.

### Step 5: Live Test Suite Execution
In the terminal, run:
```bash
cd server
npm test
```
Show the professor that all **27 tests pass across 4 test suites in ~5 seconds**, verifying that the entire business workflow, security guards, and database persistence are tested automatically.

### Step 6: Show Mutation Testing Report
Open in browser:
```text
server/reports/mutation/mutation.html
```
Highlight the **84.73% mutation score** and explain how Stryker injected 131 synthetic mutations to prove test suite strength.

---

## 3. High-Probability Viva Questions & Model Answers

### Q1: Why did you choose a Layered Architecture over a monolithic approach?
**Answer:**  
*"We implemented a Layered Client-Server Architecture using the Service Layer Pattern. By isolating presentation (React), API routing (Express controllers), business logic (Services), and database models (Sequelize ORM), we achieved high cohesion and low coupling. Controllers only handle HTTP statuses, while services strictly enforce business rules. This also allows the React web client and any future mobile apps to share the exact same backend logic without duplication."*

### Q2: How did you isolate tests from your production MySQL database?
**Answer:**  
*"In `server/config/database.js`, we implemented dynamic environment-driven connection logic. When `NODE_ENV === 'test'`, Sequelize connects to an in-memory SQLite database (`sqlite::memory:`). This means automated tests run in milliseconds without network latency, don't require an active MySQL daemon, and leave zero leftover data in the development database."*

### Q3: What is Mutation Testing and what did StrykerJS prove in your project?
**Answer:**  
*"Standard code coverage only measures if a line was executed, not whether the test would catch bugs. Mutation testing introduces intentional defects—such as inverting conditions (`!==` to `===`) or altering return values—to test the tests themselves. Our test suite achieved an 84.73% mutation score with 111 mutants killed on `donationService.js`, proving that our assertions actively catch state violations and boundary errors."*

### Q4: How does your system prevent unauthorized status transitions?
**Answer:**  
*"We implemented a finite state machine in `donationService.js`. A donation can only follow the sequence: `Available` → `Requested` → `Accepted` → `Picked Up` → `Delivered`. If an attacker attempts to skip phases (for instance, trying to jump from `Available` directly to `Delivered`), the service throws a validated error and returns `400 Bad Request`. Furthermore, route-level RBAC middleware ensures that only NGOs can request donations, and only volunteers can update delivery transit states."*
