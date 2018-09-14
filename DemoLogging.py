import queue
import logging
import threading
import PySimpleGUI as sg
import time


logger = logging.getLogger('mymain')


def externalFunction():
    logger.info('Hellp from external app')
    logger.info('External app sleeping 5 seconds')
    time.sleep(5)
    logger.info('External app waking up and exiting')


class ThreadedApp(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        externalFunction()

    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


def main():
    form = sg.FlexForm('Log window', default_element_size=(30, 2), font=('Helvetica', ' 10'), default_button_element_size=(8, 2), return_keyboard_events=True)

    layout =  \
        [
            [sg.Multiline(size=(127, 30), key='log')],
            [sg.ReadFormButton('Start', bind_return_key=True, key='start'), sg.Quit('Exit')]
        ]

    form.LayoutAndRead(layout, non_blocking=True)
    appStarted = False

    # Setup logging and start app
    logging.basicConfig(level=logging.DEBUG)
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    threadedApp = ThreadedApp()

    # Loop taking in user input and querying queue
    while True:
        # Check button
        (button, value) = form.ReadNonBlocking()

        if button is 'Start':
            if appStarted is False:
                threadedApp.start()
                logger.debug('App started')
                form.FindElement('start').Update(disabled=True)
                appStarted = True
        elif value is None or button is 'EXIT':
            break

        # Poll queue
        try:
            record = log_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            msg = queue_handler.format(record)
            logText = form.FindElement('log').Get()
            logText += msg
            form.FindElement('log').Update(logText)

    exit()


if __name__ == '__main__':
    main()
