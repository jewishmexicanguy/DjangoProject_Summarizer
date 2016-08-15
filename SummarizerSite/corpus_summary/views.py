from django.shortcuts import render
from django.http import HttpResponse
from corpus_summary.forms import PostDocument
from corpus_summary.libros_epitome import summarize_from_raw_text
import json

# Create your views here.
def summarize(request):
    template_vars = {
        'form': PostDocument()
    }
    return render(request, "corpus_summary/summarize.html", template_vars)

def summarize_POST(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}
        response_data['result'] = 'Callback POST successful'
        response_data['summary'] = summarize_from_raw_text(post_text, 'this title')
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"Request Error": "HTTP verb not allowed"}),
            content_type = "application/json"
        )
