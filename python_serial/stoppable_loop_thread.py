import threading
import logging

class StoppableLoopThread(threading.Thread):
    """
        Thread class with a stop() method. The worker function must return none to break loop
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.
        """
        super(StoppableLoopThread, self).__init__(group=group, target=target, name=name,
                 args=args, kwargs=kwargs, daemon=daemon)
        self._stop_event = threading.Event()            

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            logging.debug("starting loop...")
            while not self._stop_event.is_set():
                if self._target:
                    target_return = self._target(*self._args, **self._kwargs)
                    if(target_return == None):
                        self._stop_event.set()
            logging.debug("ending loop...")
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()