from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import os


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
 
# FIX, CSRF FLAW: remove @csrf_exempt
@csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # FIX, BROKEN AUTHENTICATION FLAW: check if the user has already voted
    # if request.session.get(f'voted_{question.id}', False):
    #    return HttpResponseForbidden("You have already voted for this question.")
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        #BROKEN AUTHENTICATION FLAW:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        #FIX, BROKEN AUTHENTICATION FLAW: mark the question as voted in the session
        #request.session[f'voted_{question.id}'] = True

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

#XSS FLAW:
def question_xss(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # FIX, XSS FLAW: return render(request, "polls/detail.html", {"question": question})
    return HttpResponse(f"<h1>{question.question_text}</h1>")
    

#SENSITIVE DATA EXPOSURE FLAW
def sensitive_data(request):
    sensitive_info = {
        "secret_key" : "django-insecure-h@7zi!si72n5f+v%-!jr(b@02&+pxw50^s25q6^l&35j5-fv_#",
    }
    return HttpResponse(f"Secret Key: {sensitive_info['secret_key']}")

#FIX, SENSITIVE DATA EXPOSURE FLAW
#def sensitive_data(request):
    #secret_key = os.getenv('SECRET_KEY')
    #return HttpResponse("Sensitive information is securely stored.")

#CSRF FLAW
def malicious_page(request):
    return render(request, "polls/malicious.html")

