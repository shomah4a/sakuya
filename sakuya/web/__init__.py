#-*- coding:utf-8 -*-

from . import application



def app_factory(*argl, **argd):

    return application.make_application()



def main():

    from wsgiref import simple_server

    from sakuya.model import session

    session.initialize('sqlite:///data.db')

    app = app_factory()

    simple_server.make_server('', 8080, app).serve_forever()




if __name__ == '__main__':

    main()

