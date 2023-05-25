import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name="dtcb8jjq0",
    api_key="934738636266866",
    api_secret="MI8p0sPJtwxrdmtimjXp2VZApBQ",
    secure=True
)

'''
This function uploads image to cloudinary
and returns secure url of it
'''


def upload(path):
    response = cloudinary.uploader.upload(path)
    return response['secure_url']
