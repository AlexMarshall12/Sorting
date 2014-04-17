from pyramid.config import Configurator
from sqlalchemy import engine_from_config
#from pyramid import JSON
from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from pyramid.settings import asbool
    if asbool(settings.get('env.use_env_variables', False)):
        from os import getenv
        settings['sqlalchemy.url'] = getenv(settings['sqlalchemy.url'])
 
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    #json_renderer=JSON()
    #def decimal_adapter(obj, request):
     #   return string
    #json_renderer.add_adapter(decimal.decimal, decimal_adapter)
    #config.add_renderer('json',json_renderer)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('sorting','/sorting')
    config.scan()
    
    
    return config.make_wsgi_app()

