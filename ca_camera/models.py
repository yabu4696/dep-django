from django.db import models

from . import def_chrome 

class Item_maker(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    meta_des = models.CharField(max_length=255,default='<meta name="description" content="カメラのレビューや評価サイトだけを表示したいというお悩みはありませんか？本サイトでは、カメラのレビューや評価サイトサイトだけを一覧表示！あなたに最適なアイテムを見つけてください。">')

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Wantoitem(models.Model):
    item_name = models.CharField(blank=True,null=True,max_length=255)
    maker_name = models.ForeignKey(Item_maker,on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=False, unique=True)
    # meta_des = models.CharField(blank=True,null=True,max_length=255)
            
    def __str__(self):
        return self.item_name

    def scraping(self):
        driver = def_chrome.make_driver()
        print('途中１-ドライバ初期設定')
        driver.get("https://google.com")
        kw_in_title_path = '/workspace/ca_camera/pattern/kw_in_title.txt'
        kw_out_title_path = '/workspace/ca_camera/pattern/kw_out_title.txt'
        kw_in_list = def_chrome.kw_in_title(kw_in_title_path)
        kw_out_list = def_chrome.kw_out_title(kw_out_title_path)
        search_word = self.maker_name.name+' AND '+self.item_name+' AND '+('({0})'+' -{1}').format(kw_in_list,kw_out_list)
        print('途中１-検索ワード')
        def_chrome.search(driver, search_word)
        print('途中１-ドライバー起動')
        except_file_main = '/workspace/ca_camera/pattern/except_main_list.txt'
        except_file_sub = '/workspace/ca_camera/pattern/except_sub_list.txt'
        contain_title = '/workspace/ca_camera/pattern/contain_title.txt'
        except_title = '/workspace/ca_camera/pattern/except_title.txt'

        in_keyword,out_keyword = def_chrome.get_url(driver,except_file_main,except_file_sub,contain_title,except_title)
        driver.close()
        return in_keyword,out_keyword

class Main(models.Model):
    wantoitem = models.ForeignKey(Wantoitem, on_delete=models.CASCADE) 
    main_url = models.URLField(max_length=200)
    main_title = models.CharField(max_length=255)
    main_ogp_img = models.URLField(max_length =200,blank=True,null=True)

class Sub(models.Model):
    wantoitem = models.ForeignKey(Wantoitem, on_delete=models.CASCADE)
    sub_url = models.URLField(max_length =200)
    sub_title = models.CharField(max_length=255)
    sub_ogp_img = models.URLField(max_length =200,blank=True,null=True)
