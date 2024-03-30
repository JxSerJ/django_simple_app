from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    response_text = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Main page</title>
</head>
<body>
<h1>Django simple project</h1>
<p>Hello World!</p>
<br><br><br>
<p>Stack:</p>
<ul>
  <li>Python 3.12.3</li>
  <li>Django 5.0</li>
  <li>SQLite3</li>
</ul>
</body>
</html>
    """
    return HttpResponse(response_text)


def about(request):
    response_text = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>About</title>
</head>
<body>
<h1>About page</h1>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing
    elit. Ad cupiditate doloribus ducimus nam provident quo similique! Accusantium
    aperiam fugit magnam quas reprehenderit sapiente temporibus voluptatum!</p>
</body>
</html>
"""
    return HttpResponse(response_text)
