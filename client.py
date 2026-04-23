"""
Chat Application - CLIENT
=========================
Python Project 5 (Beginner Level)

Run server.py FIRST, then run this file to join the chat.
Open multiple terminals and run client.py in each to simulate multiple users!

HOW TO RUN:
    python client.py
"""

import socket
import threading

# =============================================
#   CLIENT SETTINGS (must match server)
# =============================================
HOST = "127.0.0.1"   # Server address (localhost)
PORT = 5555           # Must match server port


# =============================================
#   RECEIVE MESSAGES IN BACKGROUND
# =============================================

def receive_messages(client_socket):
    """Continuously listen for messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(message)
            else:
                print("\n  ❌ Disconnected from server.")
                break
        except:
            print("\n  ❌ Connection to server lost.")
            break


# =============================================
#   MAIN CLIENT PROGRAM
# =============================================

def start_client():
    print("=" * 47)
    print("   💬  Chat Application - CLIENT  💬")
    print("       Python Programming - Project 5")
    print("=" * 47)
    print(f"   Connecting to server at {HOST}:{PORT}...")
    print("=" * 47)
    
    # Create socket and connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((HOST, PORT))
        print("   ✅ Connected to server!\n")
        
    except ConnectionRefusedError:
        print("\n  ❌ Could not connect to server!")
        print("  💡 Make sure server.py is running first.")
        print("     Run: python server.py\n")
        return
    
    # Wait for server to ask for name
    try:
        prompt = client_socket.recv(1024).decode("utf-8")
        if prompt == "ENTER_NAME":
            name = input("  Enter your username: ").strip()
            if not name:
                name = "Anonymous"
            client_socket.send(name.encode("utf-8"))
    except:
        print("  ❌ Error during connection setup.")
        return
    
    print()
    print("  ─────────────────────────────────────")
    print("  📋 Commands:")
    print("     /users  → See who's online")
    print("     /quit   → Leave the chat")
    print("  ─────────────────────────────────────")
    print()
    
    # Start background thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()
    
    # Main loop — send messages
    try:
        while True:
            message = input("")
            
            if not message.strip():
                continue
            
            # Send message to server
            client_socket.send(message.encode("utf-8"))
            
            # Exit if user types /quit
            if message.strip().lower() == "/quit":
                print("\n  👋 You left the chat. Goodbye!")
                break
    
    except KeyboardInterrupt:
        print("\n\n  👋 Disconnected. Goodbye!")
    
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
