# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from pastebin.models import Snippet
from pastebin.serializers import SnippetModelSerializer

@csrf_exempt
@api_view(http_method_names=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def get_snippets(request, pk=None):
    if request.method.upper() == 'GET':
        if pk is not None:
            snippet = get_object_or_404(Snippet, pk=pk)
            serializer = SnippetModelSerializer(snippet)
        else:
            snippets = Snippet.objects.all()
            serializer = SnippetModelSerializer(snippets, many=True)

        return JsonResponse(serializer.data)

    if request.method.upper() == 'POST':
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.user = User.objects.get(pk=1)
            obj.save()
            serializer = SnippetModelSerializer(obj)
            return JsonResponse(serializer.data, status=201)

    if request.method.upper() in ['PUT', 'PATCH']:
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            obj = Snippet.objects.get(pk=pk)
            obj.title = request.data['title']
            obj.code = request.data['code']
            obj.lang = request.data['lang']
            obj.save()
            serializer = SnippetModelSerializer(obj)
        return JsonResponse(serializer.data, status=201)

    if request.method.upper() == "DELETE":
        obj = get_object_or_404(Snippet.objects.filter(pk=pk))
        obj.delete()
        return Response(status=204)

class SnippetView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            snippet = get_object_or_404(Snippet, pk=pk)
            serializer = SnippetModelSerializer(snippet)
        else:
            snippets = Snippet.objects.all()
            serializer = SnippetModelSerializer(snippets, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.user = User.objects.get(pk=1)
            obj.save()
            serializer = SnippetModelSerializer(obj)
            return JsonResponse(serializer.data, status=201)

    def put(self, request, pk, *args, **kwargs):
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            obj = Snippet.objects.get(pk=pk)
            obj.title = request.data['title']
            obj.code = request.data['code']
            obj.lang = request.data['lang']
            obj.save()
            serializer = SnippetModelSerializer(obj)
        return JsonResponse(serializer.data, status=201)

    def delete(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Snippet.objects.filter(pk=pk))
        obj.delete()
        return Response(status=204)

snippet_view = SnippetView.as_view()

class SnippetViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        snippet = get_object_or_404(Snippet, pk=pk)
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(serializer.data)

    def list(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    def update(self, request, pk=None):
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            obj = Snippet.objects.get(pk=pk)
            obj.title = request.data['title']
            obj.code = request.data['code']
            obj.lang = request.data['lang']
            obj.save()
            serializer = SnippetModelSerializer(obj)
        return JsonResponse(serializer.data, status=201)

    def destroy(self, request, pk):
        obj = get_object_or_404(Snippet.objects.filter(pk=pk))
        obj.delete()
        return Response(status=204)

detail_view = SnippetViewSet.as_view({'get': 'retrieve'})
list_view = SnippetViewSet.as_view({'get': 'list'})
update_view = SnippetViewSet.as_view({'put': 'update'})
delete_view = SnippetViewSet.as_view({'delete': 'destroy'})
