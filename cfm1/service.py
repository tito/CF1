import zmq
from multiprocessing import Process
from kivy.clock import Clock


class ServiceController(object):
    def start(self):
        self.ctx = zmq.Context()
        self.sock_seq_in = self.ctx.socket(zmq.PULL)
        self.sock_seq_in.bind("ipc://sequencerstatus")
        self.start_sequencer_service()

        # we check at 60FPS, so we may be in sync up to
        # 225 BPM with 16 intervals in a beat
        Clock.schedule_interval(self.poll, 1 / 60.)

    def start_sequencer_service(self):
        from cfm1.services.sequencer import run
        self.process_sequencer = Process(target=run)
        self.process_sequencer.start()
        self.sock_seq = self.ctx.socket(zmq.PUSH)
        self.sock_seq.connect("ipc://sequencer")

    def join(self):
        self.sock_seq.send_json(("EXIT", ))
        self.process_sequencer.join()

    def poll(self, *largs):
        sock_seq_in = self.sock_seq_in
        sock_seq = self.sock_seq
        while sock_seq_in.poll(timeout=1):
            msg = sock_seq_in.recv_json()
            cmd, args = msg[0], msg[1:]
            print("Sequencer: {}: {}".format(cmd, args))



service = ServiceController()
