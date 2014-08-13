# -*- coding: utf-8 -*-
import pytest

from collections import defaultdict

from mfr.core import RenderResult, assets_by_extension

@pytest.fixture
def html():
    return '<p>Hello</p>'

def test_basic_init(html):
    css = ['/static/style.css']
    rr = RenderResult(html, assets={'css': css})
    assert rr.content == html
    assert rr.assets['css'] == css


def test_init_with_list(html):
    rr = RenderResult(html, assets=['/static/style.css', '/static/script.js'])

    assert rr.content == html
    assert rr.assets['css'] == ['/static/style.css']
    assert rr.assets['js'] == ['/static/script.js']
    assert rr.assets['notfound'] == []


def test_assets_by_extension():
    result = assets_by_extension(['/static/style.css',
        '/static/style2.css', '/static/script.js'])
    assert result['css'] == ['/static/style.css', '/static/style2.css']
    assert result['js'] == ['/static/script.js']

def test_init_with_only_html(html):
    rr = RenderResult(html)
    assert rr.assets == {}
    assert isinstance(rr.assets, defaultdict)

def test_init_with_dict():
    rr = RenderResult(html, assets={'css': ['style.css']})
    assert isinstance(rr.assets, defaultdict)

def test_str(html):
    rr = RenderResult(html)
    assert str(rr) == html

def test_repr():
    rr = RenderResult('foo')
    assert repr(rr) == '<RenderResult({0!r})>'.format('foo')

def test_in():
    rr = RenderResult('foo bar baz')
    assert 'bar' in rr

def test_unicode():
    rr = RenderResult('foo')
    assert str(rr) == str('foo')
