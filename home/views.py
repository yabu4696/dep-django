from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import ContactForm
from .models import Item_category

from django.http import HttpResponse
from django.conf import settings
import textwrap
from django.core.mail import BadHeaderError, EmailMessage

def index(request):
    return render(request, 'home/index.html')

def category(request):
    categories = Item_category.objects.all()
    query = request.GET.get('query')
    if query:
        categories = categories.filter(
            Q(name__icontains=query)
        ).distinct()
    return render(request, 'home/category-list.html', {
        'categories':categories,
    })

def contact(request):
  form = ContactForm(request.POST or None)
  if form.is_valid():
     name = form.cleaned_data['name']
     message = form.cleaned_data['message']
     email = form.cleaned_data['email']
     subject = 'お問い合わせありがとうございます。'
     contact = textwrap.dedent('''
        ※このメールはシステムからの自動返信です。

        {name} 様
        
        お問い合わせありがとうございます。
        以下の内容でお問い合わせを受け付けました。
        内容を確認させていただき、ご返信させていただきますので、少々お待ちください。

        ----------------------------------

        ・お名前
        {name}

        ・メールアドレス
        {email}

        ・メッセージ
        {message}
        
        -----------------------------------
        WEB: https://wanto-item.com/
     ''').format(
        name=name,
        email=email,
        message=message
     )
     to_list = [email]
     bcc_list = [settings.EMAIL_HOST_USER]
     try:
        message = EmailMessage(subject=subject, body=contact, to=to_list, bcc=bcc_list)
        message.send()
     except BadHeaderError:
        return HttpResponse('無効なヘッダが検出されました。')
     return redirect('home:done')

  return render(request, 'home/contact.html',{'form': form})

def done(request):
   return render(request, 'home/done.html')