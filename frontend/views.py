from django.shortcuts import render

from django.views import View

class LandingPage(View):
    def get(self, request):
        context = {}
        return render(
            request=request,
            template_name='frontend/landing_page.html',
            context=context
        )
