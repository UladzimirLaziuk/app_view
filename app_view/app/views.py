from django.db.models import Q
from django.views.generic import ListView, DetailView

from app.models import ProgramModel, Score
# Create your views here.
from rest_framework.generics import CreateAPIView

from app.serializers import ProgramModelSerializer


class CreateModel(CreateAPIView):
    queryset = ProgramModel.objects.all()
    serializer_class = ProgramModelSerializer



class ScoreListView(ListView):
    template_name = 'score.html'
    model = Score
    queryset = Score.objects.all()[:50]

class ScoreDetailView(DetailView):
    model =  Score
    template_name = 'score_detail.html'

class SearchResultsView(ListView):
    model = Score
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get("query")
        object_list = Score.objects.filter(
            Q(name__icontains=query) | Q(vendor__icontains=query)
        )
        return object_list

