from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
import os
import pandas as pd

from .forms import BookForm
from .models import Book


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })

def avro_schema(request):
    # if request.method == 'POST':
    avro_str = None
    query_str = None
    for file in os.listdir('media/'):
        if file.endswith(".xlsx"):
            cols = pd.read_excel('media/'+file).columns
            avro_str = '''
{
"type": "record",
"name": "avro_schemma",
"fields":
[ 
'''
            query_str = '''
CREATE TABLE db.schemma_name.data_temp(
'''
            i = 0
            length = len(cols)
            for s in cols:
                for ch in ['\\','/','*','-','.',',','(',')']:
                    s = s.replace(ch,'')
                s = s.replace(r' ','_')
                i+=1
                if i < length:
                    avro_str = avro_str + '    { "name": "' + s + '", "type": ["null","string"]},' + '\n'
                    query_str = query_str + '    ' + s + '  VARCHAR(200),' + '\n'
                else:
                    avro_str = avro_str + '    { "name": "' + s + '", "type": ["null","string"]}' + '\n'
                    query_str = query_str + '    ' + s + '  VARCHAR(200)' + '\n'
            avro_str = avro_str + ''' ]
}'''
            query_str = query_str + ''')'''

    return render(request, 'avro_schema.html', {
    'avro_str': avro_str,
    'query_str': query_str
    })

def upsert(request):
    query_str1 = ''
    query_str2 = ''
    for file in os.listdir('media/'):
        if file.endswith(".xlsx"):
            cols = pd.read_excel('media/'+file).columns
            query_str = '''
INSERT INTO db.schemma_name.data_temp(
    SELECT
'''         
            on_consatrint = '''ON CONFLICT ON CONSTRAINT consatrint_name_key 
DO''' + '\n'
            i = 0
            length = len(cols)
            for s in cols:
                for ch in ['\\','/','*','-','.',',','(',')']:
                    s = s.replace(ch,'')
                s = s.replace(r' ','_')
                i+=1
                if i < length:
                    query_str1 = query_str1 + '       ' + s + ',' + '\n'
                    query_str2 = query_str2 + '       ' + s + ' = coalise.' + s + ',' + '\n'
                else:
                    query_str1 = query_str1 + '       ' + s + '\n'
                    query_str2 = query_str2 + '       ' + s + ' = coalise.' + s  + '\n'
                
            query_str1 = query_str1 + '     FROM db.schemma_name.data_temp' + ''')''' + '\n'

            query_str = query_str + query_str1 + on_consatrint + query_str2 

    return render(request, 'upsert.html', {
    'query_str': query_str
    })

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
