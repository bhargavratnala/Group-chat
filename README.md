# Group-chat
Flask web application for group chat with personal rooms

Python integrated with JavaScript to send and receive messages using WebSockets.

This project leverages Flask-SocketIO to handle real-time communication between the server and clients. WebSockets provide a persistent connection between the client and server, allowing for instant message delivery without the need for constant polling.

Name of the user should be entered first and then there are two options:
1. Create room
2. Enter existing room

## Getting Start

To get started with Group-chat applicatio

1. Clone the repository:
    ```sh
    git clone https://github.com/bhargavratnala/Group-chat.git
    ```
2. Getting Started:
    ```sh
    cd Group-chat
    ```
3. start server
    ```sh
    python server.py
    ```
4. run client
    ````sh
    python client.py
    ```
    open `localhost:9999` in browser

The user can click "Create room" to create a new room.

They can click "Enter existing room" to join a room by entering the room code.
