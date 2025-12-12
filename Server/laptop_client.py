import socket
import time
import json
import random

# IP của Jetson khi chạy chế độ Hotspot độc lập
SERVER_IP = "10.42.0.1"
SERVER_PORT = 65432
BUFFER_SIZE = 1024

print(f"Laptop Client đang kết nối tới Jetson tại {SERVER_IP}:{SERVER_PORT}")

# Tạo socket UDP
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Đặt timeout 1 giây (để không bị treo nếu Jetson không trả lời)
client_sock.settimeout(1.0)

counter = 0

try:
    while True:
        # 1. Tạo dữ liệu giả lập (giống như ESP32 gửi lên)
        data = {
            "device": "Laptop_Client",
            "packet_id": counter,
            "sensor_value": random.randint(100, 500)  # Random giá trị cảm biến
        }
        
        # Chuyển đổi sang JSON và encode thành bytes
        message = json.dumps(data).encode('utf-8')
        
        try:
            # 2. Gửi đi
            start_time = time.time()
            client_sock.sendto(message, (SERVER_IP, SERVER_PORT))
            print(f"Đã gửi: {data}")
            
            # 3. Chờ nhận phản hồi từ Jetson
            response, addr = client_sock.recvfrom(BUFFER_SIZE)
            end_time = time.time()
            
            # Tính độ trễ (Latency)
            latency = (end_time - start_time) * 1000
            print(f"Jetson phản hồi: {response.decode('utf-8')}")
            print(f"Độ trễ (Round-trip): {latency:.2f} ms")
            
        except socket.timeout:
            print("Timeout: Không thấy Jetson trả lời")
        except Exception as e:
            print(f"Lỗi: {e}")

        counter += 1
        time.sleep(1) # Gửi mỗi 1 giây

except KeyboardInterrupt:
    print("\Đã dừng Client.")
    client_sock.close()