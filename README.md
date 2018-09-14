# MultiThreading
Test Multi-threading using PySimpleGui

This illustrates a sample application of PySimpleGui in a multi-threaded environment. The main thread consists of essentially what is a debug window that I had to implement by hand so I could control what happens.

A simple task is set up in a worker thread, which communicates to the main thread and the "debug" window using logging over a queue.

This is a fairly new attempt at Python and using PySimpleGui, so any feedback would be helpful.

If you find this useful, feel free to use in your own project.
