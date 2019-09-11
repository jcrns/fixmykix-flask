# from project import app
from project import socketio, app

# Main function for file startup
if __name__ == '__main__':
	socketio.run(app, port=8000) 