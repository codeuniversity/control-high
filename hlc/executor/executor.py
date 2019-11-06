import grpc
import hlc.mhist_api.rpc_pb2_grpc as rpc_grpc

channel = grpc.insecure_channel('localhost:6666')
stub = rpc_grpc.MhistStub(channel)
