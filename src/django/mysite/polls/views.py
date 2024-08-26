from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    return render(
        request, "polls/index.html", {"latest_question_list": latest_question_list}
    )


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = Question(pk=question_id)
    return render(request, "results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    selected_choice = question.choice_set.get(pk=request.POST["choice"])

    return HttpResponseRedirect(reverse("results", args=(question.id,)))
