from ..client import Client
from .service_file_pb2_grpc import FileStub
import grpc


class GRPCClient(Client):

    def __init__(self, context):
        super().__init__(context)
        self.stub = FileStub(grpc.insecure_channel(self.grpc_server))

    def read(self, uuid):
        raise NotImplemented

    def stat(self, uuid):
        raise NotImplemented
