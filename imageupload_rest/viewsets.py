import imp
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from .serializers import UploadImageSerializer
from upload_image.models import UploadImage
from accounts.models import Patient
import os
from PIL import Image
import numpy as np
from uuid import uuid4
import time 

from keras.models import load_model

class FileUploadView(APIView):
    def __init__(self):
        permission_classes = []
        parser_class = (MultiPartParser, JSONParser)
        self.model_path = f"{os.getcwd()}/model/best_model.hdf5"
    def post(self, request, *args, **kwargs):
        # print(dir(request.stream.body))
        context = {}
        # to retrieve email from url
        email = request.GET.get('username')
        print(request.data)
        # print(dir(request.stream))

        # email = email.lower() if email else None
        account = Patient.objects.filter(user__username=email)

        if account.count() == 0:
            context['response'] = 'Error'
            context['error_message'] = 'email not found'
            return Response(data=context)

        account = account[0]

        context['image'] = request.FILES.get('image')

        file_serializer = img_object = UploadImage.objects.filter(patient_id=account.id)
        if img_object.count() == 0:
            img_object = UploadImage.objects.create(patient_id=account.id)
            
        else:
            img_object = img_object[0]
            
        file_serializer = UploadImageSerializer(img_object, data={**context, 'patient': account.id})

        if file_serializer.is_valid():

            model = load_model(self.model_path)
            img_path = fr'{os.getcwd()}\media\img\{file_serializer.validated_data["image"]}'

            file_serializer.save()
            try :
                img2 = Image.open(img_path)
                y = np.array(img2.resize((128,128)))
                y = y.reshape(1, 128, 128, 3)
                result = model.predict([y])
                print(f">>>> {result}")
                classification = np.where(result == np.amax(result))[1][0]
                print(f"c>>>> {classification}")
                if classification == 0:
                    result =  "Not a tumor"
                else:
                    result =  "a tumor"
                print(f"the result is {result}")
            except : 
                result = "please upload valid photo"

            context = {**context, **file_serializer.data.copy()}
            context['response'] = "Success"

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
