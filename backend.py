import cv2  # Importing the OpenCV library for image processing
import base64  # Importing the base64 library for encoding and decoding data
import numpy as np  # Importing the NumPy library for numerical operations
import socketio  # Importing the Socket.IO library for real-time communication
import eventlet  # Importing the Eventlet library for concurrent programming
from deepface import DeepFace  # Importing the DeepFace library for facial analysis
from fer import FER  # Importing the FER library for facial emotion recognition

#cap = cv2.VideoCapture('your-stream-url')  # Replace with your livestream URL
sio = socketio.Server(cors_allowed_origins="http://127.0.0.1:5500")  # Creating a Socket.IO server instance
detector = FER(mtcnn=True)  # Creating an instance of the FER detector

def numpy_to_list(data):
    if isinstance(data, np.ndarray):  # Checking if the data is a NumPy array
        return data.tolist()  # Converting the NumPy array to a Python list
    elif isinstance(data, list):  # Checking if the data is already a list
        return data  # Returning the data as it is
    else:
        return data  # Returning the data as it is

@sio.on('connect')  # Decorator to handle the 'connect' event
def connect(sid, environ):
    print('connect ', sid)  # Printing a message when a client connects

@sio.on('frame')  # Decorator to handle the 'frame' event
def process_frame(sid, data):
    frame_data = base64.b64decode(data.split(',')[1])  # Decoding the base64 encoded frame data
    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)  # Decoding the image data and converting it to a NumPy array

    df_result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)  # Analyzing the facial emotions using DeepFace
    emotion_result = detector.detect_emotions(frame)  # Detecting emotions in the frame using FER

    frame_bytes = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()  # Encoding the frame as a JPEG image and converting it to bytes

    # Split the frame_bytes into chunks of size 1000
    chunks = [frame_bytes[i:i+1000] for i in range(0, len(frame_bytes), 1000)]

    for i, chunk in enumerate(chunks):
        sio.emit('frame_results', {'frame': chunk, 'deepface': df_result, 'emotion': emotion_result, 'chunk_index': i, 'total_chunks': len(chunks)})  # Emitting the frame results to the client

app = socketio.WSGIApp(sio)  # Creating a WSGI application using the Socket.IO server

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)  # Starting the server on port 5000