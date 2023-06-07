from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from answer_generator import chat_generator

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        state = data['state']
        if state == "problem_solved":
            return JsonResponse({"answer": "Das freut mich sehr! Kann ich Ihnen sonst noch helfen?"})
        elif state == "unabled":
            return JsonResponse({"answer": "Es tut mir leid, dass ich Ihnen nicht helfen kann, aber die Infrastrukturabteilung wird Ihnen gerne helfen, rufen Sie xxx xxx xxx an oder schreiben Sie eine E-Mail an infrastructure_and_hardware@it_solutions.com und sie werden Ihnen sofort helfen."})
        else:
            input = data['input']
            response = chat_generator.process_input(input, state)
            return JsonResponse(response)

