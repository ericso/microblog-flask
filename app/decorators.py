from threading import Thread
# from multiprocessing import Process


def async(f):
  def wrapper(*args, **kwargs):
    thr = Thread(target=f, args=args, kwargs=kwargs)
    thr.start()

    # p = Process(target=f, args=args, kwargs=kwargs)
    # p.start()

  return wrapper
