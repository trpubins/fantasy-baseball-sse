"""
Python 3 module that propagates an exception occurring inside a thread up to its caller.
https://stackoverflow.com/a/31614591
"""

# Standard imports
from threading import Thread


class PropagatingThread(Thread):
    """
    Extends the threading.Thread class by propagating exceptions to the caller thread.
    """
    
    def run(self):
        """
        Method representing the thread's activity.
        """
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    
    def join(self, timeout=None):
        """
        Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        is_alive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        """
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret
