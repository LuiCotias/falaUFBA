# -*- coding: utf-8 -*-

db.define_table('category', Field('name', requires=(IS_SLUG(),IS_LOWER(),IS_NOT_IN_DB(db,'category.name'))))

db.define_table('post',
                Field('category', 'reference category', readable=False, writable=False),
                Field('title', 'string', requires=IS_NOT_EMPTY()),
                Field('url', requires=IS_EMPTY_OR(IS_URL())),
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                Field('votes','integer', default=0,readable=False, writable=False),
                auth.signature)

db.define_table('vote',
                Field('post','reference post'),
                Field('score','integer', default=+1),
                auth.signature)

db.define_table('comm',
                Field('post','reference post',readable=False, writable=False),
                Field('parent_comm','reference comm',readable=False, writable=False),
                Field('votes','integer',default=0,readable=False, writable=False),
                Field('body','text'),
                auth.signature)


db.define_table('comm_vote',
                Field('comm','reference comm'),
                Field('score','integer', default=+1),
                auth.signature)

def author(id):
    if id is None:
        return 'Desconhecido'
    else:
        user = db.auth_user(id)
        return A('%(first_name)s %(last_name)s' % user, _href=URL('list_posts_by_author', args=user.id))


#from gluon.contrib.populate import populate
#if db(db.auth_user).count()<2:
#    populate(db.auth_user,100)
#    db.commit()
#if db(db.post).count()<2:
#    populate(db.post,500)
#    db.commit()
#db(db.post.id>1).delete()
#db(db.auth_user.id>1).delete()
#db(db.comm.id>1).delete()
#if db(db.comm).count()<2:
#    populate(db.comm,300)
#    db.commit()
