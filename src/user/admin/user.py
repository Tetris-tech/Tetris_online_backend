from sqladmin import ModelView

from .. import models


class UserAdmin(ModelView, model=models.User):
    """Admin page for User model."""

    column_list = [
        models.User.id,
        models.User.username,
        models.User.rating,
        models.User.friends,
        models.User.added_by,
    ]
