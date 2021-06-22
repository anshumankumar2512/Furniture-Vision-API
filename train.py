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

from functions import *


DATADIR=os.path.join(os.getcwd(), 'img')

#Get url for training images
response_list=cloudinaryurl(DATADIR)

#Clearing previous uploads
clarifai_clearportal()

#Upload training images to Clarifai
for dictionary in response_list:
    id=clarifai_train(dictionary['url'])   
    dictionary['input_id']=id
#print(response_list)
#print("done")
cleardb()
#print("done again")
updatedb(response_list)
