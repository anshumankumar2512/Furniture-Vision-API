from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='2702e5276dc34e15a737b65b5277b2eb')

app = ClarifaiApp()
model = app.public_models.general_model
response = model.predict_by_url(url='https://images.pexels.com/photos/7199194/pexels-photo-7199194.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500')
concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(concept['name'], concept['value'])