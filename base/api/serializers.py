from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    # Take the room model and serailize it and return it's json object
    class Meta:
        model = Room
        fields = "__all__"
