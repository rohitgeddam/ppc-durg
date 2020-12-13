const attendanceToDate = $("#to_date")
const attendanceFromDate = $("#from_date")
const attendanceForm = $("#attendance-form")

$("#submit-btn").click(
    function(e){
        e.preventDefault();
        $("#js-error-message").html("")  
 
        $.ajax({
            url: attendanceForm.attr("data-url"),
            data: {
                'from_date': attendanceFromDate.val(),
                'to_date': attendanceToDate.val(),
            },
            dataType: 'json',
            success: function(data){
                if(data["message"] != "success"){
                    $("#js-error-message").html(
                        `<p style="color:red;">${data["message"]}</p>`
                    ) 
                } else {
                    $('#js-workout-days').html(
                        `${data["total_days_present_in_range"]} / ${data["total_days_in_range"]}`
                    )
                    $('#js-workout-hours').html(
                        `${data["total_workout_minutes_in_range"]}`
                    )
                }
            },
            failure: function(){
                $("#js-error-message").html(
                    "Some Error Occured"
                )
            }
        })
    }
)
