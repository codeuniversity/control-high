import random
import time
import grpc
from concurrent import futures
from hlc.mhist_api.rpc_pb2 import MeasurementMessage, Measurement, Raw
from hlc.mhist_api.rpc_pb2_grpc import add_MhistServicer_to_server, MhistServicer
from hlc.receiver.receiver import Receiver
import multiprocessing as mp


class MhistMock(MhistServicer):

    def __init__(self, map_channel, pos_channel, gait_channel):
        super().__init__()
        self.map_channel = map_channel
        self.pos_channel = pos_channel
        self.gait_channel = gait_channel

        self.gait_feedback = self.generate_gait_feedback()
        self.map_updates = self.generate_map_updates()
        self.robot_position = ["{},{}".format(0, 0)]

    def generate_gait_feedback(self):
        feedback_examples = []
        for i in range(1, 7):
            feedback_examples.append('l{} done'.format(i))
            feedback_examples.append(
                'l{} stuck at {} rotation'.format(i, random.randint(0, 120)))
            feedback_examples.append(
                'l{} stuck at {} lifting'.format(i, random.randint(0, 120)))
            feedback_examples.append('l{} not responding'.format(i))
        return feedback_examples

    def generate_map_updates(self):
        map_update = []
        for x in range(19):
            for y in range(19):
                map_update.append('{},{}'.format(x, y))
        return map_update

    def Subscribe(self, request, context):
        timestamp = int(time.time())

        for feedback in self.gait_feedback:
            message = MeasurementMessage(
                name=self.gait_channel,
                measurement=Measurement(
                    raw=Raw(
                        ts=timestamp,
                        value=feedback.encode()
                    )
                )
            )
            yield message
        for update in self.map_updates:
            message = MeasurementMessage(
                name=self.map_channel,
                measurement=Measurement(
                    raw=Raw(
                        ts=timestamp,
                        value=update.encode()
                    )
                )
            )
            yield message
        for position in self.robot_position:
            message = MeasurementMessage(
                name=self.pos_channel,
                measurement=Measurement(
                    raw=Raw(
                        ts=timestamp,
                        value=position.encode()
                    )
                )
            )
            yield message


def serve_mhist_mock(mhist_servicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MhistServicer_to_server(
        mhist_servicer, server)
    server.add_insecure_port('127.0.0.1:6655')
    server.start()
    while True:
        time.sleep(1)


def test_receiver():
    map_channel = "map_updates"
    pos_channel = "position_updates"
    gait_channel = "gait_feedback"

    map_queue = mp.Queue()
    pos_queue = mp.Queue()
    gait_queue = mp.Queue()

    mhist_mock = MhistMock(map_channel, pos_channel, gait_channel)
    mhist_process = mp.Process(target=serve_mhist_mock, args=(mhist_mock, ))
    mhist_process.start()

    receiver = Receiver(map_queue, pos_queue, gait_queue,
                        map_channel, pos_channel, gait_channel, mhist_port="6655")
    receiver.start()
    time.sleep(3)
    receiver.terminate()
    mhist_process.terminate()

    assert map_queue.qsize() == len(mhist_mock.map_updates)
    assert pos_queue.qsize() == len(mhist_mock.robot_position)
    assert gait_queue.qsize() == len(mhist_mock.gait_feedback)
