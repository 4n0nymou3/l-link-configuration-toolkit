import uuid

from l_toolkit.state import State


def fresh_state():
    return State(device_id=str(uuid.uuid4()))
