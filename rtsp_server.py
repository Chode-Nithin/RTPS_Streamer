import socket
import threading
import cv2
import numpy as np
import time
import struct
import traceback
from collections import deque

# Configuration
SERVER_IP = '192.168.0.100'
SERVER_PORT = 8000
VIDEO_FILE = 'video.mp4'
BUFFER_SIZE = 10  # Buffer size for performance calculation

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)
print(f"RTSP server listening on {SERVER_IP}:{SERVER_PORT}")

# Performance metrics
frame_timestamps = deque(maxlen=BUFFER_SIZE)
frame_latencies = deque(maxlen=BUFFER_SIZE)

# Function to handle client connections
def handle_client(client_socket, client_address):
    try:
        print(f"New client connected: {client_address}")
        video_capture = cv2.VideoCapture(VIDEO_FILE)
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("End of video stream")
                break
            # Record the timestamp when the frame is captured
            capture_timestamp = time.time()
            # Convert the frame to JPEG format
            ret, jpeg_frame = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error encoding frame as JPEG")
                break
            # Send the length of the frame followed by the frame itself
            frame_size = len(jpeg_frame)
            client_socket.sendall(frame_size.to_bytes(4, byteorder='big'))
            client_socket.sendall(jpeg_frame)
            # Send the timestamp along with the frame
            timestamp_bytes = struct.pack('d', capture_timestamp)
            client_socket.sendall(timestamp_bytes)
            print(f"Frame transmitted to {client_address}")
            # Wait for acknowledgment from the client
            ack = client_socket.recv(1)
            if ack:
                # Calculate latency
                receive_timestamp = time.time()
                latency = receive_timestamp - capture_timestamp
                frame_latencies.append(latency)
                frame_timestamps.append(capture_timestamp)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
        traceback.print_exc()
    finally:
        print(f"Client {client_address} disconnected")
        client_socket.close()
        video_capture.release()
        # Calculate performance and scalability metrics
        avg_latency = sum(frame_latencies) / len(frame_latencies) if frame_latencies else 0
        fps = len(frame_timestamps) / (frame_timestamps[-1] - frame_timestamps[0]) if len(frame_timestamps) > 1 else 0
        print(f"Average latency: {avg_latency * 1000:.2f} ms")
        print(f"Frames per second: {fps:.2f}")

# Main server loop
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()