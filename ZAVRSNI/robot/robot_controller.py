from enum import Enum
import socket
from typing import Optional
from dataclasses import dataclass

BUFFER_SIZE = 9
DESTINATION = tuple[str, int]


class Master(Enum):
    MASTER = (11).to_bytes(1, 'big', signed=False)


class Slaves(Enum):
    SLAVE1 = (21).to_bytes(1, 'big', signed=False)


class PacketType(Enum):
    GET_CALIBRATED_SPEEDS = (1).to_bytes(1, 'big', signed=False)
    GET_LINE_POSITION = (2).to_bytes(1, 'big', signed=False)
    SET_WHEEL_SPEED_AND_DIRECTION = (3).to_bytes(1, 'big', signed=False)
    RESPONSE_CALIBRATED_WHEEL_SPEEDS = (4).to_bytes(1, 'big', signed=False)
    RESPONSE_LINE_POSITION = (5).to_bytes(1, 'big', signed=False)
    GET_STATUS = (6).to_bytes(1, 'big', signed=False)
    RESPONSE_RUNNING = (7).to_bytes(1, 'big', signed=False)
    RESPONSE_STOPPED = (8).to_bytes(1, 'big', signed=False)


class RobotStates(Enum):
    STOP = 1 << 0
    FORWARD = 1 << 1
    LEFT1 = 1 << 2
    LEFT2 = 1 << 3
    LEFT3 = 1 << 4
    RIGHT1 = 1 << 5
    RIGHT2 = 1 << 6
    RIGHT3 = 1 << 7
    STOPPED = 1 << 8
    RUNNING = 1 << 9


@dataclass(frozen=True)
class RGB:
    red: int = 0
    green: int = 0
    blue: int = 0

    def to_bytes(self) -> bytes:
        rgb = \
            (self.red << 16) | \
            (self.green << 8) | \
            self.blue

        return rgb.to_bytes(3, 'big')


@dataclass(frozen=True)
class WheelsSpeeds:
    leftSlow: int
    rightSlow: int
    leftNormal: int
    rightNormal: int
    leftFast: int
    rightFast: int


@dataclass(frozen=True)
class ReceivedPacket:
    packed_type: PacketType
    device_id: int
    value: bytes


@dataclass(frozen=True)
class WheelSpeedAndDirection:
    left_direction: int
    left_speed: int
    right_direction: int
    right_speed: int

    def to_bytes(self) -> bytes:
        return \
            self.left_direction.to_bytes(1, 'big') + \
            self.left_speed.to_bytes(1, 'big') + \
            self.right_direction.to_bytes(1, 'big') + \
            self.right_speed.to_bytes(1, 'big')


def packet_builder(packet_type: PacketType, device_id: bytes, value: Optional[bytes] = b'') -> bytes:
    packet = packet_type.value + device_id + value
    packet += bytes(BUFFER_SIZE - len(packet))
    return packet


def send_packet(packet: bytes, destination: DESTINATION) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(packet, destination)


def is_packet_type_valid(packet_type: int) -> bool:
    try:
        PacketType(packet_type)
        return True
    except ValueError:
        return False


def receive_packet(buffer_size) -> Optional[ReceivedPacket]:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        packet = s.recvfrom(buffer_size)[0]

        if not is_packet_type_valid(packet[0]):
            return None

        return ReceivedPacket(PacketType(packet[0]), packet[1], packet[2:])


def is_device_id_valid(device_id: int) -> bool:
    try:
        Slaves(device_id)
        return True
    except ValueError:
        return False


def get_response(
        packet_type: PacketType,
        device_id: bytes,
        value: bytes,
        destination: DESTINATION,
        buffer_size: Optional[int] = BUFFER_SIZE
) -> Optional[ReceivedPacket]:
    packet = packet_builder(packet_type.value, device_id, value)

    send_packet(packet, destination)

    response = receive_packet(buffer_size)

    if not is_device_id_valid(response.device_id):
        return None

    return response


def get_calibrated_speeds(
        device_id: bytes,
        destination: DESTINATION,
        buffer_size: Optional[int] = BUFFER_SIZE
) -> Optional[WheelsSpeeds]:
    response = get_response(PacketType.GET_CALIBRATED_SPEEDS, device_id, b'', destination, buffer_size)

    if not response or response.packed_type != PacketType.GET_CALIBRATED_SPEEDS:
        return None

    return WheelsSpeeds(*response.value)


