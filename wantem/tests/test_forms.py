from django.test import TestCase
from app.models import Wantoitem,Main,Except
from app.forms import WantoitemForm



class WantoitemTests(TestCase):
    def test_form(self):
        item = dict(item_name='apple')
        form = WantoitemForm(item)
        self.assertTrue(form.is_valid())
        
    
        


