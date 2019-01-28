from rest_framework import serializers
from cotidia.core.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        exclude = ["id"]