def get_line_position(
        device_id: bytes,
        destination: DESTINATION,
        buffer_size: Optional[int] = BUFFER_SIZE
) -> Optional[int]:
    response = get_response(PacketType.RESPONSE_LINE_POSITION, device_id, b'', destination, buffer_size)

    if not response or response.packed_type != PacketType.RESPONSE_LINE_POSITION:
        return None

    return int.from_bytes(response.value, 'big', signed=False)


def set_wheel_speed(
        wheels_direction_and_speed: bytes,
        rgb: bytes,
        device_id: bytes,
        destination: DESTINATION
) -> None:
    packet = packet_builder(
        PacketType.SET_WHEEL_SPEED_AND_DIRECTION,
        device_id,
        wheels_direction_and_speed + rgb
    )

    send_packet(packet, destination)


def get_slave_status(
        device_id: bytes,
        destination: DESTINATION,
        buffer_size: int = BUFFER_SIZE
) -> Optional[bool]:
    response = get_response(PacketType.GET_STATUS, device_id, b'', destination, buffer_size)

    if not response:
        return None

    if response.packed_type == PacketType.RESPONSE_RUNNING:
        return True

    if response.packed_type == PacketType.RESPONSE_STOPPED:
        return False


def decide_next_state(line_position: int) -> RobotStates:
    if 0 < line_position <= 1000:
        return RobotStates.LEFT1
    elif 1000 < line_position <= 2000:
        return RobotStates.LEFT2
    elif 2000 < line_position <= 3000:
        return RobotStates.LEFT3
    elif line_position > 6000:
        return RobotStates.RIGHT1
    elif line_position > 5000:
        return RobotStates.RIGHT2
    elif line_position > 4000:
        return RobotStates.RIGHT3
    elif 3000 < line_position <= 4000:
        return RobotStates.FORWARD
    else:
        return RobotStates.STOP


def wheel_settings_and_rgb(current_state: RobotStates, calibrated_speeds: WheelsSpeeds) -> tuple[WheelSpeedAndDirection, RGB]:
    to_send_speed_and_direction = WheelSpeedAndDirection(0, 0, 0, 0)
    to_send_rgb = RGB(255, 0, 0)

    match current_state:
        case RobotStates.STOP:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, 0, 0, 0)
            to_send_rgb = RGB(255, 0, 0)
        case RobotStates.FORWARD:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, calibrated_speeds.leftFast, 0, calibrated_speeds.rightFast)
            to_send_rgb = RGB(0, 255, 0)
        case RobotStates.LEFT1:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, 0, 0, calibrated_speeds.rightFast)
            to_send_rgb = RGB(255, 255, 0)
        case RobotStates.LEFT2:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, calibrated_speeds.leftSlow, 0, calibrated_speeds.rightFast)
            to_send_rgb = RGB(127, 255, 0)
        case RobotStates.LEFT3:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, calibrated_speeds.leftNormal, 0, calibrated_speeds.rightFast)
            to_send_rgb = RGB(63, 255, 0)
        case RobotStates.RIGHT1:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, calibrated_speeds.leftFast, 0, 0)
            to_send_rgb = RGB(0, 255, 255)
        case RobotStates.RIGHT2:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, calibrated_speeds.leftFast, 0, calibrated_speeds.rightSlow)
            to_send_rgb = RGB(0, 255, 127)
        case RobotStates.RIGHT3:
            to_send_speed_and_direction = \
                WheelSpeedAndDirection(0, calibrated_speeds.leftFast, 0, calibrated_speeds.rightNormal)
            to_send_rgb = RGB(0, 255, 63)

    return to_send_speed_and_direction, to_send_rgb


def main():
    destination: DESTINATION = ('192.168.1.1', 2390)

    previous_state = None
    current_state = RobotStates.STOP
    next_state = RobotStates.STOP

    robot_state = RobotStates.RUNNING

    calibrated_speeds = get_calibrated_speeds(Master.MASTER.value, destination, BUFFER_SIZE)

    while True:
        slave_status = get_slave_status(Master.MASTER.value, destination, BUFFER_SIZE)

        if slave_status is None:
            continue

        if slave_status:
            robot_state = RobotStates.RUNNING
        else:
            robot_state = RobotStates.STOPPED

        line_position = get_line_position(Master.MASTER.value, destination, BUFFER_SIZE)

        if robot_state == RobotStates.RUNNING:
            next_state = decide_next_state(line_position)

        previous_state = current_state
        current_state = next_state

        to_send_speed_and_direction, to_send_rgb = wheel_settings_and_rgb(current_state, calibrated_speeds)

        set_wheel_speed(
            to_send_speed_and_direction.to_bytes(),
            to_send_rgb.to_bytes(),
            Master.MASTER.value,
            destination
        )
