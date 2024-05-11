import socket
import cv2
import numpy as np
import struct
import time

# Configuration
SERVER_IP = '192.168.0.100'
SERVER_PORT = 8000

# Socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Connected to RTSP server at {SERVER_IP}:{SERVER_PORT}")

# Performance metrics
frame_latencies = []
frame_timestamps = []

# Function to receive and display the stream
def receive_stream():
    try:
        frame_count = 0
        while True:
            # Receive the length of the frame
            frame_size_bytes = client_socket.recv(4)
            if not frame_size_bytes:
                print("End of stream")
                break
            frame_size = int.from_bytes(frame_size_bytes, byteorder='big')

            # Receive the frame data
            frame_data = b''
            while len(frame_data) < frame_size:
                packet = client_socket.recv(frame_size - len(frame_data))
                if not packet:
                    raise Exception("Error receiving frame")
                frame_data += packet

            # Receive the timestamp
            timestamp_bytes = client_socket.recv(8)
            timestamp = struct.unpack('d', timestamp_bytes)[0]

            # Convert the frame data to a NumPy array
            frame_array = np.frombuffer(frame_data, dtype=np.uint8)

            # Decode the JPEG data to a frame
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

            # Display the timestamp on the frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            cv2.putText(frame, timestamp_str, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Calculate performance metrics
            latency = time.time() - timestamp
            frame_latencies.append(latency)
            frame_timestamps.append(timestamp)
            avg_latency = sum(frame_latencies) / len(frame_latencies)
            fps = len(frame_timestamps) / (frame_timestamps[-1] - frame_timestamps[0]) if len(frame_timestamps) > 1 else 0

            # Overlay performance metrics on the frame
            cv2.putText(frame, f"Avg Latency: {avg_latency * 1000:.2f} ms", (10, 60), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 90), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Display or save the frame
            cv2.imshow('RTSP Stream', frame)
            cv2.waitKey(1)  # Adjust delay as needed for display

            # Send acknowledgment to the server
            client_socket.send(b'1')

            # Increment frame count
            frame_count += 1

    except Exception as e:
        print(f"Error receiving stream: {e}")
    finally:
        client_socket.close()
        cv2.destroyAllWindows()

# Start receiving and displaying the stream
receive_stream()