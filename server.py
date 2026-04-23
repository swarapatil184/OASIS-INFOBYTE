"""
Chat Application - SERVER
=========================
Python Project 5 (Beginner Level)

Run this file FIRST on one terminal window.
Then run client.py in other terminal windows to connect.

HOW TO RUN:
    python server.py
"""

import socket
import threading
import datetime

# =============================================
#   SERVER SETTINGS
# =============================================
HOST = "127.0.0.1"   # Localhost (your own computer)
PORT = 5555           # Port number to listen on
MAX_CLIENTS = 10      # Maximum number of users allowed

# Store connected clients and their names
clients = []   # list of (socket, name)


# =============================================
#   HELPER FUNCTIONS
# =============================================

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")


def broadcast(message, sender_socket=None):
    """Send a message to ALL connected clients except the sender."""
    for client_socket, name in clients[:]:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                remove_client(client_socket)


def broadcast_all(message):
    """Send a message to ALL connected clients including sender."""
    for client_socket, name in clients[:]:
        try:
            client_socket.send(message.encode("utf-8"))
        except:
            remove_client(client_socket)


def remove_client(client_socket):
    """Remove a disconnected client from the list."""
    for item in clients[:]:
        if item[0] == client_socket:
            clients.remove(item)
            client_socket.close()
            return item[1]  # Return the name
    return "Unknown"


def get_name(client_socket):
    """Get the name of a client by their socket."""
    for sock, name in clients:
        if sock == client_socket:
            return name
    return "Unknown"


# =============================================
#   HANDLE EACH CLIENT IN A THREAD
# =============================================

def handle_client(client_socket, address):
    """Handle communication with a single client."""
    
    print(f"[{timestamp()}] New connection from {address}")
    
    try:
        # Ask for username
        client_socket.send("ENTER_NAME".encode("utf-8"))
        name = client_socket.recv(1024).decode("utf-8").strip()
        
        if not name:
            name = f"User{len(clients)+1}"
        
        # Add to client list
        clients.append((client_socket, name))
        
        print(f"[{timestamp()}] {name} joined the chat. ({len(clients)} users online)")
        
        # Announce to everyone
        broadcast_all(f"\n  📢 [{timestamp()}] {name} joined the chat! 👋")
        broadcast_all(f"  👥 Users online: {len(clients)}\n")
        
        # Send welcome message to the new user
        client_socket.send(f"\n  ✅ Welcome to the chat, {name}!".encode("utf-8"))
        client_socket.send(f"\n  💡 Type your message and press Enter to send.".encode("utf-8"))
        client_socket.send(f"\n  💡 Type '/quit' to leave the chat.\n".encode("utf-8"))
        
        # Listen for messages from this client
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                
                if not message:
                    break
                
                # Handle quit command
                if message.strip().lower() == "/quit":
                    break
                
                # Handle list users command
                elif message.strip().lower() == "/users":
                    user_list = ", ".join([n for _, n in clients])
                    client_socket.send(f"\n  👥 Online users: {user_list}\n".encode("utf-8"))
                
                # Regular message — broadcast to others
                else:
                    formatted = f"\n  💬 [{timestamp()}] {name}: {message}"
                    print(formatted)
                    broadcast(formatted, sender_socket=client_socket)
                    # Confirm to sender
                    client_socket.send(f"  ✅ (sent)\n".encode("utf-8"))
                    
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Error with {name}: {e}")
                break
    
    except Exception as e:
        print(f"[{timestamp()}] Error: {e}")
    
    finally:
        # Client disconnected
        removed_name = remove_client(client_socket)
        print(f"[{timestamp()}] {removed_name} left the chat. ({len(clients)} users online)")
        broadcast_all(f"\n  📢 [{timestamp()}] {removed_name} left the chat. 👋\n")


# =============================================
#   START THE SERVER
# =============================================

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(MAX_CLIENTS)
        
        print("=" * 47)
        print("   💬  Chat Application - SERVER  💬")
        print("       Python Programming - Project 5")
        print("=" * 47)
        print(f"   ✅ Server started on {HOST}:{PORT}")
        print(f"   ✅ Waiting for clients to connect...")
        print(f"   💡 Press Ctrl+C to stop the server.")
        print("=" * 47)
        print()
        
        while True:
            client_socket, address = server.accept()
            # Start a new thread for each client
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.daemon = True
            thread.start()
    
    except KeyboardInterrupt:
        print("\n\n[Server] Shutting down...")
        broadcast_all("\n  📢 Server is shutting down. Goodbye!\n")
    
    finally:
        server.close()
        print("[Server] Closed.")


if __name__ == "__main__":
    start_server()
