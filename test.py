import cv2
import pytest

# Test if the gun cascade classifier loads successfully
def test_gun_cascade_classifier():
    gun_cascade = cv2.CascadeClassifier('C:/Users/Ramsha/Downloads/gun/cascade.xml')
    assert not gun_cascade.empty()

# Test if the video capture initializes successfully
def test_video_capture():
    camera = cv2.VideoCapture('C:/Users/Ramsha/Downloads/gun/gg2.mp4')
    assert camera.isOpened()

# Test the main gun detection loop
def test_gun_detection():
    gun_cascade = cv2.CascadeClassifier('C:/Users/Ramsha/Downloads/gun/cascade.xml')
    camera = cv2.VideoCapture('C:/Users/Ramsha/Downloads/gun/gg2.mp4')

    firstFrame = None
    gun_exist = False
    gun_count = 0
    detected_frames = []

    while True:
        ret, frame = camera.read()

        if not ret:
            break

        # Perform your gun detection logic here

        # Add your assertions to test the gun detection

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

# Run the tests
if __name__ == '__main__':
    pytest.main(['-v', 'test_gun_detection.py'])
