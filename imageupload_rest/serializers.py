
from rest_framework import serializers
from upload_image.models import UploadImage


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ('patient', 'image')
