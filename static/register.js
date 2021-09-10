$(document).ready(function() {

    document.onreadystatechange = function () {  
        if(document.readyState=="complete") { 
            _init_bind_listeners();
        } 
    }

    const _init_bind_listeners = () => {
        // link to the regist view
        $("#submit_new_user").on('click', (e) => {
             if (!validateLoginData()) return false;
             let config = {
                url: '/register',
                type: 'POST',
                current_user: $("#username_cur")[0].value,
                password: $("#password")[0].value,
                phone: $("#phone_num")[0].value == ''?'':$("#phone_num")[0].value
            }
            let result = handlerSubmitRequest(config);
            return result;
        })
    };


    const validateLoginData = () => {
        let validate_status = true;
        if ($("#password")[0].value == '' &&  $("#username_cur")[0].value == '') {
            $("#password").addClass('error_login_style');
            $("#username_cur").addClass('error_login_style');
            validate_status = false;
        } else  if ($("#password")[0].value == ''){
            $("#password").addClass('error_login_style');
            validate_status = false;
        } else  if ($("#username_cur")[0].value == '') {
            $("#username_cur").addClass('error_login_style');
            validate_status = false;
        } else {
            if ($("#password").hasClass("error_login_style")) {
                $("#password").removeClass('error_login_style');
            }
            if ($("#username_cur").hasClass("error_login_style")) {
                $("#username_cur").removeClass('error_login_style');
            }
        }
        return validate_status;
    }

    const getCookie = (name) => {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }
    const handlerSubmitRequest = (config) => {
        config._xsrf = getCookie("_xsrf");
        let status = false;
            $.ajax({
                type:config.type,
                url:config.url,
                data: $.param(config),
                async: false,
                success: (data)=>{
                    if (!data.status) {
                        // if response status is false
                        // send the error message to the view 
                        console.log(data.data)
                    }
                    status =  data.status;
                },
                complete: (data)=>{
                    console.log(data, 'jjjjjjjjjjjjjj')
                },
                dataType: 'json'
            }) 
        return status;
    }
})