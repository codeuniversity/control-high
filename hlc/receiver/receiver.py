import grpc
import hlc.mhist_api.rpc_pb2_grpc as rpc_grpc
from hlc.mhist_api.rpc_pb2 import Filter, MeasurementMessage, Measurement, Raw
from multiprocessing import Process
from multiprocessing.queues import Queue

MHIST_address = 'localhost'
MHIST_port = '6666'

channel = grpc.insecure_channel(MHIST_address + ':' + MHIST_port)
stub = rpc_grpc.MhistStub(channel)


class Receiver(Process):

    def __init__(
            self, map_queue: Queue, pos_queue: Queue, gait_queue: Queue,
            map_channel: str, pos_channel: str, gait_channel: str,
            daemon=False, name='receiver-process'):
        # super().__init__(group=None, target=None, name=name, args=None, daemon=daemon)
        super().__init__()
        self.map_queue = map_queue
        self.pos_queue = pos_queue
        self.gait_queue = gait_queue
        self.map_channel = map_channel
        self.pos_channel = pos_channel
        self.gait_channel = gait_channel

    def run(self):
        channels = [self.map_channel, self.pos_channel, self.gait_channel]
        for message in stub.Subscribe(
                Filter(names=channels)):

            if message.measurement.HasField("numerical"):
                measurement = message.measurement.numerical
            elif message.measurement.HasField("categorical"):
                measurement = message.measurement.categorical
            elif message.measurement.HasField("raw"):
                measurement = message.measurement.raw

            if message.name == self.map_channel:
                self.map_queue.put(
                    {'ts': measurement.ts, 'value': measurement.value})
            elif message.name == self.pos_channel:
                self.pos_queue.put(
                    {'ts': measurement.ts, 'value': measurement.value})
            elif message.name == self.gait_channel:
                self.gait_queue.put(
                    {'ts': measurement.ts, 'value': measurement.value})
