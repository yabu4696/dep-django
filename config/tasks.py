from datetime import datetime
from celery import shared_task
import time
from ca_camera.models import Wantoitem, Main, Sub, Item_maker

@shared_task
def form_celery():
    print('処理開始')
    new_item = Wantoitem.objects.all().latest('id')
    print('途中１')
    in_keyword,out_keyword = new_item.scraping()
    print('途中２')
    for main_url,main_list in in_keyword.items():
        Main.objects.create(wantoitem=new_item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
    for sub_url,sub_list in out_keyword.items():
        Sub.objects.create(wantoitem=new_item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
    print('処理完了')

@shared_task
def reload_celery(*args):
    reload_items = Wantoitem.objects.filter(pk__in=args)
    print('処理開始')
    for item in reload_items:
        Main.objects.filter(wantoitem=item).delete()
        Sub.objects.filter(wantoitem=item).delete()
        in_keyword,out_keyword = item.scraping()
        for main_url,main_list in in_keyword.items():
            Main.objects.create(wantoitem=item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
        for sub_url,sub_list in out_keyword.items():
            Sub.objects.create(wantoitem=item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
        item.save()
    print('処理完了')

@shared_task
def add(x1, x2):
	time.sleep(10)
	y = x1 + x2
	print('処理完了')
	return y
