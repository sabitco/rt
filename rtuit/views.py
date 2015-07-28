# Create your views here.
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rtuit.models import Trend
from rtuit.models import Status
from rtuit.models import CandidateWords
from rtuit.forms import TrendForm
from django.views.generic.base import TemplateView
from rtuit.operations import operations
from collections import OrderedDict

class TrendSummaryView(TemplateView):
    template_name = "rtuit/summary.html"

    def get_context_data(self, **kwargs):
        context = super(TrendSummaryView, self).get_context_data(**kwargs)
        context['trend'] =Trend.objects(id=self.kwargs['pk'])[0]
        context['cantidad']= Status.objects.all().count()
        context['idf']= operations.calculateIdf()
        context['cantidad_status_list']= Status.objects(trend= context['trend'].name).count()           
        context['status_list']= Status.objects(trend= context['trend'].name)
        context['candidate_sumary']= operations.betterWords(CandidateWords.objects(trend= context['trend'].name))
        betterWords = dict()
        
        status = dict() 
        status_order = dict() 


        for lw in context['candidate_sumary']:
            betterWords = dict((sorted(lw.words.items(), key=lambda x: x[1], reverse=True)[:10]))

        ss = dict()
        for s in context['status_list']:
            ss[s.normalized] = s


        for s in ss.values():
            for k, v in betterWords.items():
                if k in s.normalized:
                    status[s.id_str] = v + status[s.id_str] if  s.id_str in status else v
    
        context['status_list']= Status.objects(id_str__in = sorted(status, key=lambda x: x[1], reverse=True)[:20]) 
        return context



class TrendAddTwitterView(TemplateView):
    template_name = "rtuit/add_twitter.html"

    def get_context_data(self, **kwargs):
        context = super(TrendAddTwitterView, self).get_context_data(**kwargs)
        messages.success(self.request, "Tistado guardado exitosamente.")
        return "listado guardado exitosamente."

class TrendInfoView(TemplateView):
    template_name = "rtuit/info.html"

class TrendListView(ListView):
    model = Trend
    context_object_name = "trend_list"
    
    def get_template_names(self):
        return ["rtuit/list.html"]

    def get_queryset(self):
        trends = Trend.objects
        if 'all_trends' not in self.request.GET:
            trends = trends.filter(is_published=True)
        return trends

class TrendCreateView(CreateView):
    model = Trend
    form_class = TrendForm

    def get_template_names(self):
        return ["rtuit/create.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        messages.success(self.request, "The trend has been created.")
        return super(TrendCreateView, self).form_valid(form)

class TrendDetailView(DetailView):
    model = Trend
    context_object_name = "trend"

    def get_template_names(self):
        return ["rtuit/detail.html"]

    def get_object(self):
        return Trend.objects(id=self.kwargs['pk'])[0]

class TrendUpdateView(UpdateView):
    model = Trend
    form_class = TrendForm
    context_object_name = "trend"

    def get_template_names(self):
        return ["rtuit/update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "The trend has been updated.")
        return super(TrendUpdateView, self).form_valid(form)

    def get_object(self):
        return Trend.objects(id=self.kwargs['pk'])[0]

class TrendDeleteView(DeleteView):
    model = Trend

    def get_success_url(self):
        return reverse('list')

    def get(self, *args, **kwargs):
        """ Skip confirmation page """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "The trend has been removed.")
        return redirect(self.get_success_url())

    def get_object(self):
        return Trend.objects(id=self.kwargs['pk'])[0]


