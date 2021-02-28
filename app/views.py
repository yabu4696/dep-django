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
    return render(request, 'app/index.html', {
         'items':items,
         'maker_list':maker_list
        })
    
def detail(request, slug):
    item = get_object_or_404(Wantoitem, slug=slug)
    main_lists = Main.objects.filter(wantoitem=item)
    sub_lists = Sub.objects.filter(wantoitem=item)
    return render(request, 'app/detail.html', {
        'item':item,
        'main_lists':main_lists,
        'sub_lists':sub_lists
        })

def maker_index(request):
    maker_list = Item_maker.objects.all()
    return render(request, 'app/maker_list.html', {
        'maker_list':maker_list
    })

def maker_detail(request, slug):
    maker = get_object_or_404(Item_maker, slug=slug)
    items = Wantoitem.objects.filter(maker_name=maker)
    return render(request, 'app/maker_detail.html', {
        'items':items,
        'maker':maker,
        })

def form(request):
    if not request.user.is_superuser:
        return redirect('app:index')
    else:
        if request.method == 'POST':
            form = WantoitemForm(request.POST)
            if form.is_valid():
                form.save()
                new_item = Wantoitem.objects.all().latest('id')
                in_keyword,out_keyword = new_item.scraping()
                for main_url,main_list in in_keyword.items():
                    Main.objects.create(wantoitem=new_item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
                for sub_url,sub_list in out_keyword.items():
                    Sub.objects.create(wantoitem=new_item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
            return redirect('app:index')
        else:
            form = WantoitemForm()
            return render(request, 'app/form.html',{'form':form})

def delete(request): 
    if not request.user.is_superuser:
        return redirect('app:index')
    else:
        if request.method == 'POST':    
            item_pks = request.POST.getlist('delete') 
            Wantoitem.objects.filter(pk__in=item_pks).delete()
            return redirect('app:index')
        else:
            items = Wantoitem.objects.all()
            return render(request, 'app/delete.html', {'items':items})



def reload(request):
    if not request.user.is_superuser:
        return redirect('app:index')
    else:
        if request.method == 'POST':
            item_pks = request.POST.getlist('reload') 
            reload_items = Wantoitem.objects.filter(pk__in=item_pks)
            for item in reload_items:
                Main.objects.filter(wantoitem=item).delete()
                Sub.objects.filter(wantoitem=item).delete()
                in_keyword,out_keyword = item.scraping()
                for main_url,main_list in in_keyword.items():
                    Main.objects.create(wantoitem=item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
                for sub_url,sub_list in out_keyword.items():
                    Sub.objects.create(wantoitem=item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
                item.save()
            return redirect('app:reload')
        else:
            items = Wantoitem.objects.all().order_by('maker_name')
            return render(request, 'app/reload.html', {'items':items})
            

def edit(request, slug):
    if not request.user.is_superuser:
        return redirect('app:detail', slug=slug)
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
            return redirect('app:detail', slug=slug)

        else:
            form = WantoitemForm(instance=item)
            return render(request, 'app/form.html',{'form':form})

def exclusion(request,slug):
    if not request.user.is_superuser:
        return redirect('app:detail', slug=slug)
    else:
        if request.method == 'POST':
            main_pks = request.POST.getlist('exclusion_main')
            exec_list_main = Main.objects.filter(pk__in=main_pks)
            for main in exec_list_main:
                domain_name = urlparse(main.main_url).netloc
                with open('./app/pattern/except_sub_list.txt', mode='a') as f:
                    f.write('\n'+domain_name)
            exec_list_main.delete()

            sub_pks = request.POST.getlist('exclusion_sub')
            exec_list_sub = Sub.objects.filter(pk__in=sub_pks)
            for sub in exec_list_sub:
                domain_name = urlparse(sub.sub_url).netloc
                with open('./app/pattern/except_sub_list.txt', mode='a') as f:
                    f.write('\n'+domain_name)
            exec_list_sub.delete()
            return redirect('app:detail',slug=slug)
        else:
            item = get_object_or_404(Wantoitem, slug=slug)
            main_list = Main.objects.filter(wantoitem=item)
            sub_list = Sub.objects.filter(wantoitem=item)
            return render(request, 'app/exclusion.html', {
                'item':item, 
                'main_list':main_list,
                'sub_list':sub_list
                })

def rayout(request):
    return render(request,'app/rayout_detail.html')



