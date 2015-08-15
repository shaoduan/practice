from django.shortcuts import render

# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse
from .models import Question

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ','.join([p.question_text for p in latest_question_list]) 
#    return HttpResponse(output)

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('duan/index.html')
#    context = RequestContext(request, {
#        'latest_question_list': latest_question_list,
#    })
#    return HttpResponse(template.render(context))

def index(request):
    from django.shortcuts import render
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_question_list': latest_question_list }
    return render(request, 'duan/index.html', context)


#def detail(request, question_id): 
#    return HttpResponse("You're looking at question %s." % question_id)

#def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question Does Not Exist!")
#    return render(request, 'duan/detail.html', {'question': question} )

def detail(request, question_id):
    from django.shortcuts import get_object_or_404, render
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'duan/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s" % question_id )

def vote(request, question_id):
    return HttpResponse("You'r voting on question %s." % question_id)


