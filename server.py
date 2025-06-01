import socket
import threading
import db

HOST = '127.0.0.1'
PORT = 9090

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
        data = conn.recv(1024).decode()
        if not data:
            return
        parts = data.strip().split("|")
        command = parts[0]

        if command == "REGISTER":
            username, password = parts[1], parts[2]
            result = db.register_user(username, password)
            conn.sendall(result.encode())

        elif command == "LOGIN":
            username, password = parts[1], parts[2]
            user_id = db.login_user(username, password)
            conn.sendall(str(user_id).encode())

        elif command == "ADD_HABIT":
            user_id, habit_name = parts[1], parts[2]
            result = db.add_habit(user_id, habit_name)
            conn.sendall(result.encode())

        elif command == "GET_HABITS":
            user_id = parts[1]
            habits = db.get_habits(user_id)
            if habits:
                result = "HABITS|" + "|".join([f"{h[0]}: {h[1]}" for h in habits])
            else:
                result = "HABITS|"
            conn.sendall(result.encode())

        elif command == "MARK_DONE":
            habit_id = parts[1]
            result = db.mark_habit_done(habit_id)
            conn.sendall(result.encode())

        elif command == "GET_STATS":
            habit_id = parts[1]
            stats = db.get_habit_stats(habit_id)
            conn.sendall(stats.encode())
        
        elif command == "CHANGE_HABIT":
            habit_id, new_name = parts[1], parts[2]
            result = db.change_habit(habit_id, new_name)
            conn.sendall(result.encode())

        elif command == "DELETE_HABIT":
            habit_id = parts[1]
            result = db.delete_habit(habit_id)
            conn.sendall(result.encode())

        else:
            conn.sendall("UNKNOWN_COMMAND".encode())

    except Exception as e:
        print(f"[ERROR] {e}")
        conn.sendall("ERROR".encode())
    finally:
        conn.close()

def start_server():
    print(f"[STARTING] Server is starting on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[LISTENING] Server is running on {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
