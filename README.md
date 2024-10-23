#Balakay

Balakay is a Django-based web application designed for parents to manage their profiles, children’s information, and recreational activity subscriptions. With a user-friendly interface, Balakay simplifies scheduling, booking, and tracking activities for parents and recreational centers. The platform provides a seamless experience for managing both parent and child profiles, as well as activity subscriptions.
Table of Contents

    Introduction
    Features
    Project Structure
    Getting Started
        Prerequisites
        Installation
    Usage
    Built With
    Authors

Introduction

Balakay offers a comprehensive solution for parents to manage their children’s activity subscriptions and bookings. It provides an efficient way to handle recreational schedules, browse available centers, and track bookings. Administrators can also leverage Django's built-in admin interface to manage users, subscriptions, and activities.
Core Modules:

    Users Management: Parents can register, log in, and update their profiles.
    Child Management: Parents can add and manage children's information, including name, birthdate, and gender.
    Activity Subscription and Booking: Subscribe to activities for children, book schedules, and track usage.
    Admin Interface: Manage users, subscriptions, and activities with Django's admin tools.

Features

    User Registration and Authentication: Parents can sign up, log in, update their profiles, and manage child-related activities.
    Child Management: Parents can easily manage their children's information (name, birthdate, gender).
    Activity Subscription: Subscribe to children's recreational activities, track usage, and manage subscription details.
    Booking System: Browse available centers, book activities, and manage bookings.
    Admin Control: Full admin control over users, subscriptions, and center schedules via the Django admin interface.

Project Structure
1. Users Application

This application handles user management, including client registration, login, profile management, and child information.
Models:

    Client: Parent profiles.
    Child: Stores children’s data.
    UserSubscription: Manages activity subscriptions for users.

Views:

    register_client: Handles user registration.
    login_user: User login view.
    logout_user: Logs the user out.
    profile_view: Displays user profiles.
    add_child_view: Manages children’s data.

Forms:

    ClientRegistrationForm: For new user registration.
    ChildForm: Allows parents to add children to their profiles.

2. Subscriptions Application

This handles subscription management for activities.
Model:

    Subscription: Stores details about subscription packages (name, price, duration, age group).

3. Centers Application

This module manages centers, schedules, and activity bookings.
Models:

    Center: Represents recreational centers.
    Section: Subdivisions of centers.
    Category: Types of activities.
    Schedule: Holds activity schedules.
    Booking: Manages user bookings.

Views:

    home_view: Displays the homepage with available categories.
    section_view: Shows details about a center's sections.
    book_schedule_view: Handles activity bookings.
    center_list_view: Lists available centers.
    user_bookings: Displays bookings made by the user.

Getting Started
Prerequisites

    Python 3.12+
    Django 5.0+

Usage

    Register: Create a parent account.
    Add Children: After logging in, add your children's details.
    Browse Centers: Explore the list of available centers and their schedules.
    Book Activities: Select activities and book schedules for your children.
    Manage Profile: Update your profile or child’s information anytime.
    Track Subscriptions: View and track activity subscriptions and their usage.

Built With

    Django — The web framework for rapid development.
    Bootstrap — For responsive design.
    HTML — Frontend development.
