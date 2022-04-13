from enum import Enum
import socket
from typing import Optional
from dataclasses import dataclass

BUFFER_SIZE = 8
DESTINATION = tuple[str, int]


class Slaves(Enum):
    SLAVE1 = int(21).to_bytes(1, 'big', signed=False)


class PacketType(Enum):
    GET_CALIBRATED_SPEEDS = int(1).to_bytes(1, 'big', signed=False)
    GET_LINE_POSITION = int(2).to_bytes(1, 'big', signed=False)
    SET_WHEEL_SPEED_AND_DIRECTION = int(3).to_bytes(1, 'big', signed=False)
    RESPONSE_CALIBRATED_WHEEL_SPEEDS = int(4).to_bytes(1, 'big', signed=False)
    RESPONSE_LINE_POSITION = int(5).to_bytes(1, 'big', signed=False)
    GET_STATUS = int(6).to_bytes(1, 'big', signed=False)
    RESPONSE_RUNNING = int(7).to_bytes(1, 'big', signed=False)
    RESPONSE_STOPPED = int(8).to_bytes(1, 'big', signed=False)


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
        left_direction: bytes,
        left_speed: bytes,
        right_direction: bytes,
        right_speed: bytes,
        device_id: bytes,
        destination: DESTINATION
) -> None:
    packet = packet_builder(
        PacketType.SET_WHEEL_SPEED_AND_DIRECTION,
        device_id,
        left_direction + left_speed + right_direction + right_speed
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