import cv2
from eyes_tracking import EyesTracking

eyes = EyesTracking()
webcam = cv2.VideoCapture(0)

while True:
    
    _, frame = webcam.read()

    eyes.refresh(frame)

    frame = eyes.annotated_frame()
    text = ""

    if eyes.is_top_left():
        text = "Looking Top Left"
    
    elif eyes.is_top_right():
        text = "Looking Top Right"
    
    elif eyes.is_bottom_left():
        text = "Looking Bottom Left"
    
    elif eyes.is_bottom_right():
        text = "Looking Bottom Right"
    
    elif eyes.is_right():
        text = "Looking Right"
    
    elif eyes.is_left():
        text = "Looking Left"
    
    elif eyes.is_center():
        text = "Looking Center"
    
    elif eyes.is_top():
        text = "Looking Top"
    
    elif eyes.is_bottom():
        text = "Looking Bottom"

    cv2.putText(frame, text, (90, 360), cv2.FONT_HERSHEY_TRIPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = eyes.iris_left_coords()
    right_pupil = eyes.iris_right_coords()
    
    cv2.putText(frame, "Left Iris:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_TRIPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right Iris: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_TRIPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Track", frame)

    if cv2.waitKey(1) == 27 & 0xFF == ord('q'):
        break
