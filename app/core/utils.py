import uuid
from core.models import PIN


def generate_unique_pin():
    while True:
        pin = (str(uuid.uuid4()).replace("-", "")[:10]).upper()
        if not PIN.objects.filter(pin_code=pin).exists():
            return pin
