from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, View
from django.contrib.contenttypes.models import ContentType

from jokes.models import Joke
from jokes.forms import JokeForm

from comments.models import Comment
from comments.forms import CommentForm


class JokeList(ListView):
    queryset = Joke.objects.all()
    template_name = 'jokes/jokes.html'
    context_object_name = 'jokes'

#
# class JokeDisplay(DetailView):
#     queryset = Joke.objects.all()
#     template_name='jokes/jokes_detail.html'
#     context_object_name='joke'


#     def get_context_data(self,*args,**kwargs):
#         context = super().get_context_data(**kwargs)#current context
#         joke = self.get_object() #the current joke
#         # context['comments'] = Comment.objects.filter_comments_by_joke(joke) #pass additional context
#         context['comments'] = joke.comments #another way of saying above using propert methods.
#         context['form'] = CommentForm #another way of saying above using propert methods.
#         return context

# class JokeComment(FormView):
#     form_class=CommentForm
#     template_name='jokes/jokes_detail.html'
#     joke_instance=Joke.objects.get(id)
#     # initial={

#     # }


#     def get_initial(self):
#         initial = super().get_initial()
#         joke_instance=Joke.objects.get(pk=self.kwargs['pk'])
#         initial['content_type'] = joke_instance.get_content_type
#         initial['object_id'] = joke_instance.pk
#         # initial.update({'content_type': joke_instance.get_content_type,
#         #                 'object_id':joke_instance.id})


#         # return self.initial.copy()
#         return initial


#     def form_valid(self,form):
#         c_type = form.cleaned_data.get(content_type=self.kwargs['content_type'])
#         print(c_type)
#         content_type = ContentType.objects.get(model=c_type)
#         obj_id = form.cleaned_data.get(object_id=self.kwargs['object_id'])
#         content_data = form.cleaned_data.get(content=self.kwargs['content'])
#         new_comment = Comment.objects.create(
#                                     user=self.request.user,
#                                     content_type=content_type,
#                                     object_id=obj_id,
#                                     content=content_data )
#         form.save()
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('jokes_detail',kwargs={'pk':self.kwargs['pk']})


# class JokeDetail(View):

#     def get(self,request,*args,**kwargs):
#         view = JokeDisplay.as_view()
#         return view(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         view =JokeComment.as_view()
#         return view(request,*args,**kwargs)

# # class JokeDetail(View):

# #     def get(self,request,pk,*args,**kwargs):
# #         joke =get_object_or_404(Joke,pk=pk)
# #         comments= joke.comments
# #         initial_data ={
# #             'content_type':joke.get_content_type,
# #             'object_id':joke.id
# #         }
# #         form = CommentForm(initial=initial_data)
# #         return render(request,'jokes/jokes_detail.html',{'joke':joke,'comments':comments,'form':form,})

# #     def post(self,request,*args,**kwargs):

# #         form=CommentForm(data=request.POST)
# #         print(form)
# #         if form.is_valid():
# #             c_type = form.cleaned_data.get('content_type')
# #             print(c_type)
# #             content_type = ContentType.objects.get(model=c_type)
# #             obj_id = form.cleaned_data.get('object_id')
# #             content_data = form.cleaned_data.get('content')
# #             new_comment = Comment.objects.create(
# #                                     user=self.request.user,
# #                                     content_type=content_type,
# #                                     object_id=obj_id,
# #                                     content=content_data )
# #             form.save()





def joke_detail(request, pk=None):
    instance = get_object_or_404(Joke, pk=pk)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        content_type = ContentType.objects.get(model='joke')
        obj_id = instance.id
        content_data = form.cleaned_data.get("content")
        parent_obj= None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id=None

        if parent_id:
            parent_qs= Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() ==1:
                parent_obj = parent_qs.first()
        
        new_comment = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj
        )        


    form = CommentForm()

    comments = instance.comments
    context = {
        "joke": instance,
        "comments": comments,
        "form": form,
    }
    return render(request, "jokes/jokes_detail.html", context)
