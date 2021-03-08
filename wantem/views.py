from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import WantoitemForm
from .models import Wantoitem, Main, Sub, Item_maker

# chrome関数
from . import def_chrome 
from urllib.parse import urlparse


def index(request):
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
    return render(request, 'wantem/index.html', {
         'items':items,
         'maker_list':maker_list
        })
    
def detail(request, slug):
    item = get_object_or_404(Wantoitem, slug=slug)
    main_lists = Main.objects.filter(wantoitem=item)
    sub_lists = Sub.objects.filter(wantoitem=item)
    return render(request, 'wantem/detail.html', {
        'item':item,
        'main_lists':main_lists,
        'sub_lists':sub_lists
        })

def maker_index(request):
    maker_list = Item_maker.objects.all()
    return render(request, 'wantem/maker_list.html', {
        'maker_list':maker_list
    })

def maker_detail(request, slug):
    maker = get_object_or_404(Item_maker, slug=slug)
    items = Wantoitem.objects.filter(maker_name=maker)
    return render(request, 'wantem/maker_detail.html', {
        'items':items,
        'maker':maker,
        })

from config.tasks import form_celery

def form(request):
    if not request.user.is_superuser:
        return redirect('wantem:index')
    else:
        if request.method == 'POST':
            form = WantoitemForm(request.POST)
            if form.is_valid():
                form.save()
                # new_item = Wantoitem.objects.all().latest('id')
                # in_keyword,out_keyword = new_item.scraping()
                # for main_url,main_list in in_keyword.items():
                #     Main.objects.create(wantoitem=new_item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
                # for sub_url,sub_list in out_keyword.items():
                #     Sub.objects.create(wantoitem=new_item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
                form_celery.apply_async()
            return redirect('wantem:index')
        else:
            form = WantoitemForm()
            return render(request, 'wantem/form.html',{'form':form})

def delete(request): 
    if not request.user.is_superuser:
        return redirect('wantem:index')
    else:
        if request.method == 'POST':    
            item_pks = request.POST.getlist('delete') 
            Wantoitem.objects.filter(pk__in=item_pks).delete()
            return redirect('wantem:index')
        else:
            items = Wantoitem.objects.all()
            return render(request, 'wantem/delete.html', {'items':items})

from config.tasks import reload_celery

def reload(request):
    if not request.user.is_superuser:
        return redirect('wantem:index')
    else:
        if request.method == 'POST':
            item_pks = request.POST.getlist('reload') 
            reload_items = Wantoitem.objects.filter(pk__in=item_pks)
            for item in reload_items:
                # Main.objects.filter(wantoitem=item).delete()
                # Sub.objects.filter(wantoitem=item).delete()
                # in_keyword,out_keyword = item.scraping()
                # for main_url,main_list in in_keyword.items():
                #     Main.objects.create(wantoitem=item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
                # for sub_url,sub_list in out_keyword.items():
                #     Sub.objects.create(wantoitem=item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
                # item.save()
                reload_celery.apply_async(item_pks)
            return redirect('wantem:reload')
        else:
            items = Wantoitem.objects.all().order_by('maker_name')
            return render(request, 'wantem/reload.html', {'items':items})
            

def edit(request, slug):
    if not request.user.is_superuser:
        return redirect('wantem:detail', slug=slug)
    else:
        item = get_object_or_404(Wantoitem,slug=slug)
        if request.method == 'POST':
            form = WantoitemForm(request.POST,instance=item)
            if form.is_valid():
                form.save()
                edit_item = get_object_or_404(Wantoitem,slug=slug)
                Main.objects.filter(wantoitem=item).delete()
                Sub.objects.filter(wantoitem=item).delete()
                in_keyword,out_keyword = edit_item.scraping()
                for main_url,main_list in in_keyword.items():
                    Main.objects.create(wantoitem=edit_item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
                for sub_url,sub_list in out_keyword.items():
                    Sub.objects.create(wantoitem=edit_item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
            return redirect('wantem:detail', slug=slug)

        else:
            form = WantoitemForm(instance=item)
            return render(request, 'wantem/form.html',{'form':form})

def exclusion(request,slug):
    if not request.user.is_superuser:
        return redirect('wantem:detail', slug=slug)
    else:
        if request.method == 'POST':
            main_pks = request.POST.getlist('exclusion_main')
            exec_list_main = Main.objects.filter(pk__in=main_pks)
            for main in exec_list_main:
                domain_name = urlparse(main.main_url).netloc
                with open('/workspace/wantem/pattern/except_sub_list.txt', mode='a') as f:
                    f.write('\n'+domain_name)
            exec_list_main.delete()

            sub_pks = request.POST.getlist('exclusion_sub')
            exec_list_sub = Sub.objects.filter(pk__in=sub_pks)
            for sub in exec_list_sub:
                domain_name = urlparse(sub.sub_url).netloc
                with open('/workspace/wantem/pattern/except_sub_list.txt', mode='a') as f:
                    f.write('\n'+domain_name)
            exec_list_sub.delete()
            return redirect('wantem:detail',slug=slug)
        else:
            item = get_object_or_404(Wantoitem, slug=slug)
            main_list = Main.objects.filter(wantoitem=item)
            sub_list = Sub.objects.filter(wantoitem=item)
            return render(request, 'wantem/exclusion.html', {
                'item':item, 
                'main_list':main_list,
                'sub_list':sub_list
                })

def rayout(request):
    return render(request,'wantem/rayout_detail.html')


from celery.result import AsyncResult

from config.tasks import add

def celery_test(request):
	task_id = add.delay(5, 5)

	result = AsyncResult(task_id)
	print('result:', result, ' : ', result.state, ' : ', result.ready())

	context = {'result': result}

	return render(request, 'wantem/celery-test.html', context)