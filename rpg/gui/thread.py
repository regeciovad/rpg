from multiprocessing import Process, Queue
from threading import Thread
from io import StringIO
from contextlib import redirect_stdout


class _StringIO(StringIO):
    """ Overwriting of StringIO for real time output caching. """

    def __init__(self, buff):
        super(_StringIO, self).__init__()
        self.buff = buff

    def write(self, s):
        super(_StringIO, self).write(s)
        if s and s != '\n':
            self.buff.put(s)


class ThreadWrapper():
    """ Unblocking way to connect functions with GUI for redirection
        it's output in real time. """

    def __init__(self, widget, func, *args):
        """ Runs function in new process and add output
            to GUI widget from thread with queue. """
        self._widget = widget
        self._queue = Queue()
        self._process = Process(target=self.wrapper,
                                args=(self._queue, func, args, ))
        self._thread = Thread(target=self.writer)
        self._running = False

    def run(self):
        """ Starts the process and the thread. """
        if not self._running:
            self._process.start()
            self._thread.start()
            self._running = True

    def kill(self):
        """ Stops the process and the thread (there are no official
            way to stop thread. This will unlocked thread and it will
            be stopped with GUI - without error). """
        self._thread._tstate_lock = None
        self._thread._stop()
        self._thread.join()
        self._process.terminate()

    @staticmethod
    def wrapper(queue, func, args):
        """ Redirects stdout and call function.
            Output will be in queue."""
        f = _StringIO(queue)
        with redirect_stdout(f):
            func(*args)
        f.close()

    def writer(self):
        """ Appends output from function to the GUI widget. """
        while self._process.is_alive():
            self._widget.appendPlainText(self._queue.get())
