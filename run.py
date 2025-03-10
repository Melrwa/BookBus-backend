from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Get the port from the environment variable (required for Render)
    port = int(os.getenv("PORT", 5000))
    
    @app.route('/')
    def hello():
        return "This Server is running"
    
    # Run the app with debug mode explicitly enabled
    app.run(host="0.0.0.0", port=port, debug=True)