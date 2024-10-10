## **Hotel Analytical System** 🏨📊

### Deployment 🌐

The **Hotel Analytical System** is deployed on Heroku and can be accessed through the following URLs:

- [Frontend](https://hotel-analytical-system-05e4799de509.herokuapp.com/)
- [Backend (API)](https://hotel-analytical-system-api-c1d8171276c0.herokuapp.com/)

### Project Description 📋

The **Hotel Analytical System** is a platform designed to analyze and manage data related to hotel management. This system allows managers to view global statistics between hotels of the same franchise, local statistics for each individual hotel, manage employees, rooms, clients and reservations, and perform updates and deletions of records efficiently.

### Main Features ✨

- **Interactive Dashboard**: Display interactive statistics and graphs using `Voila`.
- **Session Security**: Implementation of a login system with sessions.
- **Role-based content**: The content you can see on the dashboard is based on the roles that the employee has at the time of logging in, which are regular employee, supervisor and administrator.
- **Reservation Management**: Manage reservations, including creation, update and cancellation.
- **Database Connection**: Integrates a PostgreSQL database hosted on Heroku.

### Technologies Used 💻

- **Backend**:
  - `Flask` as the main framework for the API.

- **Frontend**:
  - `Voila` to turn Jupyter Notebooks into interactive web applications.
  - `Jupyter Widgets` to create an interactive interface with charts and forms.

- **Database**:
  - `PostgreSQL`, managed through Heroku.

### Concepts Learned During the Project 📚

During the completion of this project, several key concepts in web development, database management, and software architecture were learned and applied. Some of the main ones are listed below:

1. **Database Design and Entity-Relationship Diagram (ERD)**:
   - Design of an **Entity-Relationship Diagram (ERD)** to model the relationships between entities such as customers, employees, reservations, rooms, etc.
   - Creation of **normalized database schemas** in PostgreSQL, guaranteeing consistency and integrity in the data.
   - Use of primary and foreign keys to define relationships between tables and ensure referential integrity.

2. **Management of Endpoints in the API**:
   - Creation of **RESTful endpoints** with Flask to perform CRUD operations (Create, Read, Update, Delete) on the data.
   - **GET**: Retrieve data on customers, employees, reservations, and more.
   - **POST**: Add new records such as customers, employees, or reservations.
   - **DELETE**: Delete records, such as deleting customers or canceling reservations.
   - **PUT**: Update existing information, such as modifying reservation details or updating an employee's salary.

3. **Statistics and Report Generation**:
   - Use of advanced SQL queries to extract data and generate reports, such as hotel occupancy statistics, revenue per customer or room, and average length of stay.
   - Application of aggregate functions such as **SUM(), AVG(), COUNT()** to perform calculations directly in the database.

4. **Frontend and Backend Integration**:
   - Using **Voila** to turn notebooks into interactive graphical interfaces.
   - Communication between the **frontend (Jupyter Widgets)** and the **backend (Flask API)** through HTTP requests (using `requests`).
   - Validating inputs in the frontend and handling responses from the backend, displaying success or error messages as needed.

5. **Cloud Deployment**:
   - **Configuration and deployment** of the application on **Heroku**, both the frontend (Voila) and the backend (Flask and PostgreSQL).
   - Using **Git** to control versions and upload changes to the corresponding remotes (GitHub and Heroku).
   - Setting up **environment variables** on Heroku to protect sensitive credentials and customize the behavior of the application.

This project was an excellent opportunity to practice and delve deeper into full stack web development, database management, and cloud application deployment.
