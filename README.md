# Flask Workshop

A hands-on workshop for learning the fundamentals of Flask, a lightweight Python web framework for building web applications and APIs.

## Overview

This project is designed to help participants:

- understand the Flask application lifecycle
- create routes and render templates
- work with forms and request data
- connect to a database
- build and test a small web app

## Prerequisites

Before starting, make sure you have:

- Python 3.9+
- pip
- a virtual environment tool such as venv
- a code editor like VS Code or PyCharm

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd flask_workshop
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```text
flask_workshop/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   └── static/
├── tests/
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

## Common Workshop Topics

- Basic route creation
- URL parameters and query strings
- Jinja templates
- Forms and validation
- Handling GET and POST requests
- Session and flash messages
- Database integration with SQLite or PostgreSQL
- API development with JSON responses

## Running the App

Start the development server:

```bash
python run.py
```

Then open your browser and visit:

```text
http://localhost:5000
```

## Development Notes

- Use environment variables for configuration secrets.
- Keep app logic separated from route definitions when possible.
- Write tests for key behaviors and edge cases.
- Follow Flask best practices for app structure and modularity.

## License

This project is intended for educational use.

## Contributing

Contributions, fixes, and suggestions are welcome. If you want to improve the workshop, open a pull request or share your ideas.
