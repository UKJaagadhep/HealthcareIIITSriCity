import socket
import json
import time

class notifyEmerg():
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) 
            local_ip = s.getsockname()[0] 
            s.close()
            return local_ip
        except Exception as e:
            print(f"Error getting local IP: {e}")
            return None

    def notify_emergency(self):
        try:
            room_ip = self.get_local_ip()
            print(room_ip)
            if not room_ip:
                return print("Unable to retrieve local IP. Exiting.")
            
            room_port = 8082  
            
            central_server_ip = '10.2.1.192'
            central_server_port = 8081 
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((central_server_ip, central_server_port))
            
            emergency_data = {
                'room_ip': room_ip,  
                'room_port': room_port,  
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S") 
            }
            
            emergency_message = json.dumps(emergency_data)
            
            client_socket.send(emergency_message.encode('utf-8'))
            
            client_socket.close()
            
            return print(f"Emergency notification sent from room {room_ip}:{room_port} at {emergency_data['timestamp']}")
        
        except Exception as e:
            return print("Failed to send emergency notification: {e}")



