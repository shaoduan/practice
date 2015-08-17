from django.shortcuts import render

# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse
from .models import Question, Choice

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


#def results(request, question_id):
#    return HttpResponse("You're looking at the results of question %s" % question_id )

def results(request, question_id):
    from django.shortcuts import get_object_or_404, render
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'duan/results.html', {'question': question})

#def vote(request, question_id):
#    return HttpResponse("You'r voting on question %s." % question_id)


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'duan/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.object.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'duan/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'duan/results.html'



def vote(request, question_id):
    from django.shortcuts import get_object_or_404, render
    from django.http import HttpResponseRedirect, HttpResponse
    from django.core.urlresolvers import reverse

    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'duan/detail.html', { "question": p, "error_messege": "You did not select a choice.",  })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data. 
        # This prevernts data from being posted twice if user hits the Back button
        return HttpResponseRedirect(reverse('duan:results', args=(p.id,)))
