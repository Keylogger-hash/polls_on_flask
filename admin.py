from flask_admin.form import SecureForm
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.form import Select2Widget

#import app,db from __init__.py
from __init__ import app
from __init__ import db

from flask import url_for, redirect, request, abort
from models import Polls, Choice, User, Role

#flask login
from flask_login import current_user
import flask_login as login

#flask security
from flask_security import SQLAlchemyUserDatastore, Security

#flask admin
import flask_admin
from flask_admin import helpers, expose




#Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db,User,Role)
security = Security(app, user_datastore)

#create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return (current_user.is_active and
        current_user.is_authenticated and
        current_user.has_role('admin'))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login',next=request.url))


#Переадресация страниц (используется в шаблонах)
class MyAdminIndexView(flask_admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_page'))
        return super(MyAdminIndexView,self).index()

    @expose('/login/',methods=('GET','POST'))
    def login_page(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        return super(MyAdminIndexView,self).index()

    @expose('/logout/')
    def logout_page(self):
        login.logout_user()
        return redirect(url_for('.index'))

    @expose('/reset/')
    def reset_page(self):
        return redirect(url_for('.index'))


class AdminChoice(sqla.ModelView):
    form_base_class = SecureForm
    can_export = True
    column_hide_backrefs = False
    column_display_pk = True
    form_columns = ['choice_text','votes','question_id']
    list_columns = ['choice_text','votes','question_id']


class AdminPolls(sqla.ModelView):
    form_base_class = SecureForm
    can_export = True
    column_hide_backrefs = False
    form_columns = ['text','pub_date']
    list_columns = ['id','text','pub_date']

# class AdminPolls(ModelView):
#     column_display_pk = True # optional, but I like to see the IDs in the list
#     column_hide_backrefs = False
#     column_list = ('id', 'name', 'parent')
#     form_columns = ('id','tex)


admin = Admin(app, name="polls", index_view=MyAdminIndexView(), base_template='admin/master-extended.html',template_mode='bootstrap3')
admin.add_view(MyModelView(User,db.session))
admin.add_view(AdminPolls(Polls,db.session))
admin.add_view(AdminChoice(Choice,db.session))

@security.context_processor
def security_context_processor():
    return dict(
    admin_base_template=admin.base_template,
    admin_view=admin.index_view,
    h=helpers,
    get_url=url_for
    )

if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port='5002')
