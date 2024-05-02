# Real-Time Emotion Detection

This project uses a livestream or a local camera feed to perform real-time emotion detection. It uses the DeepFace and FER libraries for emotion detection and sends the results to a web client using Socket.IO.

## Prerequisites

- Python 3.6 or higher
- OpenCV
- DeepFace
- FER
- Socket.IO
- Eventlet

You can install the required Python libraries using pip:

```bash
pip install opencv-python deepface fer python-socketio eventlet
```

Running the Server
To start the server, run the following command:

```bash
python backend.py

```

Viewing the Client
Open index.html in a web browser to view the client. The client will automatically connect to the server and start displaying the camera feed with emotion detection results.
