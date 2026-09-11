# ReFood Connect

## Smart Food Waste Redistribution Platform

---

## Project Overview
ReFood Connect is a web-based platform developed to reduce food wastage by connecting food donors with NGOs and volunteers. The project aims to simplify the food donation process and ensure that excess food reaches people in need instead of being wasted.

---

## Software Design (DA-2)

The ReFood Connect platform utilizes a **Layered Client-Server Architecture** (MVC) to ensure strong separation of concerns. We applied high cohesion and low coupling by isolating business rules into a dedicated Service layer, while using Sequelize ORM to abstract database interactions away from the Express.js controllers. The user interface was designed with strict role-based modularity, ensuring that Donors, NGOs, and Volunteers only see functionality relevant to their specific tasks, vastly reducing cognitive load.

![Architecture Diagram](./design/diagrams/Architecture.png)

*(Note: Figma UI Mockups can be found in the `/design/wireframes/` folder)*

---

## Target Users
- **Food Donors** – Restaurants, hotels, supermarkets, bakeries.
- **NGOs** – Organizations collecting and distributing food.
- **Volunteers** – Individuals assisting in collection and delivery.
- **Administrator** – Manages the platform.

---

## Technology Stack
- **Frontend:** React.js (Vite), Tailwind CSS
- **Backend:** Node.js, Express.js
- **Database:** MySQL, Sequelize ORM
- **Deployment:** Docker, Docker Compose

---

## Quick Start – Local Development

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
- **Frontend:** `http://localhost:5173`
- **Backend:** `http://localhost:8000`

---

## Contributors
- Saanvi Gupta (24BDS1023)
- Chirag Asija (24BDS1073)

**VIT Chennai**  
**B.Tech Computer Science and Engineering**
