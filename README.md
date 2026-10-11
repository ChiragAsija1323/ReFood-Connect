# 🍃 ReFood Connect

**Smart Food Waste Redistribution Platform**

---

## Project Overview

ReFood Connect is a web-based platform designed to reduce food wastage by connecting food donors with NGOs and volunteers. The project aims to simplify the food donation process and ensure that excess food reaches people in need instead of being wasted.

---

## Key Features & User Roles

Our platform provides capabilities for five distinct user roles:

- **Food Donors**: Create surplus food donation listings, specify quantity and expiry information, and track donation status.
- **NGOs / Food Banks**: Browse available donations, request suitable food, and manage received donations.
- **Volunteers**: View available pickup tasks, accept deliveries, and update delivery status.
- **Beneficiaries**: Receive donated food through the NGO and volunteer distribution process.
- **Administrators**: Monitor platform activity, manage users, verify organizations, and oversee donations.

---

## 🏗️ Software Design & Architecture (DA-2)

The ReFood Connect platform follows a Layered Client-Server Architecture with clear separation between the presentation, application/API, business logic, and data access responsibilities. This structure was selected to improve maintainability, modularity, and separation of concerns.

### Design Principles

#### Modularity
The application is divided into separate presentation, API, business logic, and data access layers. This allows individual modules to be developed, tested, and maintained independently.

#### High Cohesion
Each module is responsible for a focused set of related tasks. For example, donation-related operations are grouped within the donation functionality instead of being scattered across unrelated modules.

#### Low Coupling
The React frontend communicates with the backend through REST APIs instead of directly accessing the database. This keeps the frontend and backend independent and makes future changes easier.

#### Abstraction
Sequelize ORM provides an abstraction over database operations, allowing the application to work with models and persistence logic without directly handling database-specific SQL throughout the application.

---

### High-Level Architecture

The system uses a Layered Client-Server Architecture. The React.js frontend provides the user interface, communicates with the Node.js/Express.js backend through REST APIs, and the backend uses Sequelize ORM for database access to MySQL.

![ReFood Connect High-Level Architecture](./design/diagrams/Architecture.png)

**Architecture style:** Layered Client-Server Architecture

**Why this style?**
This style separates presentation, application logic, business rules, and persistence responsibilities. It reduces dependencies between layers, improves code organization, and makes future changes easier because individual layers can be modified with minimal impact on the others.

---

### 🎨 User Interface Design

The user interface was designed in Figma and refined from the DA-1 wireframes to improve visual hierarchy, consistency, navigation, readability, and ease of use.

1. Login
2. Registration
3. Food Donor Dashboard
4. NGO Dashboard
5. Volunteer Dashboard
6. Administrator Dashboard

**Figma Prototype:** [Add final Figma prototype link here]

#### How the UI was made user-friendly
- Consistent navigation across role-based dashboards
- Clear visual hierarchy using headings, cards, status indicators, and primary actions
- Simple forms for donation creation and authentication
- Role-specific dashboards so users see only relevant functionality
- Clear status labels for donations, requests, and deliveries
- Consistent spacing, typography, and visual styling
- Responsive layout considerations

---

### Design Decisions

1. **Layered architecture** — chosen to separate UI, API, business logic, and database responsibilities.
2. **REST API communication** — chosen to keep the React frontend independent from backend implementation details.
3. **Sequelize ORM** — chosen to provide database abstraction and simplify interaction with MySQL.
4. **Role-based dashboards** — chosen so each user role gets a focused interface containing relevant actions.

---

## Technology Stack

**Frontend:**
React.js + Vite

**Backend:**
Node.js + Express.js

**Database:**
MySQL

**ORM:**
Sequelize

**DevOps:**
Docker + Docker Compose

**Design:**
Figma + Draw.io / diagrams.net

**HTTP Client:**
Axios

---

## 🚀 Quick Start – Local Development

The entire application stack, including the MySQL database, has been containerized. You can build and run it seamlessly using Docker Compose.

### Clone the Repository
```bash
git clone https://github.com/ChiragAsija1323/ReFood-Connect.git
cd ReFood-Connect
```

### Build and Start with Docker
```bash
docker compose up --build
```

### Application URLs
- **Frontend UI:** `http://localhost:5173`
- **Backend API:** `http://localhost:8000`

---

## Project Structure

```text
ReFood-Connect/
├── client/
├── server/
├── design/
│   ├── diagrams/
│   │   ├── Architecture.drawio
│   │   └── Architecture.png
│   └── wireframes/
│       ├── AdminDashboard.png
│       ├── FoodDonorDashboard.png
│       ├── Login.png
│       ├── NGODashboard.png
│       ├── Registration.png
│       └── VolunteerDashboard.png
├── docs/
│   ├── MoSCoW_Prioritization.md
│   ├── Software_Design_Document.md
│   ├── User_Stories.md
│   └── Vision_Document.md
├── docker-compose.yml
└── README.md
```

---

### 📁 Design Artifacts

This repository contains the design phase submissions for Digital Assignment 1 & 2:

- [Architecture Source](./design/diagrams/Architecture.drawio)
- [Architecture PNG](./design/diagrams/Architecture.png)
- [Software Design Document](./docs/Software_Design_Document.md)

## 🧪 Quality Assurance, Testing & DA-3 Evidence

ReFood Connect adheres to strict software verification standards as evaluated in Digital Assignment 3 (Review 3):

### 1. Automated Integration & Regression Testing
Tests are isolated from development databases using an in-memory SQLite driver (`sqlite::memory:`).

```bash
# Run complete test suite (27 tests across 4 suites)
cd server
npm test

# Run dedicated regression test suite
npm run test:regression
```
* **Status:** 27/27 Tests Passed (100% Pass Rate).
* **Execution Time:** ~5.3 seconds.

### 2. Mutation Testing (StrykerJS)
Fault-injection mutation testing was performed on `server/services/donationService.js`:

```bash
cd server
npx stryker run
```
* **Total Mutants Evaluated:** 131
* **Mutants Killed:** 111 (✓)
* **Covered Mutation Score:** **88.80%**
* **Total Mutation Score:** **84.73%** (improved from 60.31% baseline)
* **HTML Report:** `server/reports/mutation/mutation.html`

### 3. Build & Containerization
```bash
# Frontend production build
cd client
npm run build

# Docker Compose specification validation
docker compose config
```

---

## 📁 DA-3 Documentation & Deliverables

- 📄 **[DA-3 Technical Evidence Report (Markdown)](./docs/DA3_Evidence_Report.md)**
- 📕 **[DA-3 Technical Evidence Report (PDF)](./docs/DA3_Evidence_Report.pdf)**
- 📄 **[DA-3 Final Project Report & Appendices (Markdown)](./docs/DA3_Project_Report.md)**
- 📕 **[DA-3 Final Project Report & Appendices (PDF)](./docs/DA3_Project_Report.pdf)**
- 🎤 **[Live Viva & Demonstration Script](./docs/VIVA_DEMO_GUIDE.md)**
- 🏗️ **[Software Design Document (DA-2)](./docs/Software_Design_Document.md)**
- 📐 **[Architecture Diagram (PNG)](./design/diagrams/Architecture.png)**

---

## Contributors

* **Chirag Asija** (Registration No: `24BDS1073`)  
* **Saanvi Gupta** (Registration No: `24BDS1023`)  

**Course:** Software Engineering (`BCSE301L`)  
**Institution:** Vellore Institute of Technology (VIT), Chennai Campus

