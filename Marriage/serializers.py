from rest_framework import serializers
from .models import MarriageData, Contact, MeetingPoint, Testimonials, Gallery, Parents

class MarraigeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarriageData
        fields = '__all__'
        

class MarriageContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class MarraigeMeetingPointDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingPoint
        fields = '__all__'

class MarraigeTestimonialsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = '__all__'

class MarraigeParentsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = '__all__'

class MarraigeGalleryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'
