function userLogPie(){
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
        url :'/account/user/stat/list/',
        method: 'GET',
        dataType: 'json',
        async: false,
        contentType: 'application/json',
        processData: false,
        success: function(result) {
            console.log(result);
            for (var i = 0; i < result.length; i++) {
                data.push(result[i].visitcount);
                labels.push(result[i].username);
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
    })

}