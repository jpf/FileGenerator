from Queue import Queue
from StringIO import StringIO
import threading
from time import sleep


class FileGenerator(object):
    def __init__(self):
        self.q = Queue()
        self.io = StringIO()

    def read_generator(self):
        running = True
        while(running):
            try:
                info = self.q.get(block=True, timeout=1)
                if info is None:
                    self.io.close()
                    self.q.task_done()
                    break
                else:
                    (pos, length) = info
                save_pos = self.io.tell()
                self.io.seek(pos)
                data = self.io.read(length)
                self.io.seek(save_pos)
                yield data
                self.q.task_done()
            except:
                running = False

    def write(self, s):
        info = (self.io.tell(), len(s))
        self.q.put(info)
        return self.io.write(s)

    def close(self):
        """ignore a close so read_generator can still access the StringIO"""
        self.q.put(None)
        return True

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            return getattr(self.io, name)(*args, **kwargs)
        return _missing


class GeneratorWorker(threading.Thread):
    def __init__(self, generator):
        self.__generator = generator
        threading.Thread.__init__(self)

    def run(self):
        rv = ''
        for x in self.__generator:
            rv += x
        print 'got: ', rv

if __name__ == '__main__':
    f = FileGenerator()

    GeneratorWorker(f.read_generator()).start()

    f.write('Test')
    f.seek(0)
    print 'read: ', f.read()
    sleep(1)
    f.write('ing')
    f.close()
