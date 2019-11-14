import hlc.mhist_api.rpc_pb2_grpc as rpc_grpc
from hlc.receiver.receiver import Receiver
from hlc.mhist_api.rpc_pb2 import MeasurementMessage, Measurement, Numerical, Filter, Raw

import grpc
import time
import random
from multiprocessing import Queue
from multiprocessing.queues import Queue as dt_queue


channel = grpc.insecure_channel('localhost:6666')
stub = rpc_grpc.MhistStub(channel)


class SLAMMock():

    def __init__(self, map_channel, position_channel):
        self.map_channel = map_channel
        self.position_channel = position_channel

    def _generate_point(self):
        x = random.randint(0, 255)
        y = random.randint(0, 255)
        point = {'ts': int(time.time()), 'value': bytes([x, y])}
        return point

    def push_position(self):
        point = self._generate_point()
        measurement = Measurement(
            raw=Raw(ts=point['ts'], value=point['value']))
        stub.Store(MeasurementMessage(
            name=self.position_channel, measurement=measurement))
        return point

    def push_20points(self):
        points = []
        messages = []
        for i in range(20):
            p = self._generate_point()
            m = MeasurementMessage(name=self.map_channel,
                                   measurement=Measurement(raw=Raw(ts=p['ts'], value=p['value'])))
            points.append(p)
            messages.append(m)
        stub.StoreStream(iter(messages))
        return points


class GaitMock():

    def __init__(self, feedback_channel):
        self.feedback_channel = feedback_channel

    def _generate_feedback(self):
        feedback_examples = ['done']
        for i in range(1, 7):
            feedback_examples.append(
                'l{} stuck at {} rotation'.format(i, random.randint(0, 120)))
            feedback_examples.append(
                'l{} stuck at {} lifting'.format(i, random.randint(0, 120)))
            feedback_examples.append('l{} not responding'.format(i))
        feedback = {'ts': int(time.time()), 'value': random.choice(
            feedback_examples).encode()}
        return feedback

    def push_feedback(self):
        feedback = self._generate_feedback()
        measurement = Measurement(
            raw=Raw(ts=feedback['ts'], value=feedback['value']))
        stub.Store(MeasurementMessage(name=self.feedback_channel,
                                      measurement=measurement))
        return feedback


def test_base_case():
    # dt_queue - datatype queue
    # used to fix autocomplete for Queue
    map_queue: dt_queue
    pos_queue: dt_queue
    gait_queue: dt_queue

    map_queue = Queue()
    pos_queue = Queue()
    gait_queue = Queue()

    map_channel = 'map_updates'
    pos_channel = 'position_updates'
    gait_channel = 'gait_feedback'

    p = Receiver(map_queue, pos_queue, gait_queue,
                 map_channel, pos_channel, gait_channel)
    p.start()

    slam_mock = SLAMMock(map_channel, pos_channel)
    gait_mock = GaitMock(gait_channel)

    position = slam_mock.push_position()
    map_update = slam_mock.push_20points()
    gait_feedback = gait_mock.push_feedback()

    time.sleep(1)

    # assert pos_queue.qsize() == 1
    assert map_queue.qsize() == 20
    assert gait_queue.qsize() == 1

    assert pos_queue.get() == position
    assert gait_queue.get() == gait_feedback

    for p in map_update[::-1]:
        assert map_queue.get() == p

    p.terminate()


def test_multiqueue():
    pass
