import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.utils import get_unique_file_name, save_image
from services.rice_detector import HomogeneousBgDetector
from services.leaf_detector import LeafDetector
from services.cloudinary import upload
from db.db import get_connection
import io
from rest_framework.parsers import JSONParser
from constants.constants import TEMP_DIR


firebase = get_connection()

# RICE API VIEWS

# This view is responsible for retrieving data from firebase


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def get_rice(request):
    print("I am here")
    user_id = request.GET.get('user_id', None)
    if user_id is not None:
        records = firebase.child(
            "rice-data").order_by_child("userId").equal_to(user_id).get()

        json_records = []
        for record in records.each():
            json_records.append(record.val())

        print("JSON_RESPONSE: ", json_records)

        return Response({'success': True, 'data': json_records})

    data = {
        'success': True,
        'message': 'Please provide user id in params',

    }
    return Response(data)


# This view is responsible for image detection and uploading image to cloudinary
@api_view(['POST', 'GET'])
def detect_rice(request):

    try:
        if request.method == 'POST':
            if request.FILES and 'image' in request.FILES.keys():
                file = request.FILES['image']
                image_name = get_unique_file_name(file.name)
            else:
                image_name = request.data['image']['name']
                image_b64_data = request.data['image']['data']

            # Saving image
            file_path = TEMP_DIR / image_name
            save_image(file_path, base64.b64decode(image_b64_data), b64=True) if image_b64_data else save_image(
                file_path, file.chunks())

            # Now we will detect image using detector
            detector = HomogeneousBgDetector()
            image_data = detector.detect(image_name)

            # Now we will upload detected image to the cloudinary
            detected_image_path = TEMP_DIR / \
                f"{image_name.split('.')[0]}_detected.{image_name.split('.')[1]}"

            url = upload(detected_image_path)

            return Response({'success': True,
                            'message': 'Image has been saved successfully.',
                             'data': image_data,
                             'image': url})

    except KeyError as e:
        return Response({'success': False, 'message': f" {str(e)} is not found in request data. "})

    except Exception as e:
        return Response({'success': False, 'message': f" Request is not completed due to following error:\n{str(e)}"})


# This view is responsible for storing data in firebase
@api_view(['POST'])
def create_rice(request):
    try:
        data = request.body
        if data is not None or data.get('userId') is not None:
            data = io.BytesIO(data)
            data = JSONParser().parse(data)
            firebase.child("rice-data").push(data)
            return Response({'success': True, 'message': 'Stored Successfully'})
        else:
            return Response({'success': False, 'message': 'Missing Body'})
    except Exception as e:
        print(e)
        return Response({'success': False, 'message': f" Request is not completed due to following error:\n{str(e)}"})


# Leaf API actions

# This action is for storing leaf data in database
@api_view(['POST'])
def create_leaf(request):
    try:
        data = request.body
        if data is not None or data.get('userId') is not None:
            data = io.BytesIO(data)
            data = JSONParser().parse(data)
            firebase.child("leaf-data").push(data)
            return Response({'success': True, 'message': 'Stored Successfully'})
        else:
            return Response({'success': False, 'message': 'Missing Body'})
    except Exception as e:
        print(e)
        return Response({'success': False, 'message': f" Request is not completed due to following error:\n{str(e)}"})


# This action is for retreiving leaves data from database
@api_view(['GET'])
def get_leaves(request):
    user_id = request.GET.get('user_id', None)
    if user_id is not None:
        records = firebase.child(
            "leaf-data").order_by_child("userId").equal_to(user_id).get()

        json_records = []
        for record in records.each():
            json_records.append(record.val())
        
        return Response({'success': True, 'data': json_records})

    data = {
        'success': True,
        'message': 'Please provide user id in params',

    }
    return Response(data)


# This view is responsible for image detection and uploading image to cloudinary
@api_view(['POST', 'GET'])
def detect_leaf(request):

    try:
        if request.method == 'POST':
            if request.FILES and 'image' in request.FILES.keys():
                file = request.FILES['image']
                image_name = get_unique_file_name(file.name)
            else:
                image_name = request.data['image']['name']
                image_b64_data = request.data['image']['data']

            # Saving image
            file_path = TEMP_DIR / image_name
            save_image(file_path, base64.b64decode(image_b64_data), b64=True) if image_b64_data else save_image(
                file_path, file.chunks())

            # Now we will detect image using detector
            detector = LeafDetector()
            image_data = detector.detect(image_name)

            # Now we will upload detected image to the cloudinary
            detected_image_path = TEMP_DIR / \
                f"{image_name.split('.')[0]}_detected.{image_name.split('.')[1]}"

            url = upload(detected_image_path)

            return Response({'success': True,
                            'message': 'Image has been saved successfully.',
                             'data': image_data,
                             'image': url})

    except KeyError as e:
        return Response({'success': False, 'message': f" {str(e)} is not found in request data. "})

    except Exception as e:
        return Response({'success': False, 'message': f" Request is not completed due to following error:\n{str(e)}"})
