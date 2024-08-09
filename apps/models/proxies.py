from apps.models.users import User


class CustomerUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class AuthorUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

class ModeratorUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Moderator'
        verbose_name_plural = 'Moderators'