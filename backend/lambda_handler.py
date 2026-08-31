# Import the Magnum adapter that bridges a FastAPI/FastAPI-like app
# to the AWS Lambda event/request format.
from magnum import Magnum

# Import the FastAPI application instance created in app.main.
# This is the WSGI/ASGI app that defines the API routes and handlers.
from app.main import app

# Create a Lambda-compatible handler by wrapping the app with Magnum.
# This object adapts incoming AWS Lambda events and context into the
# format expected by the application, and then converts the response
# back into the Lambda response structure.
handler = Magnum(app)