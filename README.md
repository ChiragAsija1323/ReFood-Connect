# ReFood Connect

## Smart Food Waste Redistribution Platform

---

## Project Overview

ReFood Connect is a web application developed to reduce food wastage by connecting food donors with NGOs and volunteers. Restaurants, hotels, supermarkets, and event organizers can donate surplus food, while NGOs can request donations and volunteers can assist with collecting and delivering the food to those in need.

The main goal of the project is to make food donation simple, transparent, and efficient.

---

## Problem Statement

Every day, a significant amount of edible food is discarded even though many people do not have access to sufficient meals. The absence of a centralized platform makes it difficult for donors, NGOs, and volunteers to coordinate food redistribution effectively. ReFood Connect addresses this problem by providing a common platform for all stakeholders.

---

## Project Objectives

- Minimize food wastage through timely redistribution.
- Provide a platform for food donors to donate surplus food.
- Enable NGOs to view and request available donations.
- Allow volunteers to manage food pickup and delivery.
- Track the complete donation process from donor to recipient.
- Improve coordination between all users of the system.

---

## User Roles

The system supports four different user roles:

- **Food Donor** – Adds and manages food donations.
- **NGO** – Requests and receives available food donations.
- **Volunteer** – Collects food from donors and delivers it to NGOs.
- **Administrator** – Monitors users, donations, and overall system activities.

---

## Main Features

- Secure user registration and login
- Food donation management
- Donation browsing and acceptance
- Volunteer assignment
- Pickup and delivery tracking
- Individual dashboards for each user role
- Donation history and status updates

---

## Technology Stack

### Frontend
- React.js

### Backend
- Node.js
- Express.js

### Database
- MySQL

### Development Tools
- GitHub
- Docker
- Figma
- Draw.io
- Visual Studio Code

---

## Project Structure

```text
ReFood-Connect/
│
├── client/
├── server/
├── design/
│   ├── diagrams/
│   └── wireframes/
├── docs/
├── docker/
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Branching Strategy

This project follows the **GitHub Flow** workflow.

- **main** – Contains the stable version of the project.
- **feature/*** – Used for developing individual features.

Examples:

- feature/login-page
- feature/donor-dashboard
- feature/volunteer-module

Once a feature is completed and tested, it is merged into the **main** branch.

---

## Project Documentation

The project documentation is available inside the **docs** folder.

It includes:

- Vision Document
- User Stories
- MoSCoW Prioritization
- Architecture Description

---

## UI Design

All Figma wireframes are stored in:

```text
design/wireframes/
```

These wireframes include:

- Login Page
- Registration Page
- Food Donor Dashboard
- NGO Dashboard
- Volunteer Dashboard
- Admin Dashboard

---

## Local Development

Detailed setup instructions and Docker commands will be added after the development environment is configured.

---

## Future Enhancements

Some features planned for future versions include:

- Mobile application support
- GPS-based pickup tracking
- Push notifications
- AI-assisted food matching
- Reports and analytics dashboard

---

## Contributors

**Chirag Asija**
**Saanvi Gupta**

VIT Chennai  
B.Tech Computer Science and Engineering

---

## License

This project has been developed as part of the **Software Engineering (BCSE301L)** course at **VIT Chennai** for academic purposes.