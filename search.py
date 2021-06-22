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

def search_results():
    DATADIR=os.path.join(os.getcwd(), 'processed')

#Get url for search images
    response_list=cloudinaryurl(DATADIR)
    #print(response_list)

 #Perform visual search and return input ids of all matching images. For each search entries.
    url_list=[]
    for dictionary in response_list:
       search_results=clarifai_search(dictionary['url'])
       #print(search_results)
       ids=[result['input_id'] for result in search_results]
       cursors=searchdb(ids)
       for cursor in cursors:
           response={}
           response['filename']=cursor['filename']
           response['url']=cursor['url']
           url_list.append(response)
    return (url_list)
#print(search_results())       
    


