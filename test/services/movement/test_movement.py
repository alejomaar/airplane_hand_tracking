import pytest
from services.movement import Movement
import time
from datetime import datetime
from unittest.mock import patch


@pytest.fixture
def movement():
    movement = Movement()
    time.sleep(0.01)
    return movement


def test_initialization(movement):
    assert len(movement.position) == Movement.MAX_LENGTH_QUEUES
    assert len(movement.velocity) == Movement.MAX_LENGTH_QUEUES
    assert len(movement.time) == Movement.MAX_LENGTH_QUEUES
    assert movement.iter == 0


def test_update_dynamics(movement: Movement):
    movement.update_dynamics(1.0)
    assert movement.iter == 1
    assert movement.position[0] == pytest.approx(1)
    assert movement.velocity[0] != 0


def test_calculate_velocity(movement: Movement):
    with patch("services.movement.movement.datetime") as mock_datetime:
        mock_datetime.now.side_effect = [
            datetime(2023, 12, 10, 1, 1, 4),
            datetime(2023, 12, 10, 1, 1, 5),
            datetime(2023, 12, 10, 1, 1, 7)
        ]

        movement.update_dynamics(1.0)
        movement.update_dynamics(4.0)
        movement.update_dynamics(8.0)

    assert movement.velocity[0] == pytest.approx(2)
    assert movement.velocity[1] == pytest.approx(3)
    
def test_denoised_velocity_none(movement: Movement):
    with patch("services.movement.movement.datetime") as mock_datetime:
        mock_datetime.now.side_effect = [
            datetime(2023, 12, 10, 1, 1, 4),
            datetime(2023, 12, 10, 1, 1, 5),
        ]
        movement.update_dynamics(1.0)
        movement.update_dynamics(2.0)
    denoised_velocity = movement.denoised_velocity
    assert denoised_velocity is None  



def test_denoised_velocity_exist(movement: Movement):
    with patch("services.movement.movement.datetime") as mock_datetime:
        mock_datetime.now.side_effect = [
            datetime(2023, 12, 10, 1, 1, 4),
            datetime(2023, 12, 10, 1, 1, 5),
            datetime(2023, 12, 10, 1, 1, 6),
             datetime(2023, 12, 10, 1, 1, 7)
        ]
    
        movement.update_dynamics(0)
        movement.update_dynamics(1.0)
        movement.update_dynamics(2.0)
        movement.update_dynamics(4.0)
        
    assert movement.denoised_velocity is not None  
    assert movement.denoised_velocity == pytest.approx(1.5)
