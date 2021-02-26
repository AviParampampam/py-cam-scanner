import socket
import threading
from queue import Queue


def scan_cameras(start: int, end: int, timeout=1.5, threads=150) -> list:
    cameras = []
    print_lock = threading.Lock()
    q = Queue()

    def _scan(n):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        host = '192.168.1.' + str(n)
        try:
            con = sock.connect((host, 554))
            with print_lock:
                cameras.append(host)
            con.close()
        except:
            pass

    def _threader():
        while True:
            _scan(q.get())
            q.task_done()

    for x in range(threads):
        threading.Thread(target=_threader, daemon=True).start()

    for worker in range(start, end):
        q.put(worker)

    q.join()

    return cameras


print(scan_cameras(10, 500))
# print(scan_camera('192.168.1.15:554'))
