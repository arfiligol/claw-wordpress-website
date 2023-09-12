from stem import Signal
from stem.control import Controller

def renewTorNYM():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=None)
        controller.signal(Signal.NEWNYM)