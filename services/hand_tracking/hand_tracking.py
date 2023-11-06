import cv2
import mediapipe as mp
from numpy.typing import NDArray
from numpy import uint8


class HandTracking:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        self.keypoints_index = [5, 17, 0]
        self.hand_detector = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=1
        )
        self.detection = None

    def find_hand(self, frame: NDArray[uint8]):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.detection = self.hand_detector.process(frame_rgb)

        if self.detection.multi_hand_landmarks:
            for hand_landmark in self.detection.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmark, self.mp_hands.HAND_CONNECTIONS
                )

    def find_main_keypoint(self) -> tuple[float, float]:
        if not (self.detection.multi_hand_landmarks):
            return None
        hand_landmark = self.detection.multi_hand_landmarks[0]

        vertex = hand_landmark.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        return vertex.x, vertex.y
