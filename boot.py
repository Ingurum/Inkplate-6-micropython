import machine

from app import App

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Waking up.')
    app = App()
    app.on_wakeup()
