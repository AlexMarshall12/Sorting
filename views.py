import re
import random
import transaction
import json 
import decimal
import math
from random import choice
from docutils.core import publish_parts
from pyramid.renderers import JSON
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.response import Response
from pyramid.view import view_config
from decimal import Decimal
from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.expression import func, select
from sqlalchemy import update 

from .models import (
    DBSession,
    Item,
    )

ranges={'o':(0,3), 'p':(0,3),'a':(0,3),'f':(0,3),'x':(0,3),'q':(0,3)}

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    
    session=DBSession()

    unicode_names=session.query(Item.name).all()
    unicode_values=session.query(Item.data).all()
    
    values=[]
    for i in range(len(unicode_names)):
        b=float(unicode_values[i][0])
        values.append("%0.2f" % (b-5))

    names=json.dumps(unicode_names)

    post_data=request.POST
    
    #if post_data.get('action') == "Submit2":
    if request.POST:
        name=request.params['name']
        data=request.params['data']
        url=request.params['url']
        item=Item(name,data,url)
        session.add(item)
        #ins=items.insert().values(name='',data='fill')
        return HTTPFound(location=request.route_url('home'))
    return {'names':names,'values':values}
    #return {}

@view_config(route_name='sorting', renderer='templates/sorting.pt')
def sorting(request):
    
    session=DBSession()

    if request.method == "GET":

    
        #length_table=session.query(func.count(Item.id)).scalar()
        #randoms=random.sample(range(1,length_table+1),2)
        #first=session.query(Item).order_by(Item.id).offset(random).first()
        #second=session.query(Item).order_by(Item.id).offset(random)
        #query1=session.query(Item).filter_by(id=randoms[0]+1)
        #results = session.query(Item).filter(Item.id.in_(randoms)).all()
        results = session.query(Item).order_by(func.random()).limit(2).all()
        #item1=query1.one()
        #query2=session.query(Item).filter_by(id=randoms[1]+1)
        #item2=query2.one()
        id1=results[0].id
        id2=results[1].id
        name1=results[0].name
        name2=results[1].name
        data1=results[0].data
        disp_data1="%0.2f" % (data1-5)
        data2=results[1].data
        disp_data2="%0.2f" % (data2-5)
        url1=results[0].url
        url2=results[1].url
        dist=(data2-data1)/400
        corr1=decimal.Decimal(math.exp(-((data1-10)**2)/3))
        corr2=decimal.Decimal(math.exp(-((data2-10)**2)/3))
        return {'disp_data1':disp_data1,'disp_data2':disp_data2, 'dist':dist,
        'id1':id1,'id2':id2,'results':results,
        'name1':name1,'name2':name2, 'data1':data1,'data2':data2, 'url1':url1,'url2':url2}
    if request.method == "POST":
        post_data=request.POST
        #output=post_data.get('myradio')
        key1=request.params['id1']
        key2=request.params['id2']
        #dist=float(request.params['dist'])
        data1=decimal.Decimal(request.params['data1'])
        data2=decimal.Decimal(request.params['data2'])
        dist=data2-data1
        corr1=decimal.Decimal(math.exp(-((data1-10)**2)/5))
        corr2=decimal.Decimal(math.exp(-((data2-10)**2)/5))
        randoms=[key1,key2]
        #results = session.query(Item).filter(Item.id.in_(randoms)).all()
        result1= session.query(Item).filter(Item.id==key1).one()
        result2= session.query(Item).filter(Item.id==key2).one()
        x=3
        print dist
        if request.params["form"] == "form1":
            result1.data=result1.data+(1-(1/(1+10**dist)))*corr1*x
            result2.data=result2.data+(0-(1/(1+10**(-1*dist))))*corr2*x
            return HTTPFound(location=request.route_url('sorting'))    
        if request.params["form"] == "form2":
            result1.data=result1.data+(0-(1/(1+10**dist)))*corr1*x
            result2.data=result2.data+(1-(1/(1+10**(-1*dist))))*corr2*x
            return HTTPFound(location=request.route_url('sorting'))  
    return {'results':results, 'randoms':randoms}







conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_sorting_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

