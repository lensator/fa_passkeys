fa_passkeys

fa_passkeys is a Python package designed to seamlessly integrate WebAuthn (passkey/biometric authentication) into FastAPI applications using MongoDB as the backend. It provides a robust foundation for implementing secure, passwordless authentication, along with an admin interface and comprehensive logging capabilities.

📦 Installation

Install the fa_passkeys package using pip:

```bash pip install fa_passkeys ```

🚀 Quick Start

Integrate fa_passkeys into your FastAPI application with minimal setup.

1. Initialize FastAPI Application
# main.py

```
from fastapi import FastAPI
import uvicorn
from fa_passkeys import initialize_app
from fa_passkeys.config import settings
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key)

# Define custom user fields
settings.custom_user_fields = {
    'email': (str, ...),
    'display_name': (str, None),
}

# Initialize fa_passkeys
@app.on_event("startup")
async def startup_event():
    await initialize_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

2. Configure Environment Variables
Create a .env file in your project root and define the necessary configuration:

# Database settings
DB_URI=mongodb://localhost:27017
DB_NAME=fa_passkeys_db

# WebAuthn settings
RP_NAME=YourApp
RP_ID=yourapp.com
ORIGIN=https://yourapp.com

# Logging settings
LOGGING_LEVEL=INFO
LOGGING_HANDLERS=console,file
LOGGING_FILE_PATH=fa_passkeys.log

# Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=securepassword

# Security settings
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256

# Session settings
SESSION_SECRET_KEY=your_session_secret_key
3. Run the Application
Start your FastAPI application:

uvicorn main:app --reload
🧑‍💻 Admin Interface

Access the admin interface to manage users and their credentials.

Login: Navigate to http://localhost:8000/admin/login and log in using the admin credentials defined in your .env file.
Manage Users: After logging in, you can view, inspect, and delete users via the admin dashboard.
📝 Logging

fa_passkeys includes built-in logging for monitoring authentication events and admin actions.

Configuration Options:
LOGGING_LEVEL: Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
LOGGING_HANDLERS: Define logging handlers (console, file).
LOGGING_FILE_PATH: Specify the file path for file logging.
Logs can be accessed via the console or the specified log file (fa_passkeys.log by default).

📚 Documentation

For detailed documentation, including advanced configurations and API references, please refer to the official documentation.

🤝 Contributions

Contributions are welcome! Please submit issues or pull requests to improve the package.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

