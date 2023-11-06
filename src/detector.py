import cv2
import mediapipe as mp
import numpy as np     
     
     
class HandDetector():
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands 

        self.keypoints_index = [5,17,0]
        self.hand_detector = self.mp_hands.Hands( static_image_mode = False,  max_num_hands = 1)
        self.detection = None
        
    def find_hand(self,frame):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.detection = self.hand_detector.process(frame_rgb)
        
        if(self.detection.multi_hand_landmarks):
            for hand_landmark in self.detection.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame,hand_landmark,self.mp_hands.HAND_CONNECTIONS)
                
        return frame
                
    def find_main_keypoint(self,frame,screen_coordinates=True):
        if not (self.detection.multi_hand_landmarks):
            return None
        hand_landmark = self.detection.multi_hand_landmarks[0]
        
        vertex = hand_landmark.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        if(screen_coordinates):
            height,width,_ = frame.shape 
            return np.array([vertex.x* width,vertex.y* height])
        return np.array([vertex.x,vertex.y])