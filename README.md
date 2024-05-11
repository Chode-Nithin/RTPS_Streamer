# RTSP Streamer

## Overview

The RTSP Streamer is a Python-based application designed to efficiently distribute a single RTSP (Real-Time Streaming Protocol) stream to multiple client nodes with low latency. It enables simultaneous access to the RTSP stream from multiple clients or applications while maintaining high performance and robustness.

## Features

- **RTSP Stream Distribution:** The application receives an RTSP stream from a source and distributes it to connected client nodes.
- **Low Latency Transmission:** The streaming process is optimized to minimize latency, ensuring real-time delivery of the video stream.
- **Error Handling and Robustness:** Robust error handling mechanisms are implemented to gracefully manage network disruptions, client disconnections, and other potential issues.
- **Performance Optimization:** The application is optimized for performance and scalability, utilizing techniques such as multithreading, buffering, and caching to enhance streaming efficiency.
- **Real-time Metrics Display:** Latency, frames per second (FPS), and other performance metrics are displayed in real-time during the streaming process, providing insights into the streaming performance.

## How to Use

### Server Setup

1. Clone the repository to your local machine.
2. Configure the server IP address and port in the `SERVER_IP` and `SERVER_PORT` variables, respectively.
3. Ensure that the required dependencies, including OpenCV, are installed.
4. Run the server script (`rtsp_server.py`) to start the server.

### Client Setup

1. Clone the repository to your local machine.
2. Configure the server IP address and port in the `SERVER_IP` and `SERVER_PORT` variables, respectively.
3. Ensure that the required dependencies, including OpenCV, are installed.
4. Run the client script (`client.py`) to connect to the server and receive the stream.

## Key Functions

- **handle_client(client_socket, client_address):** Function to handle client connections on the server side. Manages the streaming process, error handling, and performance metrics calculation.
- **receive_stream():** Function on the client side to receive and display the stream. Handles video decoding, performance metrics calculation, and real-time display of streaming data.

## Key Points

- **Compatibility:** Ensure compatibility of the OpenCV library (`cv2`) across server and client systems to enable proper video display and decoding.
- **Error Handling:** Implement robust error handling mechanisms to gracefully manage network disruptions, client disconnections, and other potential issues.
- **Performance Optimization:** Optimize the streaming process for low latency and high FPS by employing techniques such as multithreading, buffering, and caching.
- **Real-time Metrics Display:** Display real-time metrics such as latency and FPS during the streaming process to provide insights into the performance of the application.

## Contributors

- Chode Nithin


---
