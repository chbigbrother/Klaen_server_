Dropzone.autoDiscover = false; // dropzone 초기화
$(function(){

    // .csv 업로드 버튼
    $('#uploadBtn').on('click', function(){
        $('#csvUploadModal').modal({backdrop: 'static', keyboard: false})
        $("#csvUploadModal").modal("show");
    });

    // csv 업로드
    var formData = new FormData();
    var dropzone = new Dropzone("#csvDropzone", {
        url: "/sensor/iaq/csv/upload/",
        addRemoveLinks: true,
        maxFiles: 1,
        init: function(e) {
            // 파일 업로드 성공 시
            this.on('success', function(file) {
                formData.append("file", dropzone.getAcceptedFiles()[0]);
                fileName = file.name;
                //확장자 체크(작업장별 다름)
                if(!hasExtension(fileName, ['csv'])){
                    Swal.fire({
                      icon: 'error',
                      title: '파일 형식 오류',
                      text: '.csv 파일을 업로드 해 주세요.',
                    });
                    return false;
                }
            });

        }
    });
    $('#upload').on('click', function(){
        $.ajax({
            url: "/sensor/iaq/upload/",
            method:'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function(result){
                location.reload();
            },
            error: function(error){
                console.log(error)
            }
        });

    });
});