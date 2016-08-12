from django.shortcuts import render
from django.http import HttpResponse
from corpus_summary.forms import PostDocument

# Create your views here.
def summarize(request):
    #return HttpResponse('Hello, you have arrived.')

    template_vars = {
        'form': PostDocument()
    }
    return render(request, 'corpus_summary/summarize.html', template_vars)

def summarize_POST(request):
    pass