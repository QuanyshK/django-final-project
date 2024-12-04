# Balakay

Balakay is a Django-based web application designed for parents and recreational centers to manage profiles, children’s information, activity subscriptions, and bookings. It also includes an analytics dashboard, subscription tracking, and a custom admin panel, providing a seamless experience for both users and administrators.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Built With](#built-with)
- [Future Improvements](#future-improvements)
- [License](#license)

## Introduction

Balakay simplifies the management of recreational activities, subscriptions, and bookings for both parents and centers. The platform integrates advanced analytics, a subscription system, and booking functionality into a scalable and secure solution.

### Core Modules:

- **User Management**: Parents can register, log in, and manage profiles for themselves and their children.
- **Subscription System**: Flexible subscription plans tailored to various needs, with tracking of usage and remaining visits.
- **Activity Management**: Book and track activities for children.
- **Admin Panel for Partners**: Partners can manage their sections, schedules, and activities.
- **Analytics Dashboard**: Visualize key metrics like user registrations, booking stats, and activity trends.

## Features

- **Interactive Analytics Dashboard**:
  - Visualize user registrations, bookings, and center activity.
  - Real-time data filtering and custom charts.

- **Custom Admin Panel**:
  - Role-based management for partners and administrators.
  - Full control over centers, schedules, and user subscriptions.

- **Flexible Subscription System**:
  - Multiple subscription plans with daily, monthly, and premium visit options.
  - Track active subscriptions, remaining days, and visits.

- **Booking System**:
  - Schedule and book activities directly through the platform.
  - Manage user bookings and monitor activity.

- **User Authentication**:
  - Secure login with JWT-based API authentication.
  - Profile management for parents and children.

- **API Integration**:
  - RESTful APIs for accessing and managing data.
  - Documented with Swagger for easy third-party integration.

- **Performance Optimization**:
  - Redis caching for faster data retrieval.
  - Optimized query handling for large-scale datasets.

## Project Structure

### 1. **Users Application**
Handles user registration, authentication, and profile management.

- **Models**:
  - `Client`: Stores parent profiles.
  - `Child`: Stores children’s data.
  - `UserSubscription`: Manages subscriptions for users and children.

- **Views**:
  - `profile_view`: Displays user profiles and active subscriptions.
  - `add_child_view`: Allows parents to manage children's information.
  - `subscription_detail`: Provides detailed information on active subscriptions.

---

### 2. **Subscriptions Application**
Manages flexible subscription packages for activities.

- **Models**:
  - `Subscription`: Defines subscription plans with details like price, duration, and visit limits.
  - `AgeGroup`: Links subscription plans to specific age groups.

- **Views**:
  - `SubscriptionViewSet`: API for managing subscriptions.
  - `AgeGroupViewSet`: API for managing age groups.

---

### 3. **Centers Application**
Manages centers, activities, and bookings.

- **Models**:
  - `Center`: Represents recreational centers.
  - `Section`: Subdivisions within centers.
  - `Category`: Types of activities.
  - `Schedule`: Activity schedules.
  - `Booking`: User bookings.

- **Views**:
  - `home_view`: Displays available categories and activities.
  - `book_schedule_view`: Handles booking activities for children.
  - `user_bookings`: Displays the user’s bookings.

---

### 4. **Merchant Application**
Provides tools for partners (e.g., recreational centers).

- **Views**:
  - `manage_schedule`: Allows partners to manage schedules.
  - `add_schedule`: Partners can add new activity schedules.

---

### 5. **Analytics Application**
Provides an interactive dashboard for monitoring key metrics.

- **Features**:
  - Charts for user registrations, center activity, and bookings.
  - Top user activity analysis.

---

## Getting Started

### Prerequisites

- Python 3.12+
- Django 5.0+
- Docker (optional for deployment)
- PostgreSQL or SQLite (for database)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/balakay.git
   cd balakay
