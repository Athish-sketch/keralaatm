# ATM Fleet Cash Optimization & Predictive Telemetry Platform

A hybrid PHP/Python web platform that models branch cash-out risks, automates emergency mathematical replenishment fallbacks during cloud disconnects, and enforces role-based fleet isolation.

---

## Key Features

* Predictive Microservice: Python/Flask backend evaluating withdrawal velocity, temporal consumption spikes, and emergency replenishment schedules.
* High Availability Math Fallback: If the external prediction microservice goes offline, client operations switch instantly to a deterministic local moving-average algorithm to eliminate downtime.
* Multi-Tenant Branch RBAC: Role-Based Access Control enforcing query-level scope restrictions so branch managers can only inspect their designated fleet.
* Client-Side Async Polling: Simulates live transaction throughput using the JavaScript Fetch API to update telemetry dials without cron overhead.

---

## Technical Stack

* Web Application: PHP 8.x (PDO), JavaScript (Vanilla ES6), HTML5, Bootstrap 5
* Predictive Microservice: Python 3.10+, Flask, NumPy
* Database: MySQL (Structured Schema, Foreign Key Constraints, Indexed Lookups)
* Hosting: InfinityFree (Web Layer), Render (Microservice API)

---

## Architecture Overview

[Browser Dashboard]
        │
        ├── (Direct DB Queries / Auth via PDO) ────► [MySQL Database]
        │
        └── (Async Telemetry via Fetch API) ──────► [Python Flask Microservice]
                                                           │
                                          (If Down: Trigger Deterministic Math Fallback)

---

## Setup & Configuration

1. Database Setup:
   Import schema.sql into your MySQL server.
   Configure database credentials in config/db.php.

2. Run the Prediction Microservice:
   cd api
   pip install -r requirements.txt
   python app.py

3. Host PHP Front-End:
   php -S localhost:8080
