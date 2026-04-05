# Sports Pick'em Project - Platform

## Video Demo

https://youtu.be/mJrBDhuYcM0

## Project Description

Sports Pick'em Platform is a web application that allows users to create and participate in prediction leagues for sports such as the NFL and NBA.
The platform enables users to make picks for upcoming games, track results in real time, and compete against other participants through a live leaderboard.
The project was built using Python with Flask for the backend, SQLite for the database, and HTML/CSS/JavaScript for the frontend.
It integrates live sports data from ESPN to dynamically update game scores and results.

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
