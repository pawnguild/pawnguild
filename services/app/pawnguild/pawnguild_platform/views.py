from django.views.generic.edit import View
from django.shortcuts import render

class Home(View):
    
    def get(self, request):
        context = {}
        return render(
            request, "pawnguild_platform/home.html", context=context
        )
