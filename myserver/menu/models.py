from django.db import models

# Create your models here.
class MenuLists(models.Model):
    menu_id = models.CharField(max_length=255, verbose_name='메뉴 아이디')
    menu_name = models.CharField(max_length=255, verbose_name='메뉴명')
    user_group = models.ForeignKey("account.UserGroup", on_delete=models.CASCADE, db_column="user_group_id",
                                   verbose_name='사용자 그룹')
    menu_parent = models.CharField(max_length=255, verbose_name='상위메뉴 PK')
    menu_link = models.CharField(max_length=255, verbose_name='메뉴 링크')
    menu_order = models.FloatField(null=True, verbose_name='메뉴 정렬 순서')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일자')

class MenuCheckLists(models.Model):
    menu_id = models.ForeignKey("MenuLists", on_delete=models.CASCADE, db_column="menu_id",
                                   verbose_name='메뉴 아이디')
    user_id = models.ForeignKey("account.User", on_delete=models.CASCADE, db_column="username",
                                   verbose_name='사용자 아이디')
    menu_yn = models.CharField(max_length=2, verbose_name='메뉴사용yn')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일자')