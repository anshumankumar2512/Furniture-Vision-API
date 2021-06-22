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


##################     CLOUDINARY SECTION

def cloudinaryurl(DATADIR):

 #Authenticate Cloudinary
 key=os.environ.get('CLOUDINARY_KEY')
 secret=os.environ.get('CLOUDINARY_SECRET')
 cloudinary.config(
  cloud_name = 'visionsearch',  
  api_key = key,  
  api_secret = secret
  )
 

 formats=['jpg', 'jpeg', 'png']
 response_list=[]
 for image in os.listdir(DATADIR):
   if image.split('.')[1] in formats:   
    path=os.path.join(DATADIR, image)
    response= cloudinary.uploader.upload(path) 
    di={}
    di['filename']=response['original_filename']
    di['url']=response['url']
    response_list.append(di)
 return response_list


####################         CLARIFAI SECTION


def clarifai_train(cloudinary_url):
 api_key=os.environ.get('CLARIFAI_KEY') 
 metadata = (('authorization', 'Key 6c9bfc1ce038475ea47a1cab44af5d7d'),)

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

 return(post_inputs_response.inputs[0].id )



def clarifai_search(cloudinary_url):
  api_key=os.environ.get('CLARIFAI_KEY') 
  metadata = (('authorization', 'Key 6c9bfc1ce038475ea47a1cab44af5d7d'),)
  post_annotations_searches_response = stub.PostAnnotationsSearches(
    service_pb2.PostAnnotationsSearchesRequest(
        searches = [
            resources_pb2.Search(
                query=resources_pb2.Query(
                    ranks=[
                        resources_pb2.Rank(
                            annotation=resources_pb2.Annotation(
                                data=resources_pb2.Data(
                                    image=resources_pb2.Image(
                                        url=cloudinary_url
                                    )
                                )
                            )
                        )
                    ]
                )
            )
        ]
    ),
    metadata=metadata
  )

  if post_annotations_searches_response.status.code != status_code_pb2.SUCCESS:
    raise Exception("Post searches failed, status: " + post_annotations_searches_response.status.description)

  query_list=[]
  for hit in post_annotations_searches_response.hits:
    if hit.score>=0.85:
        di={}
        di['input_id']=hit.input.id
        di['score']=hit.score
        query_list.append(di)
  return query_list      



def clarifai_clearportal():
  api_key=os.environ.get('CLARIFAI_KEY') 
  metadata = (('authorization', 'Key 6c9bfc1ce038475ea47a1cab44af5d7d'),)
  

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





##################        MONGODB SECTION

def updatedb(entries):
 # replace this with your MongoDB connection string
 client=MongoClient('mongodb+srv://'+os.environ.get('DB_USER')+':'+os.environ.get('DB_PASSWORD')+'@internship.qp5bx.mongodb.net/computervision?retryWrites=true&w=majority',tlsAllowInvalidCertificates=True)
 db = client.computervision
 visualsearch = db.visualsearch
 visualsearch.insert_many(entries)

def searchdb(id_list):
 # replace this with your MongoDB connection string
 client=MongoClient('mongodb+srv://'+os.environ.get('DB_USER')+':'+os.environ.get('DB_PASSWORD')+'@internship.qp5bx.mongodb.net/computervision?retryWrites=true&w=majority',tlsAllowInvalidCertificates=True)
 db = client.computervision
 visualsearch = db.visualsearch
 results = db.visualsearch.find({"input_id": {"$in": id_list}})
 return results

def cleardb():
 client=MongoClient('mongodb+srv://'+os.environ.get('DB_USER')+':'+os.environ.get('DB_PASSWORD')+'@internship.qp5bx.mongodb.net/computervision?retryWrites=true&w=majority',tlsAllowInvalidCertificates=True)
 db = client.computervision
 visualsearch = db.visualsearch
 visualsearch.delete_many({})