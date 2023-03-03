from menu.models import MenuLists, MenuCheckLists

def menu_list(request):
    user_id = request.session.get('user')
    menus = MenuCheckLists.objects.filter(user_id_id=user_id).order_by('id')
    menu_result = []
    menu_dict = {}
    cnt = 0
    for i in menus:
        cnt += 1
        menu_dict[cnt] = i.menu_yn
    menu_result.append(menu_dict)
    return {
        "menus" : menu_result
    }