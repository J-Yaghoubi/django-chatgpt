from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import environ
import openai

from config.settings import BASE_DIR
from .models import Chat


env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

openai.api_key = env('API_KEY', default='change_me')


def chat(request):
    chats = Chat.objects.all()
    ctx = {
        'chats': chats,
    }
    return render(request, 'chat.html', context=ctx)


@csrf_exempt
def ajax(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':   # Check if request is Ajax

        text = request.POST.get('text')

        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{text}"}]
        )
        response = res.choices[0].message["content"]

        Chat.objects.create(text=text, gpt=response)

        return JsonResponse({'data': response})
    return JsonResponse({})
