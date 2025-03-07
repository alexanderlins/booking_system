import pytest
import datetime as d
from unittest.mock import patch
import booking_system as b

# CONFIGURATION

@pytest.fixture
def sample_room():
    return b.Room("R001", "Sample", True)

@pytest.fixture
def sample_reservation(sample_room):
    start_time = d.datetime.now() + d.timedelta(days=1)
    end_time = start_time + d.timedelta(hours=2)
    return b.Reservation(sample_room, "igli2400", "RES001", start_time, end_time, 0)

# TESTS

def test_create_room():
    room = b.Room("R001", "Testing Room", True)
    assert room.room_id == "R001"
    assert room.room_name == "Testing Room"
    assert room.is_reservable is True

def test_add_room(capsys):
    b.ReservationHandler().add_room("R002", "Another Room")
    captured = capsys.readouterr()
    assert "Room added: Room(room_id='R002', room_name='Another Room', is_reservable=True)" in captured.out

def test_reservation_creation(sample_room):
    start_time = d.datetime(2024, 1, 20, 10, 0)
    end_time = d.datetime(2024, 1, 20, 12, 0)
    reservation = b.Reservation(sample_room, "user123", "RES123", start_time, end_time, 1)
    assert reservation.room == sample_room
    assert reservation.usr_id == "user123"
    assert reservation.res_id == "RES123"
    assert reservation.start_time == start_time
    assert reservation.end_time == end_time
    assert reservation.index == 1