Software Design Document
Project: ReFood Connect – Smart Food Waste Redistribution Platform Course: Software Engineering (BCSE301L)

Team Members:-
Chirag Asija, 24BDS1073
Saanvi Gupta, 24BDS1023


1. Design Principles Applied

In designing ReFood Connect, we strictly adhered to fundamental software engineering principles to ensure the system is scalable, robust, and easy to maintain.
Modularity & High Cohesion The system is highly modular, dividing responsibilities into distinct layers. Our backend follows the Service Layer Pattern (Routes ? Controllers ? Services ? Models).
* High Cohesion: Instead of placing database queries and business logic inside Express route handlers, we created dedicated service classes (e.g., donationService.js). The controller is only responsible for handling HTTP requests and responses, while the service strictly handles the business rules of food donations. This ensures that each module does one thing and does it well.
Low Coupling & Abstraction
* Low Coupling: The React.js frontend is entirely decoupled from the Express.js backend. They communicate exclusively via a RESTful API using Axios. The frontend does not know how the database works; it only knows the API contracts.
* Abstraction: On the backend, we utilized the Sequelize ORM to interact with the MySQL database. This abstracts away raw SQL queries. The business logic interacts with Sequelize models, meaning if we ever needed to migrate to PostgreSQL, the business logic layer would remain entirely untouched.

2. High-Level Architecture

Architecture Style Chosen: Layered Client-Server Architecture (MVC-inspired)
Why this style? We chose a Layered Client-Server architecture because ReFood Connect requires multiple distinct user roles (Donors, NGOs, Volunteers, Admins) accessing a centralized data source. Separating the Presentation Layer (React) from the Application Layer (Express API) allows us to scale the frontend and backend independently. The layered backend ensures that security (Authentication), business rules (Services), and data persistence (ORM) are strictly segregated, preventing "spaghetti code."

Figure 1: ReFood Connect High-Level Architecture Diagram

3. User Interface Design

The User Interface was designed in Figma following modern SaaS principles, focusing on clarity and reducing cognitive load for different user roles.












 (Login, Registration, Donor Dashboard, NGO Dashboard, Volunteer Dashboard, Admin Dashboard)




How we made the UI user-friendly:
1. Role-Based Dashboards: Instead of one cluttered interface, the UI dynamically changes based on the user's role. A volunteer only sees "Available Pickups", while an NGO sees "Available Donations", preventing confusion.
2. Clear Visual Hierarchy: We implemented a consistent 8px/16px/24px spacing grid and used a restrained color palette (ReFood Green #16A34A for primary actions) to guide the user's eye to important buttons like "Request Donation".
3. Visual State Tracking: We used a step-by-step progress component for deliveries (Requested ? Accepted ? Picked Up ? Delivered), allowing users to understand the status of a donation at a single glance.

4. Design Decisions & Why

1. Decision: Implementing a Service Layer (Separation of Concerns)
* Why: Moving business logic out of controllers into a Service layer makes the code reusable. For example, both the web API and a potential future mobile app API can call the exact same donationService.createDonation() function.
2. Decision: Using React.js for the Frontend
* Why: ReFood Connect requires a highly interactive dashboard where real-time status updates are frequent. React's component-based virtual DOM allows for smooth, instant UI updates without full page reloads.
3. Decision: Using Sequelize ORM instead of raw SQL queries
* Why: It protects against SQL injection attacks by default, provides an easy abstraction for defining relationships, and drastically speeds up development time.
4. Decision: Dockerizing the Environment
* Why: To eliminate "it works on my machine" issues. By using Docker Compose, the React frontend, Express backend, and MySQL database spin up consistently across any team member's operating system.

5. Maintainability and Future Changes

ReFood Connect was designed with the future in mind.
* Maintainability: Because the system exhibits low coupling, a bug in the UI layout will never break the backend database logic. Developers can easily locate code because the folder structure strictly enforces separation (Routes, Controllers, Services, Models).
* Future Changes: If we decide to add a Mobile Application for volunteers on the road, the current architecture supports this seamlessly. The Mobile App can simply consume the existing REST API without requiring any changes to the backend or database layers. Furthermore, the modular design means adding a new feature—such as AI-based food matching—would only require adding a new MatchingService without rewriting existing code.
GitHub Repository: [PASTE YOUR GITHUB REPO LINK HERE]

