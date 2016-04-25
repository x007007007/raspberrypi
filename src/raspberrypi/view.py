# -*- coding:utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse



class CamView(View):
    def get(self, request):
        return render('cam.html')

    def post(self, request):

        return JsonResponse()