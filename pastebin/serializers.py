from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from pastebin.models import Snippet

class NameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class SnippetSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=140)
    code = serializers.CharField()
    lang = serializers.ChoiceField(choices=Snippet.LANGS)

class SnippetModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_detail = serializers.SerializerMethodField()
    user_detail2 = NameUserSerializer()
    full_name = serializers.SerializerMethodField()
    created_count = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'lang', 'user', 'full_name', 'created_count', 'user_detail')

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_created_count(self, obj):
        return obj.user.snippet_set.count()


    def get_user_detail(self, obj):
        return NameUserSerializer(obj).data