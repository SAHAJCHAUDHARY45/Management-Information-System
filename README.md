# College Management Information System (MIS)

A comprehensive Django-based college management system with student and faculty portals.

## 🔗 Registration Links

### Student Registration:
- **Landing Page**: `/students/join/` - Information page with registration link
- **Direct Registration**: `/students/register/` - Direct access to registration form

### Faculty Registration:
- **Direct Registration**: `/faculty/register/` - Faculty registration form

### How to Access Registration Links:

#### Option 1: Navigation Menu
1. Go to the home page
2. Click on "Register" in the top navigation
3. Choose "Join as Student" or "Register as Faculty"

#### Option 2: Direct URLs
- Student Registration: `http://yourdomain.com/students/join/`
- Direct Student Form: `http://yourdomain.com/students/register/`
- Faculty Registration: `http://yourdomain.com/faculty/register/`

#### Option 3: Home Page Buttons
- Click "Join as Student" button on the home page
- This takes you to the student registration landing page

## New Features Added

### Student Registration Enhancements:
- **Department Selection**: Students can now select their department during registration
- **Available Departments**:
  - Computer Science
  - Information Technology
  - Electronics & Communication
  - Mechanical Engineering
  - Civil Engineering
  - Electrical Engineering
  - Other

### Improved Navigation:
- Enhanced navigation with icons
- Clear registration links in dropdown menu
- Better visual hierarchy

### Registration Link Sharing:
- Copy-to-clipboard functionality for registration links
- Clear display of all available registration URLs
- Professional landing page for student registration

## Features
- Student and Faculty registration and authentication
- Subject and result management
- Announcement system with targeted messaging
- Dashboard for both students and faculty
- Modern, responsive UI with Bootstrap
- Department-based student organization

## Quick Start
1. Run the development server: `python manage.py runserver`
2. Access the system at: `http://localhost:8000`
3. Use the registration links to add new students and faculty
4. Share registration links with new users

## Database Migration
After adding the department field, run:
```bash
python manage.py makemigrations
python manage.py migrate
```
