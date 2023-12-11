from bronfood.core.useraccount.models import UserAccount, UserAccountManager


class RestaurantOwnerManager(UserAccountManager):

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=UserAccount.Role.OWNER)
        return queryset


class RestaurantOwner(UserAccount):
    """
    Модель для владельца ресторана 'RestaurantOwner'
    """
    class Meta:
        proxy = True

    objects = RestaurantOwnerManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Role.OWNER
        return super().save(*args, **kwargs)
