# ReFood Connect

## Smart Food Waste Redistribution Platform

---

## Project Overview

ReFood Connect is a web-based platform developed to reduce food wastage by connecting food donors with NGOs and volunteers. Restaurants, hotels, supermarkets, event organizers, and other food providers can donate surplus edible food, while NGOs can request available donations and volunteers can assist with collection and delivery.

The project aims to simplify the food donation process and ensure that excess food reaches people in need instead of being wasted.

---

## Problem Statement

Food wastage is a major issue across the world. Every day, large quantities of edible food are discarded while many people struggle to access regular meals. Although many organizations are willing to donate surplus food, there is often no efficient system to connect donors with NGOs and volunteers in real time.

ReFood Connect addresses this problem by providing a centralized platform where all stakeholders can coordinate food donations quickly and efficiently.

---

## Vision Statement

To develop a reliable and user-friendly platform that minimizes food wastage by connecting food donors, NGOs, volunteers, and administrators through a single digital system, ultimately contributing to a more sustainable and hunger-free society.

---

## Target Users

The application is designed for the following users:

- **Food Donors** – Restaurants, hotels, supermarkets, bakeries, and event organizers.
- **NGOs** – Organizations responsible for collecting and distributing donated food.
- **Volunteers** – Individuals who assist in collecting and delivering food.
- **Administrator** – Manages users, donations, and overall platform activities.

---

## Project Objectives

- Reduce food wastage through efficient redistribution.
- Provide a simple platform for food donation.
- Enable NGOs to discover and request available food.
- Help volunteers manage pickup and delivery tasks.
- Track the complete donation lifecycle.
- Improve coordination among all stakeholders.

---

## Key Features

- Secure user registration and login
- Food donation management
- NGO donation request system
- Volunteer assignment
- Pickup and delivery tracking
- Role-based dashboards
- Donation history and status updates
- Admin panel for monitoring users and donations

---

## Success Metrics

The success of the project can be measured through:

- Increase in successful food donations.
- Reduction in food wastage.
- Faster response time for food requests.
- Active participation of donors, NGOs, and volunteers.
- Positive user feedback regarding usability.

---

## Assumptions and Constraints

### Assumptions

- Food donors provide only safe and edible food.
- NGOs and volunteers have internet access.
- Users enter accurate information while registering and donating food.

### Constraints

- Internet connectivity is required to use the system.
- The initial version focuses on local food redistribution.
- Real-time GPS tracking is not included in the first release.

---

## Technology Stack

### Frontend

- React.js (Vite)

### Backend

- Node.js
- Express.js

### Database

- MySQL
- Sequelize ORM

### Development Tools

- Git
- GitHub
- Docker
- Docker Compose
- Figma
- Draw.io
- Visual Studio Code

---

## Project Structure

```text
ReFood-Connect/
│
├── client/
│   └── Dockerfile
├── server/
│   └── Dockerfile
├── design/
│   ├── diagrams/
│   └── wireframes/
├── docs/
├── docker/
├── docker-compose.yml
├── README.md
├── LICENSE
└── .gitignore
```

---

## Branching Strategy

This project follows the **GitHub Flow** branching model.

- **main** contains the stable version of the project.
- **feature/** branches are created for implementing individual features.

Example feature branches:

- feature/user-auth
- feature/donor-dashboard
- feature/volunteer-module

Each feature is developed separately, tested, and then merged into the **main** branch.

---

## Project Documentation

The project documentation is available in the **docs** folder.

It includes:

- Vision Document
- User Stories
- MoSCoW Prioritization
- Architecture Description

---

## UI Design

The user interface was designed using **Figma**.

The wireframes include:

- Login Page
- Registration Page
- Food Donor Dashboard
- NGO Dashboard
- Volunteer Dashboard
- Admin Dashboard

All design files are available in:

```text
design/wireframes/
```

---

# Quick Start – Local Development

## Prerequisites

Before running the project, install the following:

- Git
- Docker Desktop
- Node.js (optional if running without Docker)

---

## Clone the Repository

```bash
git clone https://github.com/ChiragAsija1323/ReFood-Connect.git
cd ReFood-Connect
```

---

## Build Docker Images

```bash
docker compose build
```

---

## Start the Application

```bash
docker compose up
```

---

## Application URLs

Frontend:

```
http://localhost:5173
```

Backend:

```
http://localhost:8000
```

---

## Future Enhancements

Some planned improvements for future versions include:

- Mobile application support
- GPS-based pickup tracking
- Push notifications
- AI-based food matching
- Reports and analytics dashboard
- Email and SMS notifications
- Real-time donation tracking

---

## Contributors

- Saanvi Gupta (24BDS1023)
- Chirag Asija (24BDS1073)

**VIT Chennai**  
**B.Tech Computer Science and Engineering**

---

## License

This project has been developed as part of the **Software Engineering (BCSE301L)** course at **VIT Chennai** for academic purposes.