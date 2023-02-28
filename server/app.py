if __name__ == '__main__':
    from api.application import create_app, create_socket
    app = create_app()
    socketio = create_socket(app)
    socketio.run(app)