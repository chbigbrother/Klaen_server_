$(".send-data").on("click", function(){
    $("#SettingModal").modal('show');
});
var command_type = "create";

$(".editContBtn").on("click", function(target){
    var typeD = target.currentTarget.id.replace("edit_", "");
    var data = new Object();
    data.type = typeD;
    command_type = "update";
    $.ajax({
        url: "/scheduler/search/type/",
        method: "GET",
        data: data,
        datatype:'JSON',
        success: function(data){
            var d = JSON.parse(data)
            $("#timer").val(d[0].timer);
            $("#type").val(d[0].type);
        },
        error: function(error){
            console.log(error)
        }
    });

    $("#SettingModal").modal('show');
});

function saveSettings(){
    var setdata = new Object();
    var type = $(".type:selected").val();
    var timer = $("#timer").val();

    setdata.type = type;
    setdata.timer = timer;
    setdata.command_type = command_type;
    $.ajax({
        url: "/scheduler/save/settings/",
        data : JSON.stringify(setdata),
        type:'json',
        contentType: 'application/json',
        method: "POST",
        success: function(data){
            location.reload();
        },
        error: function(error){
            console.log(error)
        }
    });
}