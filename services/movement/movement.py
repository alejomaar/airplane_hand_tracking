from datetime import datetime
import numpy as np
from collections import deque


class Movement:
    MAX_LENGTH_QUEUES = 3
    DENOISE_KERNEL = np.array([0.18, 0.32, 0.5])

    def __init__(self):
        self.position = deque([0, 0, 0], self.MAX_LENGTH_QUEUES)
        self.velocity = deque([0, 0, 0], self.MAX_LENGTH_QUEUES)
        self.time = deque(
            [datetime.now(), datetime.now(), datetime.now()], self.MAX_LENGTH_QUEUES
        )
        self.iter = 0

    def update_dynamics(self, position: float) -> None:
        self.position.append(position)
        self.time.append(datetime.now())
        self.velocity.append(self.calculate_velocity())
        self.iter = self.iter + 1

    def calculate_velocity(self) -> float:
        return (self.position[0] - self.position[1]) / (
            self.time[0] - self.time[1]
        ).total_seconds()

    @property
    def denoised_velocity(self) -> tuple[float, float]:
        if self.iter < 3:
            return (0, 0)
        return self.DENOISE_KERNEL @ np.array(list(self.velocity))
