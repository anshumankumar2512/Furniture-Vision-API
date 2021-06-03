from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
import json


metadata = (('authorization', 'Key 2702e5276dc34e15a737b65b5277b2eb'),)

request = service_pb2.PostModelOutputsRequest(
    model_id='aaa03c23b3724a16a56b629203edc62c',
    inputs=[
      resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(url='https://images.pexels.com/photos/7199194/pexels-photo-7199194.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500')))
    ])
response = stub.PostModelOutputs(request, metadata=metadata)

if response.status.code != status_code_pb2.SUCCESS:
    raise Exception("Request failed, status code: " + str(response.status.code))
print(response)
#for concept in response.outputs[0].data.concepts:
    #print('%12s: %.2f' % (concept.name, concept.value))