from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .models import Topic,Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """显示所有主题"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

# def topic(request, topic_id):
#     topic = Topic.objects.get(id=topic_id)
#     entries = topic.entry_set.order_by('-date_added')
#     context = {'topic': topic, 'entries': entries}
#     return render(request, 'learning_logs/topics.html', context)
#       一定要小心拼写
@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if  request.method != 'POST':
        #未提交数据:创建一个新表单
        form = TopicForm()
    else:
        #POST提交的数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form }
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    """在特定的主题中添加条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
        form.save()
        return HttpResponseRedirect(reverse('learning_logs:topics', args=[topic_id]))
    context = {'topic': topic,'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request,entry_id):
    """编辑特定的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)







