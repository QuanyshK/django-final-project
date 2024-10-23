Balakay: Parent and Child Activity Management System
Balakay is a Django-based web application designed for parents to manage their profiles, children's information, and recreational activity subscriptions. It allows users to register, log in, manage their children's details, book activities, and track subscriptions. The platform is built to simplify managing schedules, bookings, and activities for parents and recreational centers.

Features
User Registration and Authentication: Parents can sign up, log in, and update their profiles.
Child Management: Parents can add and manage their children's information (name, birthdate, gender).
Activity Subscription: Parents can subscribe to activities for their children, track usage, and monitor subscription details.
Booking System: Users can browse centers, book schedules, and view their bookings.
Admin Interface: Django's admin interface is available for managing users, subscriptions, and activities.
Project Structure
1. Users Application
The Users Application handles user management, including:

Models: Client, Child, UserSubscription.
Views:
register_client: Handles user registration.
login_user: User login view.
logout_user: Logs the user out.
profile_view: Displays the user's profile.
update_profile: Allows users to update their profile information.
add_child_view: Handles adding children to a user's profile.
Forms:
ClientRegistrationForm: Used for user registration.
UserLoginForm: Handles user authentication.
UserUpdateForm: Updates user information.
ClientUpdateForm: Updates client (parent) details.
ChildForm: Adds a child to a parent's profile.
2. Subscriptions Application
The Subscriptions Application manages activity subscriptions:

Model: Subscription.
Fields:
name: Name of the subscription.
price: Price of the subscription.
active: Active status of the subscription.
duration: Length of the subscription.
age_group: Target age group for the subscription.
3. Centers Application
The Centers Application manages recreational centers, schedules, and bookings:

Models:
Center: Represents a recreational center.
Section: Subdivisions of a center.
Category: Categories of activities.
Schedule: Timetables for activities.
Booking: User bookings for activities.
Views:
home_view: Displays the homepage with categories.
section_view: Displays details of a specific section and its schedules.
book_schedule_view: Handles booking a schedule for a child.
booking_success_view: Displays a success message after booking.
center_list_view: Displays a searchable list of centers.
center_details: Shows center details and its schedules.
user_bookings: Displays a list of bookings made by the user.
cancel_booking_view: Handles booking cancellations.
booking_detail: Displays and manages details of a specific booking.
Form:
BookingForm: Used for booking activities for children.
Installation
Clone the repository:
bash
Копировать код
git clone https://github.com/yourusername/balakay.git
Install dependencies:
bash
Копировать код
pip install -r requirements.txt
Apply migrations:
bash
Копировать код
python manage.py migrate
Run the server:
bash
Копировать код
python manage.py runserver
Usage
Register: Create a parent account.
Add Children: After registration, log in and add details for your children.
Browse Centers: Search through available centers and their activity schedules.
Book Activities: Choose an activity and book a schedule for your child.
Manage Profile: Update your profile or child details as needed.
Track Subscriptions: View and track your child’s activity subscriptions and usage.
