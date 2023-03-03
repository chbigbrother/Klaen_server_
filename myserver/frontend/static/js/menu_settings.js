
$('.form-check-input').on('click', function(target){

    var menu_id = target.currentTarget.className.split(' ')[1];
    var menu_yn = target.currentTarget.className.split(' ')[2];

    var obj = new Object();
    obj.menu_id = menu_id;
    obj.menu_yn = menu_yn;
    $.ajax({
        url: "/menu/setting/modify/",
        datatype:'JSON',
        data: obj,
        method: "POST",
        success: function(data){
            location.reload();
        },
        error: function(error){
            console.log(error)
        }

    });


})