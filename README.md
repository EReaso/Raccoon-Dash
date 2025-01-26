# Raccoon Dash

Raccoon Dash is a simple Flask-based application designed to serve as a calendar display with additional features
including:

1. **Weather Widget**: Displays up-to-date weather information.
2. **Photo Screensaver**: Rotates images when the application is idle.

It supports user-friendly configuration through a dedicated endpoint and is intended to run on a screen for convenient
access.

## Endpoints

### `/display/`

- **Purpose**: Serves the main dashboard which includes the calendar view, weather widget, and photo screensaver.
- **Usage**: Open this endpoint on the desired screen for display purposes. It is designed to be minimalistic and
  visually appealing, making it ideal for a centralized calendar and widget display.

### `/`

- **Purpose**: Provides a configuration interface for the application.
- **Usage**: Allows users to configure settings such as weather location, screensaver preferences, or other customizable
  options for the display.
## Installation

Clone the repo and run the update/install script, `update.py`. When using a systemctl service, ensure the default user
can restart it. Simply run the server and open up `/display/` on the screen, and `/` to configure.

When using systemctl, the service should be called Raccoon-Dash.

## Contribution

Just make a PR! 
