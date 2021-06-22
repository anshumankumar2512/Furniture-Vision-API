import os
import cloudinary
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

import pymongo
from pymongo import MongoClient
def clarifai_clearportal():
  api_key=os.environ.get('CLARIFAI_KEY') 
  metadata = (('authorization', api_key),)
  

  list_inputs_response = stub.ListInputs(
    service_pb2.ListInputsRequest(),
    metadata=metadata
  )

  #if list_inputs_response.status.code != status_code_pb2.SUCCESS:
    #raise Exception("List inputs failed, status: " + list_inputs_response.status.description)
  all_ids=[]  
  for input_object in list_inputs_response.inputs:
    all_ids.append(input_object.id)
  
    
  delete_inputs_response = stub.DeleteInputs(
    service_pb2.DeleteInputsRequest(
        ids=all_ids
    ),
    metadata=metadata
  )
  if len(all_ids)==0:
      return 0
  if delete_inputs_response.status.code != status_code_pb2.SUCCESS:
    raise Exception("Delete inputs failed, status: " + delete_inputs_response.status.description)

#clarifai_clearportal() 
def clarifai_train(cloudinary_url):
 api_key = os.environ.get('CLARIFAI_API_KEY') 
 #api_key=os.environ['CLARIFAI_API_KEY']
 metadata = (('authorization', api_key),)

 post_inputs_response = stub.PostInputs(
    service_pb2.PostInputsRequest(
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        url=cloudinary_url,
                        allow_duplicate_url=True
                    )
                )
            )
        ]
    ),
    metadata=metadata
 )

 print(post_inputs_response.inputs[0].id )
clarifai_train('https://res.cloudinary.com/visionsearch/image/upload/v1624270305/u5603dpjbbviccfsetpw.jpg')
