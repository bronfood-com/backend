from bronfood.core.useraccount.models import (
    UserAccount, UserAccountManager)


class ClientManager(UserAccountManager):

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=UserAccount.Role.CLIENT)
        return queryset


class Client(UserAccount):
    """ Модель Клиента"""
    class Meta:
        proxy = True
    objects = ClientManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Role.CLIENT
        return super().save(*args, **kwargs)
