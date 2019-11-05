update_submodule:
	git submodule update --init

proto: update_submodule
	python -m grpc_tools.protoc -I./mhist/proto --python_out=./hlc/mhist_api --grpc_python_out=./hlc/mhist_api ./mhist/proto/rpc.proto

start_grpcui:
	grpcui -proto mhist/proto/rpc.proto -plaintext localhost:6666
