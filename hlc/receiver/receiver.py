import grpc
import hlc.mhist_api.rpc_pb2_grpc as rpc_grpc
from hlc.mhist_api.rpc_pb2 import Filter, MeasurementMessage, Measurement, Raw
from multiprocessing import Process
from multiprocessing.queues import Queue


class Receiver(Process):

    def __init__(
            self, map_queue: Queue, pos_queue: Queue, gait_queue: Queue,
            map_channel: str, pos_channel: str, gait_channel: str,
            mhist_address='localhost', mhist_port='6666',
            daemon=False, name='receiver-process'):
        super().__init__(daemon=daemon, name=name)
        self.map_queue = map_queue
        self.pos_queue = pos_queue
        self.gait_queue = gait_queue
        self.map_channel = map_channel
        self.pos_channel = pos_channel
        self.gait_channel = gait_channel

        channel = grpc.insecure_channel(mhist_address + ':' + mhist_port)
        self.mhist_stub = rpc_grpc.MhistStub(channel)

    def extract_measurement(self, measurementMessage):
        if measurementMessage.measurement.HasField("numerical"):
            measurement = measurementMessage.measurement.numerical
            value = measurement.value
        elif measurementMessage.measurement.HasField("categorical"):
            measurement = measurementMessage.measurement.categorical
            value = measurement.value
        elif measurementMessage.measurement.HasField("raw"):
            measurement = measurementMessage.measurement.raw
            value = measurement.value.decode()
        else:
            raise TypeError(
                "The received MeasurementMessage has an unkown type")
        timestamp = measurement.ts

        return {'ts': timestamp, 'value': value}

    def run(self):
        channels = [self.map_channel, self.pos_channel, self.gait_channel]
        for message in self.mhist_stub.Subscribe(
                Filter(names=channels)):
            measurement = self.extract_measurement(message)

            if message.name == self.map_channel:
                self.map_queue.put(measurement)
            elif message.name == self.pos_channel:
                self.pos_queue.put(measurement)
            elif message.name == self.gait_channel:
                self.gait_queue.put(measurement)
            else:
                raise ValueError(
                    "Given channel Name doesn't match message-channel!")
