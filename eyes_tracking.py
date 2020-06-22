from __future__ import division
import os
import cv2
import dlib
from eye import Eye
from calibration import Calibration

class EyesTracking(object):

    def __init__(self):
        
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()

        self._face_detector = dlib.get_frontal_face_detector()

        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def iris_located(self):
        
        try:
            int(self.eye_left.iris.x)
            int(self.eye_left.iris.y)
            int(self.eye_right.iris.x)
            int(self.eye_right.iris.y)
            
            return True
        
        except Exception:
            return False

    def _analyze(self):
        
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)
            #print(self.eye_left.iris.x)

        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):

        self.frame = frame
        self._analyze()

    def iris_left_coords(self):

        if self.iris_located:
            x = self.eye_left.origin[0] + self.eye_left.iris.x
            y = self.eye_left.origin[1] + self.eye_left.iris.y
            return (x, y)

    def iris_right_coords(self):
        
        if self.iris_located:
            x = int(self.eye_right.origin[0]) + int(self.eye_right.iris.x)
            y = int(self.eye_right.origin[1]) + int(self.eye_right.iris.y)
            return (x, y)

    def horizontal_ratio(self):
    
        if self.iris_located:
            #print("Centre of the right eye x coordinate: ", self.eye_right.iris.x)
            pupil_left = self.eye_left.iris.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.iris.x / (self.eye_right.center[0] * 2 - 10)
            #pupil_left = abs(self.eye_left.iris.x - (self.eye_left.center[0]))
            #pupil_right = abs(self.eye_right.iris.x - (self.eye_right.center[0]))
            avg = (pupil_left + pupil_right) / 2
            #print("Average: ", avg)

            return avg


    def is_right(self):
        
        if self.iris_located:
            return self.horizontal_ratio() <= 0.35 and self.vertical_ratio() > 0.35 and self.vertical_ratio() < 0.65
            #return self.horizontal_ratio() <= 1.5

    def is_left(self):
        
        if self.iris_located:
            return self.horizontal_ratio() >= 0.65 and self.vertical_ratio() > 0.35 and self.vertical_ratio() < 0.65

    def is_center(self):
        
        if self.iris_located:
            #return self.is_right() is not True and self.is_left() is not True
            return self.is_right() is not True and self.is_left() is not True and self.vertical_ratio() > 0.35 and self.vertical_ratio() < 0.65


    def vertical_ratio(self):
    
        if self.iris_located:
            pupil_left = (self.eye_left.iris.y * 2) / (self.eye_left.center[1] * 6 - 35)
            pupil_right = (self.eye_right.iris.y * 2) / (self.eye_right.center[1] * 6 - 35)
            print("Iris Y and Centre Y : ", (self.eye_left.iris.y, self.eye_left.center[1]))
            print("Vertical Ratio : ", (pupil_left + pupil_right) / 2)
            return (pupil_left + pupil_right) / 2


    def is_top(self):
        
        if self.iris_located:
            return self.vertical_ratio() <= 0.35

    def is_bottom(self):
        
        if self.iris_located:
            return self.vertical_ratio() >= 0.65


    def is_top_right(self):
        
        if self.iris_located:
            return self.vertical_ratio() <= 0.35 and self.horizontal_ratio() <= 0.35


    def is_top_left(self):
        
        if self.iris_located:
            return self.vertical_ratio() <= 0.35 and self.horizontal_ratio() >= 0.65

    
    def is_bottom_right(self):
        
        if self.iris_located:
            return self.vertical_ratio() >= 0.65 and self.horizontal_ratio() <= 0.35


    def is_bottom_left(self):
        
        if self.iris_located:
            return self.vertical_ratio() >= 0.65 and self.horizontal_ratio() >= 0.65


    def annotated_frame(self):
        
        frame = self.frame.copy()

        if self.iris_located:
            color = (0, 0, 255)
            x_left, y_left = self.iris_left_coords()
            x_right, y_right = self.iris_right_coords()
            
            cv2.circle(frame, (x_left, y_left), 10, color, 3)
            cv2.circle(frame, (x_right, y_right), 10, color, 3)

        return frame