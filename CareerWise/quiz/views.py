from django.shortcuts import render
from django.http import JsonResponse
from .models import QuizQuestion


def startquiz(request):
    total_questions = QuizQuestion.objects.count()
    return render(request, 'quiz/startquiz.html', {'total_questions': total_questions})

def quiz_view(request):
    total_questions = QuizQuestion.objects.count()
    return render(request, 'quiz/quiz.html', {'total_questions': total_questions})

def quiz_data(request):
    quiz_questions = QuizQuestion.objects.all()
    data = [
        {
            'question': question.question,
            'options': [question.option1, question.option2, question.option3, question.option4],
            'answer': question.answer,
        }
        for question in quiz_questions
    ]
    return JsonResponse(data, safe=False)
