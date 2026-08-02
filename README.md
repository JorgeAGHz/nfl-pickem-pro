# Sports Pick'em Project - Platform

## Video Demo

https://youtu.be/mJrBDhuYcM0

## Project Description

Sports Pick’em Platform is a full-stack web application that allows users to create and participate in prediction leagues for sports such as the NFL and NBA. The platform enables users to make picks for upcoming games, track results in real time, and compete against other participants through a dynamic leaderboard.

The application was built using Python with Flask as the backend framework, SQLAlchemy for database management, and SQLite as the database. The frontend was developed using HTML, CSS, and JavaScript, with a focus on creating an intuitive and responsive user interface.

One of the core features of the project is the live game tracking system, which integrates data from the ESPN API. A background scheduler continuously updates game scores, statuses, and results, allowing users to see real-time changes reflected in the application without manual refresh. This required careful handling of asynchronous updates and database consistency.

Another important aspect of the project is the pick visibility logic. To ensure fairness, users are not able to see other participants’ picks before a game starts. This required implementing conditional rendering logic that depends on the game state and the current user viewing the data.

The platform also includes a league management system, where users can create leagues, invite others via email using secure tokens, and participate in multiple leagues simultaneously. Additionally, an admin panel was implemented to allow administrators to load games, update results, and recover missing data when necessary.

From a design perspective, the project emphasizes separation of concerns by organizing logic into different services, such as handling live data, game state validation, and external API communication. This modular approach improves maintainability and scalability.

One of the main challenges during development was ensuring that live updates did not introduce inconsistencies or reveal sensitive information prematurely. This was addressed by centralizing the live logic and carefully controlling when and how data is displayed.

Overall, this project demonstrates the integration of backend logic, real-time data processing, and user experience design into a cohesive full-stack application. It reflects not only technical implementation but also product-oriented thinking, focusing on usability, fairness, and performance.

## Author

Jorge Gonzalez

## Key Features

### User System

* User registration and login
* Secure password hashing
* Role-based access (Admin vs Users)

### League System

* Create and join leagues
* Invite users via email with unique tokens
* Multiple leagues per user

### Picks System

* Users select winners (and conditions for NFL games)
* Picks are locked when games start
* Picks visibility controlled before game start

### Live Experience

* Real-time score updates (via scheduler)
* Live leaderboard across all games
* Game status indicators (Scheduled, Live, Final)
* Visual feedback for correct/incorrect picks

### Admin Panel

* Load games from ESPN API
* Update live scores manually
* Bootstrap missing historical results
* System monitoring (games, users, live games)

---

## Design Decisions

One of the main challenges of the project was ensuring that live updates did not break user experience or reveal sensitive information (such as other users' picks before games start). This was solved by centralizing the logic in a dedicated `live_service`, which controls how data is displayed depending on game status and viewer.

Another important decision was separating responsibilities into services:

* `espn_service` handles external API data
* `live_service` manages game state logic
* `game_service` controls game timing and locking

This modular structure improves maintainability and scalability.

---

## Technologies Used

* Python
* Flask
* SQLAlchemy
* SQLite
* HTML / CSS / JavaScript
* APScheduler (background jobs)
* ESPN API (sports data)

---

## Future Improvements

* Deploy as a production web app (Render / Railway)
* Add mobile-friendly responsive design
* Implement real-time updates with WebSockets
* Add advanced analytics (win probability, upset alerts)
* Improve UI/UX to match professional sports apps
