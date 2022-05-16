import cocotb
from cocotb.triggers import Timer, Combine
import logging

#help(logging)
"""basicConfig(**kwargs)
        Do basic configuration for the logging system.
        
        This function does nothing if the root logger already has handlers
        configured, unless the keyword argument *force* is set to ``True``.
        It is a convenience method intended for use by simple scripts
        to do one-shot configuration of the logging package.
        
        The default behaviour is to create a StreamHandler which writes to
        sys.stderr, set a formatter using the BASIC_FORMAT format string, and
        add the handler to the root logger.
        
        A number of optional keyword arguments may be specified, which can alter
        the default behaviour.
        
        filename  Specifies that a FileHandler be created, using the specified
                  filename, rather than a StreamHandler.
        filemode  Specifies the mode to open the file, if filename is specified
                  (if filemode is unspecified, it defaults to 'a').
        format    Use the specified format string for the handler.
        datefmt   Use the specified date/time format.
        style     If a format string is specified, use this to specify the
                  type of format string (possible values '%', '{', '$', for
                  %-formatting, :meth:`str.format` and :class:`string.Template`
                  - defaults to '%').
        level     Set the root logger level to the specified level.
        stream    Use the specified stream to initialize the StreamHandler. Note
                  that this argument is incompatible with 'filename' - if both
                  are present, 'stream' is ignored.
        handlers  If specified, this should be an iterable of already created
                  handlers, which will be added to the root handler. Any handler
                  in the list which does not have a formatter assigned will be
                  assigned the formatter created in this function.
        force     If this keyword  is specified as true, any existing handlers
                  attached to the root logger are removed and closed, before
                  carrying out the configuration as specified by the other
                  arguments.
        encoding  If specified together with a filename, this encoding is passed to
                  the created FileHandler, causing it to be used when the file is
                  opened.
        errors    If specified together with a filename, this value is passed to the
                  created FileHandler, causing it to be used when the file is
                  opened in text mode. If not specified, the default value is
                  `backslashreplace`.
        
        Note that you could specify a stream created using open(filename, mode)
        rather than passing the filename and mode in. However, it should be
        remembered that StreamHandler does not close its stream (since it may be
        using sys.stdout or sys.stderr), whereas FileHandler closes its stream
        when the handler is closed.
        
        .. versionchanged:: 3.2
           Added the ``style`` parameter.
        
        .. versionchanged:: 3.3
           Added the ``handlers`` parameter. A ``ValueError`` is now thrown for
           incompatible arguments (e.g. ``handlers`` specified together with
           ``filename``/``filemode``, or ``filename``/``filemode`` specified
           together with ``stream``, or ``handlers`` specified together with
           ``stream``.
        
        .. versionchanged:: 3.8
           Added the ``force`` parameter.
        
        .. versionchanged:: 3.9
           Added the ``encoding`` and ``errors`` parameters.
"""

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# ## Defining coroutines

# Figure 1: Hello world as a coroutine
@cocotb.test()
async def hello_world(_):
    """Say hello!"""
    logger.info("Hello, world.")


# ## Awaiting simulation time

# Figure 5 Python waits for 2 nanoseconds
@cocotb.test()
async def wait_2ns(_):
    """Waits for two ns then prints"""
    await Timer(2, units="ns")
    logger.info("I am DONE waiting!")


# ## Starting tasks

# Figure 6: counter counts up with a delay
async def counter(name, delay, count):
    """Counts up to the count argument after delay"""
    for ii in range(1, count + 1):
        await Timer(delay, units="ns")
        logger.info(f"{name} counts {ii}")


# ### Ignoring a running task

# Figure 7: Launching a task and ignoring it
@cocotb.test()
async def do_not_wait(_):
    """Launch a counter"""
    logger.info("start counting to 3")
    cocotb.start_soon(counter("simple count", 1, 3))
    logger.info("ignored running_task")


# ### Awaiting a running task

# Figure 8: Waiting for a running task
@cocotb.test()
async def wait_for_it(_):
    """Launch a counter"""
    logger.info("start counting to 3")
    running_task = cocotb.start_soon(counter("simple count", 1, 3))
    await running_task
    logger.info("waited for running task")


# ### Running tasks in parallel

# Figure 9: Mom and The Count count in parallel
@cocotb.test()
async def counters(_):
    """Test that starts two counters and waits for them"""
    logger.info("The Count will count to five.")
    logger.info("Mom will count to three.")
    the_count = cocotb.start_soon(counter("The Count", 1, 5))
    mom_warning = cocotb.start_soon(counter("Mom", 2, 3))
    await Combine(the_count, mom_warning)
    logger.info("All the counting is finished")


# ### Returning values from tasks

# Figure 12: A coroutine that increments a number
# and returns it after a delay
async def wait_for_numb(delay, numb):
    """Waits for delay ns and then returns the increment of the number"""
    await Timer(delay, units="ns")
    return numb + 1


# Figure 13: Getting a return value by awaiting the
# returned RunningTask object
@cocotb.test()
async def inc_test(_):
    """Demonstrates start_soon() return values"""
    logging.info("sent 1")
    inc1 = cocotb.start_soon(wait_for_numb(1, 1))
    nn = await inc1
    logging.info(f"returned {nn}")
    logging.info(f"sent {nn}")
    inc2 = cocotb.start_soon(wait_for_numb(10, nn))
    nn = await inc2
    logging.info(f"returned {nn}")


# Figure 15: ### Killing a task
@cocotb.test()
async def kill_a_running_task(_):
    """Kill a running task"""
    kill_me = cocotb.start_soon(counter("Kill me", 1, 1000))
    await Timer(5, units="ns")
    kill_me.kill()
    logger.info("Killed the long-running task.")
