from django.http import response
from django.test import TestCase
from app.views import index
from django.urls import reverse,resolve
from django.shortcuts import render, redirect, get_object_or_404

class IndexTests(TestCase):
    def test_root_url_resolve_to_index_viewe(self):
        found = resolve('/app/')
        self.assertEqual(found.func, index)
    
    def test_index_returns_current_html(self):
        
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>WaNTo</title>', html)
        self.assertTrue(html.endwith('</html>'))  