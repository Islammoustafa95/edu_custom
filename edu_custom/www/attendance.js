frappe.ready(function() {
    $(document).ready(function(){
        var stud_id = frappe.utils.get_url_arg("student_id");
        frappe.call({
            method: "edu_custom.www.attendance.get_attendance_data",
            args: {
                stud_id: stud_id
            },
            callback: function(response) {
                var r = response.message;
                if (r) {
                    if (r.message === "invalid_id") {
                        $("#student_name").text("Invalid Student ID");
                    }
                    else if (r.student) {
                        $("#student_name").text("Student: " + r.student);

                        if (r.message === "resubscribe") {
                            $("#subscription_status").css("display","block");
                            $("#subscription_status").text("Your subscription is not active.");
                            $("#mark_attendance").css("display", none);
                        } 
                        if (!r.attendance) {
                            $("#mark_attendance").css("display","block");
                        }
                        else if (r.attendance) {
                            $("#attendance_status").text("Your today's Attendance is already marked.");
                        }
                    }  
                }
            }
        });

        $("#mark_attendance").click(function(){            
            var student_id = frappe.utils.get_url_arg("student_id");
            frappe.call({
                method: 'edu_custom.www.attendance.mark_attendance',
                args: {
                    student_id: student_id,
                    mark_attendance: '1'
                },
                callback: function(response) {
                    var r = response.message;
                    if (r) {
                        // if (r.message === 'set_student_group') {
                        //     frappe.throw(__("Please set student group"));
                        // }
                        if (r.attendance) {
                            $("#attendance_status").text("Attendance marked successfully.");
                            $("#mark_attendance").css("display","block");
                            $("#mark_attendance").prop('disabled', true);
                        }
                    }
                }
            });       
        });
    });
});