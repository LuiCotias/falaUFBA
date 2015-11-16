# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
#http://hostname/app/default/index
#http://hostname/app/default/create_post/<category>
#http://hostname/app/default/edit_post/<category>/<id>
#http://hostname/app/default/list_post_by_datetime/<category>/<page>
#http://hostname/app/default/list_post_by_votes/<category>/<page>
#http://hostname/app/default/list_post_by_author/<user_id>/<page>
#http://hostname/app/default/view_post/<category>/<id>
#http://hostname/app/default/comm_vote_post/<comm_id>/<vote +1/-1>

POSTS_PER_PAGE = 10

def get_category():
    category_name = request.args(0)
    category = db.category(name=category_name)
    if not category:
        session.flash = 'pagina não encontrada'
        redirect(URL('index'))
    return category

def index():
    rows = db(db.category).select()
    return locals()

@auth.requires_login()
def create_post():
    category = get_category()
    db.post.category.default = category.id
    form = SQLFORM(db.post, labels={'title':'Título','url':'Link', 'body':'Texto'}).process(next='view_post/[id]')
    return locals()

@auth.requires_login()
def edit_post():
    id = request.args(0, cast=int)
    db.post.category.default = id
    form = SQLFORM(db.post, id, showid=False, labels={'title':'Título','url':'Link', 'body':'Texto'}).process(next='view_post/[id]')
    return locals()

def list_posts_by_datetime():
    response.view='default/list_posts_by_votes.html'
    category = get_category()
    page = request.args(1, cast=int, default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    rows = db(db.post.category==category.id).select(orderby=~db.post.created_on, limitby=(start,stop))
    return locals()

def list_posts_by_votes():
    category = get_category()
    page = request.args(1, cast=int, default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    rows = db(db.post.category==category.id).select(orderby=~db.post.votes, limitby=(start,stop))
    return locals()

def list_posts_by_author():
    response.view='default/list_posts_by_votes.html'
    user_id = request.args(0,cast=int)
    page = request.args(1, cast=int, default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    db(db.post.created_by==user_id).select(orderby=~db.post.created_on, limitby=(start,stop))
    return locals()

def view_post():
    id = request.args(0,cast=int)
    post = db.post(id) or redirect(URL('index'))
    comment = db(db.comm.post==post.id).select(orderby=~db.comm.created_on,limitby=(0,1)).first()
    #db.comm.parent_comm.default = comments.last() if comments else None
    if auth.user:
        db.comm.post.default = id
        db.comm.parent_comm.default = comment.id if comment else None
        form = SQLFORM(db.comm,labels={'body':'Comente aqui:'}).process()
    else:
        form = A('Voce precisa logar para comentar',_href=URL('user/login'),_class='btn btn-info')
    comments = db(db.comm.post==post.id).select(orderby=db.comm.created_on)
    return locals()

def vote_callback():
    vars = request.post_vars
    if vars and auth.user:
        id = vars.id
        direction = +1 if vars.direction == 'up' else -1
        post = db.post(id)
        if post:
            vote = db.vote(post=id,created_by=auth.user.id)
            if not vote:
                post.update_record(votes=post.votes+direction)
                db.vote.insert(post=id, score=direction)
            elif vote.score!=direction:
                post.update_record(votes=post.votes+direction*2)
                vote.update_record(score=direction)
            else:
                pass
#    return locals()
    return str(post.votes)

def comm_vote_callback():
    vars = request.post_vars
    if vars and auth.user:
        id = vars.id
        direction = +1 if vars.direction == 'up' else -1
        comm = db.comm(id)
        if comm:
            vote = db.comm_vote(comm=id,created_by=auth.user.id)
            if not vote:
                comm.update_record(votes=comm.votes+direction)
                db.comm_vote.insert(comm=id, score=direction)
            elif vote.score!=direction:
                comm.update_record(votes=comm.votes+direction*2)
                vote.update_record(score=direction)
            else:
                pass
        print comm.votes
#    return locals()
    return str(comm.votes)



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
