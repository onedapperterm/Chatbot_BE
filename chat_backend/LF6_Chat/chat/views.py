from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from answer_generator import chat_generator

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        input = data['input']
        state = data['state']
        response = chat_generator.process_input(input, state)
        return JsonResponse(response)

