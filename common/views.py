from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)


class BaseListView(ListView):
    paginate_by = 10


class BaseCreateView(CreateView):
    success_url = None

    def get_success_url(self):
        return self.success_url


class BaseDetailView(DetailView):
    pass


class BaseUpdateView(UpdateView):
    success_url = None

    def get_success_url(self):
        return self.success_url


class BaseDeleteView(DeleteView):
    success_url = None

    def get_success_url(self):
        return self.success_url

