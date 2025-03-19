from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.http import JsonResponse
from home.agent import agent
from asgiref.sync import async_to_sync
from home.gemini import interact_with_agent


def home(request):
    return render(request,'home.html')



@login_required
def chat(request):
    if request.method =="POST":
        try:    
            data = json.loads(request.body)  
            user = request.user.username
            question = data.get("query") 
            if not question:
                return JsonResponse({"error": "No question provided"}, status=400)

            if question.lower() == "error":
                return JsonResponse({"error": "Error occurred!"}, status=400)

            response_text = f"{interact_with_agent(question)}"

            return JsonResponse({"response": response_text})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
def logout_request(request):
    logout(request)
    return redirect('/')


