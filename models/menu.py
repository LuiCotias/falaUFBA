# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('fala UFBA!'),XML('&trade;&nbsp;'),_href=URL('index'),
                  _class="navbar-brand")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Luiz Mateus Cotias Simões <luicotias@gmail.com>'
response.meta.description = 'Rede Social para a comunidade acadêmica da UFBA'
response.meta.keywords = 'ufba, news, social'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    #(T('Home'), False, URL('default', 'index'), []),
]
for row in db(db.category).select():
    response.menu.append((T(row.name.title()),False, URL('default', 'list_posts_by_votes', args=row.name)))

if "auth" in locals(): auth.wikimenu()
