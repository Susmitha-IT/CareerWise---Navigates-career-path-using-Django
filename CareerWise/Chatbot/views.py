from django.shortcuts import render

def startchat(request):
    return render(request, 'Chatbot/chat.html')
