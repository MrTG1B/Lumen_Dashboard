# Lumen Dashboard

## Overview
Lumen Dashboard is a data visualization platform built using the **Lumen** micro-framework, designed for lightweight and efficient data management. It allows real-time data insights, metrics tracking, and customizable components, enabling users to monitor system activities easily.

## Features
- **Real-time Data Updates**: Displays live data from various sources.
- **Customizable Widgets**: Rearrange and configure dashboard components.
- **RESTful API Integration**: Supports API endpoints for data retrieval and manipulation.
- **Responsive Design**: Optimized for desktop and mobile use.

## Tech Stack
- **Backend**: Lumen (PHP micro-framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MySQL

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MrTG1B/Lumen_Dashboard.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Lumen_Dashboard
   ```
3. Install dependencies:
   ```bash
   composer install
   ```
4. Set up the .env file:
   Update your database credentials and other settings.
5. Run database migrations:
   ```bash
      php artisan migrate
   ```
6. Start the development server:
   ```bash
   php -S localhost:8000 -t public
   ```
## Usage
1. Open your browser and visit http://localhost:8000 to access the dashboard.
2. Customize your widgets and explore data visualizations.
3. Monitor real-time metrics and generate reports.
## Contribution
We welcome contributions! To contribute:

1. Fork this repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m 'Add feature').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request.
## License
This project is licensed under the MIT License.
