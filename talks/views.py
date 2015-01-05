from __future__ import absolute_import
from braces import views
from django.views import generic
from . import models
from .forms import TalkForm, TalkListForm
from django.shortcuts import redirect
from django.http import HttpResponse


class RestrictToUserMixin(views.LoginRequiredMixin):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class TalkListListView(RestrictToUserMixin, generic.ListView):
    model = models.TalkList

    def get_queryset(self):
        return self.request.user.lists.all()

class TalkListDetailView(
    RestrictToUserMixin,
    views.PrefetchRelatedMixin,
    generic.DetailView
):
    model = models.TalkList
    prefetch_related = ('talks',)
    form_class = TalkForm
    http_method_names = ['get', 'post']
    def get_context_data(self, **kwargs):
        context = super(TalkListDetailView, self).get_context_data(**kwargs)
        context.update({'form': self.form_class(self.request.POST or None)})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = self.get_object()
            talk = form.save(commit=False)
            talk.talk_list = obj
            talk.save()
        else:
            return self.get(request, *args, **kwargs)
        return redirect(obj)




class TalkListCreateView(
     views.LoginRequiredMixin,
     views.SetHeadlineMixin,
     generic.CreateView
 ):
     form_class = TalkListForm
     headline = 'Create'
     model = models.TalkList

     def form_valid(self, form):
         self.object = form.save(commit=False)
         self.object.user = self.request.user
         self.object.save()
         return super(TalkListCreateView, self).form_valid(form)



class TalkListUpdateView(

    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.UpdateView
):
    form_class = TalkListForm
    headline = 'Update'
    model = models.TalkList



