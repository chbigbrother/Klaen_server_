function pm10Chart(type){
    var ctx = document.getElementById("myAreaChart");
    var dataset = new Array();
    var humdata = new Array();
    var tempdata = new Array();
    var dustdata = new Array();
    var labels = new Array();
    var timestamps = new Array();
    var backgroundColor = [
      'rgba(245, 238, 248)',
      'rgba(215, 189, 226)',
      'rgba(169, 204, 227)',
      'rgba(127, 179, 213)',
      'rgba(163, 228, 215)',
      'rgba(118, 215, 196)',
      'rgba(171, 235, 198)',
      'rgba(130, 224, 170)',
      'rgba(249, 231, 159)',
      'rgba(248, 196, 113)',
    ];
    var borderColor = [
      'rgba(245, 238, 248)',
      'rgba(215, 189, 226)',
      'rgba(169, 204, 227)',
      'rgba(127, 179, 213)',
      'rgba(163, 228, 215)',
      'rgba(118, 215, 196)',
      'rgba(171, 235, 198)',
      'rgba(130, 224, 170)',
      'rgba(249, 231, 159)',
      'rgba(248, 196, 113)',
    ];
    $.ajax({
        url:  "/sensor/dust/data/",
        method: 'GET',
        dataType: 'json',
        async: false,
        contentType: 'application/json',
        processData: false,
        success: function(result) {
            for (var i = 0; i < result.length; i++) {
                humdata.push(result[i].humidity);
                tempdata.push(result[i].temperature);
                dustdata.push(result[i].dustDensity);

                timestamps.push(result[i].timestamp);
            }

            dataset.push({
                    backgroundColor: "pink",
                    label: "humidity",
                    responsive: true,
                    pointRadius: 0,
                    data: humdata,
                    borderWidth: 3,
                    borderColor: "pink",
            });

            dataset.push({
                    backgroundColor: "lightblue",
                    label: "temperature",
                    responsive: true,
                    pointRadius: 0,
                    data: tempdata,
                    borderWidth: 3,
                    borderColor: "lightblue",
            });

            dataset.push({
                    backgroundColor: "lightgreen",
                    label: "dust",
                    responsive: true,
                    pointRadius: 0,
                    data: dustdata,
                    borderWidth: 3,
                    borderColor: "lightgreen",
            });

            const config = new Chart(ctx, {
                type: type,
                data: {
                    labels: timestamps,
                    datasets: dataset
                },
                options: {
                    scales: {
                          y: {
                                beginAtZero: true
                          }
                    },

                },
            });
        }

    });
}
function pm10Pie(){
    var ctx = document.getElementById("myPieChart");
    var dataset = new Array();
    var data = new Array();
    var labels = new Array();
    var backgroundColor = [
      'rgba(245, 238, 248)',
      'rgba(215, 189, 226)',
      'rgba(169, 204, 227)',
      'rgba(127, 179, 213)',
      'rgba(163, 228, 215)',
      'rgba(118, 215, 196)',
      'rgba(171, 235, 198)',
      'rgba(130, 224, 170)',
      'rgba(249, 231, 159)',
      'rgba(248, 196, 113)',
    ];
    var borderColor = [
      'rgba(245, 238, 248)',
      'rgba(215, 189, 226)',
      'rgba(169, 204, 227)',
      'rgba(127, 179, 213)',
      'rgba(163, 228, 215)',
      'rgba(118, 215, 196)',
      'rgba(171, 235, 198)',
      'rgba(130, 224, 170)',
      'rgba(249, 231, 159)',
      'rgba(248, 196, 113)',
    ];
    $.ajax({
        url:  "/scheduler/time/",
        method: 'GET',
        dataType: 'json',
        async: false,
        contentType: 'application/json',
        processData: false,
        success: function(result) {

            result = result['data']
            for (var i = 0; i < result.length; i++) {
                data.push(result[i].pm10);
                labels.push(result[i].site);
            }

            dataset.push({
                    backgroundColor: backgroundColor,
                    responsive: true,
                    pointRadius: 0,
                    borderColor:borderColor,
                    data: data,
                    borderWidth: 1
            });
            const config = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels:labels,
                    datasets: dataset
                },
                options: {
                maintainAspectRatio: false,
                tooltips: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  borderColor: '#dddfeb',
                  borderWidth: 1,
                  xPadding: 15,
                  yPadding: 15,
                  displayColors: false,
                  caretPadding: 10,
                },
                legend: {
                  display: false
                },
                cutoutPercentage: 80,
              },
            });
        }
    });

}

/*
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/post/airquality/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
*/

$('.send-new-email').on('click', function(){
    $('#modal-report').modal('show');
});

$('.send-email-btn').on('click', function(){

    var obj = new Object();
    obj.to = $('.email-to').val();
    obj.message = $('.email-contents').val();
    obj.subject = $('.subject-title').val();
    console.log(obj);
    $.ajax({
        url: "/sensor/anomaly/email/",
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

});

$('.form-selectgroup-input').on('click', function(target){
    var obj = new Object();
    obj.on_off = target.currentTarget.defaultValue;
    $.ajax({
        url: "/sensor/dust/switch/modify/",
        datatype:'JSON',
        data: obj,
        method: "POST",
        success: function(data){

        },
        error: function(error){
            console.log(error)
        }

    });
})
switches();
function switches(){
    $.ajax({
        url: "/sensor/dust/switch/get/",
        method: 'GET',
        dataType: 'json',
        async: false,
        contentType: 'application/json',
        processData: false,
        success: function(data){
            for(var i=0; i<data.length; i++){
                $('input:radio[name=dust-icons]:input[value='+ data[i].dust +']').attr("checked",true);
                $('input:radio[name=temp-icon]:input[value='+ data[i].temp +']').attr("checked",true);
                $('input:radio[name=hum-icon]:input[value='+ data[i].hum +']').attr("checked",true);
                $('input:radio[name=light-icons]:input[value='+ data[i].lighting +']').attr("checked",true);
            }
        },
        error: function(error){
            console.log(error)
        }

    });
}

$('.chartSelect').on('change', function(e){
    var type = $('.chartSelect').val();
    $('#myAreaChart').remove(); // this is my <canvas> element
    $('.chart-selections').append('<canvas id="myAreaChart" class="chartjs-render-monitor" width="1606px" height="318px"></canvas>');
    pm10Chart(type);
//    if(type=='bar'){
//
//    } else{
//        setInterval(function () {pm10Chart();
//        pm10Pie();}, 3600000);//request every x seconds
//    }

});

setInterval(function () {
    var type = $('.chartSelect').val();
    $('#myAreaChart').remove(); // this is my <canvas> element
    $('.chart-selections').append('<canvas id="myAreaChart" class="chartjs-render-monitor" width="1606px" height="318px"></canvas>');
    pm10Chart(type);
}, 3600000);
//        pm10Pie();}, 3600000);//request every x seconds