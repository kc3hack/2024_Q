# import flask_login
# import flask

# class User(flask_login.UserMixin):
#     def __init__(self, user_id):
#         self.id = user_id

#     def get_id(self):
#         return self.id

#     def is_active(self):
#         return True

#     def is_anonymous(self):
#         return False

#     @flask_login.LoginManager.user_loader
#     def load_user(user_id):
#         return User(user_id)

# 多分ゴミ