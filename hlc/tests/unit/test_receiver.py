from hlc.mhist_api.rpc_pb2 import MeasurementMessage, Measurement, Raw, Numerical, Categorical
from hlc.receiver.receiver import Receiver
import time


def test_extract_raw_measurement():
    timestamp = int(time.time())

    position_sample = "2147483648,2147483648"
    position_measurement = Measurement(
        raw=Raw(ts=timestamp, value=position_sample.encode()))
    position_message = MeasurementMessage(
        name="test", measurement=position_measurement)

    unicode_sample = "¤࣢äࢻö%€ ¡!#:;ࠕࠇ?ýࠉ"
    unicode_measurement = Measurement(
        raw=Raw(ts=timestamp, value=unicode_sample.encode()))
    unicode_message = MeasurementMessage(
        name="test", measurement=unicode_measurement)

    receiver = Receiver(None, None, None, None, None, None)

    assert receiver.extract_measurement(position_message) == {
        'ts': timestamp,
        'value': position_sample
    }
    assert receiver.extract_measurement(unicode_message) == {
        'ts': timestamp,
        'value': unicode_sample
    }


def test_extract_numeric_measurement():
    timestamp = int(time.time())

    max_int32 = 2147483648
    max_int32_measurement = Measurement(
        numerical=Numerical(ts=timestamp, value=max_int32))
    max_int32_message = MeasurementMessage(
        name="test", measurement=max_int32_measurement)

    max_int64 = 9223372036854775807.0
    max_int64_measurement = Measurement(
        numerical=Numerical(ts=timestamp, value=max_int64))
    max_int64_message = MeasurementMessage(
        name="test", measurement=max_int64_measurement)

    negative_int = -24995321
    negative_int_measurement = Measurement(
        numerical=Numerical(ts=timestamp, value=negative_int))
    negative_int_message = MeasurementMessage(
        name="test", measurement=negative_int_measurement)

    receiver = Receiver(None, None, None, None, None, None)

    assert receiver.extract_measurement(max_int32_message) == {
        'ts': timestamp,
        'value': max_int32
    }
    assert receiver.extract_measurement(max_int64_message) == {
        'ts': timestamp,
        'value': max_int64
    }
    assert receiver.extract_measurement(negative_int_message) == {
        'ts': timestamp,
        'value': negative_int
    }
