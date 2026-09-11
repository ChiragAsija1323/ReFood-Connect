# 🍃 ReFood Connect

**Smart Food Waste Redistribution Platform**

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express.js](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

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

---

## Contributors

Chirag Asija (24BDS1073)  
Saanvi Gupta (24BDS1023)  

**Software Engineering (BCSE301L)**  
VIT Chennai
