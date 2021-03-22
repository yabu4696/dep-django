from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import ContactForm
from .models import Wantoitem, Main, Sub, Item_maker

from django.http import HttpResponse
from django.conf import settings
import textwrap
from django.core.mail import BadHeaderError, EmailMessage

# chrome関数
from . import def_chrome 
from urllib.parse import urlparse

def index(request):
    return render(request, 'ca_camera/index.html')
    
def preturn(request):
    return render(request, 'ca_camera/preturn.html')

def detail(request, slug):
    item = get_object_or_404(Wantoitem, slug=slug)
    main_lists = Main.objects.filter(wantoitem=item)
    sub_lists = Sub.objects.filter(wantoitem=item)
    return render(request, 'ca_camera/detail.html', {
        'item':item,
        'main_lists':main_lists,
        'sub_lists':sub_lists
        })

def maker_index(request):
    maker_list = Item_maker.objects.all()
    return render(request, 'ca_camera/maker_list.html', {
        'maker_list':maker_list
    })

def maker_detail(request, slug):
    maker = get_object_or_404(Item_maker, slug=slug)
    items = Wantoitem.objects.filter(maker_name=maker)
    return render(request, 'ca_camera/maker_detail.html', {
        'items':items,
        'maker':maker,
        })

def search_result(request):
    items = Wantoitem.objects.all().order_by('maker_name')
    maker_list = Item_maker.objects.all()
    query = request.GET.get('query')
    if query:
        items = items.filter(
        Q(item_name__icontains=query)|
        Q(maker_name__name__icontains=query)
        ).distinct()
        maker_lists = items.values_list('maker_name__name', flat=True)
        maker_list = maker_list.filter(name__in=maker_lists)
    return render(request, 'ca_camera/search_result.html', {
         'items':items,
         'maker_list':maker_list
        })

def delete(request): 
    if not request.user.is_superuser:
        return redirect('ca_camera:index')
    else:
        if request.method == 'POST':    
            item_pks = request.POST.getlist('delete') 
            Wantoitem.objects.filter(pk__in=item_pks).delete()
            return redirect('ca_camera:index')
        else:
            items = Wantoitem.objects.all()
            return render(request, 'ca_camera/delete.html', {'items':items})

def exclusion(request,slug):
    if not request.user.is_superuser:
        return redirect('ca_camera:detail', slug=slug)
    else:
        if request.method == 'POST':
            main_pks = request.POST.getlist('exclusion_main')
            exec_list_main = Main.objects.filter(pk__in=main_pks)
            for main in exec_list_main:
                domain_name = urlparse(main.main_url).netloc
                if 'www' in domain_name:
                    domain_name = domain_name.replace('www', '')
                with open('./ca_camera/pattern/except_sub_list.txt', mode='a') as f:
                    f.write('\n'+domain_name)
            exec_list_main.delete()

            sub_pks = request.POST.getlist('exclusion_sub')
            exec_list_sub = Sub.objects.filter(pk__in=sub_pks)
            for sub in exec_list_sub:
                domain_name = urlparse(sub.sub_url).netloc
                with open('./ca_camera/pattern/except_sub_list.txt', mode='a') as f:
                    f.write('\n'+domain_name)
            exec_list_sub.delete()
            return redirect('ca_camera:detail',slug=slug)
        else:
            item = get_object_or_404(Wantoitem, slug=slug)
            main_list = Main.objects.filter(wantoitem=item)
            sub_list = Sub.objects.filter(wantoitem=item)
            return render(request, 'ca_camera/exclusion.html', {
                'item':item, 
                'main_list':main_list,
                'sub_list':sub_list
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
     return redirect('ca_camera:done')

  return render(request, 'ca_camera/contact.html',{'form': form})

def done(request):
   return render(request, 'ca_camera/done.html')
