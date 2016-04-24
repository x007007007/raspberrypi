# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import subprocess
import tempfile
import os
import warnings
import datetime
from threading import RLock


class CamRtsp(object):
    sp_grab = None
    sp_cvlc = None
    running = False
    status_lock = RLock()
    def __init__(self, path="/", port=8554):
        self.pipe_path = tempfile.mktemp(suffix="_webcam.fifo")


    def get_cam(self):
        try:
            self.sp_grab = subprocess.Popen(['raspivid', '-o', self.pipe_path,
                                          '-t', '0', '-n', '-w', '600', '-h', '400', '-fps', '12'],
                             preexec_fn=os.setsid)
            return True
        except OSError:
            return False

    def send_cvlc(self):
        args = ['cvlc', '-vvv', "stream://{}".format(self.pipe_path), '--sout', '#rtp{sdp=rtsp://:8554/}', ':demux=h264']
        try:
            self.sp_cvlc = subprocess.Popen(args, preexec_fn=os.setsid)
            return True
        except OSError:
            return False

    def stop(self):
        with self.status_lock:
            print("--stop service")
            if self.sp_grab:
                self.sp_grab.terminate()
            if self.sp_cvlc:
                self.sp_cvlc.terminate()
            if os.path.exists(self.pipe_path):
                os.unlink(self.pipe_path)
            self.running = False
            print("++stop ok")

    def start(self):
        with self.status_lock:
            print("--start service")
            if not os.path.exists(self.pipe_path):
                os.mkfifo(self.pipe_path)
            if not self.get_cam():
                warnings.warn("raspberry Pi Only")
            elif not self.send_cvlc():
                warnings.warn("cvlc not in PATH")
            self.running = True
            self.send_cvlc()
            print("++start ok")

    def status(self):
        with self.status_lock:
            print('--status-check')
            if self.running:
                if self.sp_grab.poll() or self.sp_cvlc.poll():
                    self.running = False
                    return "stop"
                else:
                    return "start"
            else:
                return "stop"

def console_run():
    try:
        cr = CamRtsp()
        cr.start()
        time_point = [datetime.datetime.now() + datetime.timedelta(seconds=26)]

        def timeout_check():
            if time_point[0] < datetime.datetime.now():
                if cr.status() == "start":
                    cr.stop()

        class WatchDogHandler(tornado.web.RequestHandler):
            def get(self):
                time_point[0] = datetime.datetime.now() + datetime.timedelta(seconds=26)
                print cr.status()
                if cr.status() != "start":
                    cr.start()
                self.write(time_point[0].strftime("%s"))

        httpd = tornado.web.Application([
            (r"/.*", WatchDogHandler),
        ])
        httpd.listen(5001, 'localhost')

        tornado.ioloop.PeriodicCallback(timeout_check, 5000).start()
        tornado.ioloop.IOLoop.current().start()
    finally:
        cr.stop()


if __name__ == "__main__":
    console_run()