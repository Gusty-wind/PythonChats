$(document).ready(function() {

    const _init_bind_listeners = () => {
        $('#enable_show_psw').bind('click', () => {
            $('#enable_show_psw').hide();
            $('#disable_hide_psw').show();
            $("#password")[0].type ='text';
        })
        $('#disable_hide_psw').bind('click', () => {
            $('#disable_hide_psw').hide();
            $('#enable_show_psw').show();
            $("#password")[0].type ='password';
        })
        $("#password").on('input propertychange', () => {
            if ($("#password").hasClass("error_login_style")) {
                $("#password").removeClass('error_login_style');
            }
        })
        $("#username_cur").on('input propertychange', () => {
            if ($("#username_cur").hasClass("error_login_style")) {
                $("#username_cur").removeClass('error_login_style');
            }
        })
        //  !!!! intercept request and valiate the request 
        $("#conform_username").on('click', () => {
            if (!validateLoginData()) return false;
                let config = {
                    url: '/validate',
                    type: 'POST',
                    current_user: $("#username_cur")[0].value,
                    password: $("#password")[0].value
                }
                let result = handlePostRequest(config);
                return result
            
        })
        // link to the regist view
        $("#register_new").on('click', () => {
            // !need to change the httpxxx to get url code
            window.location.href = 'http://localhost:9008/register';
        })
    };

    const getCookie = (name) => {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }
  
     const handlePostRequest = (config) => {
        config._xsrf = getCookie("_xsrf");
        let status = false;
            $.ajax({
                type:config.type,
                url:config.url,
                data: $.param(config),
                async: false,
                success: (data)=>{
                    if (!data.data.status) {
                        // if response status is false
                        // send the error message to the view 
                        console.log(data.data)
                    }
                    status =  data.data.status;
                },
                dataType: 'json'
            }) 
        return status;
    }

    const validateLoginData = () => {
        let login_status = true;
        if ($("#password")[0].value == '' &&  $("#username_cur")[0].value == '') {
            $("#password").addClass('error_login_style');
            $("#username_cur").addClass('error_login_style');
            login_status = false;
        } else  if ($("#password")[0].value == ''){
            $("#password").addClass('error_login_style');
            login_status = false;
        } else  if ($("#username_cur")[0].value == '') {
            $("#username_cur").addClass('error_login_style');
            login_status = false;
        } else {
            if ($("#password").hasClass("error_login_style")) {
                $("#password").removeClass('error_login_style');
            }
            if ($("#username_cur").hasClass("error_login_style")) {
                $("#username_cur").removeClass('error_login_style');
            }
        }
        return login_status;
    }
    document.onreadystatechange = function () {  
        if(document.readyState=="complete") { 
            // default hide the enable show pwd
            $('#disable_hide_psw').hide();
            _init_bind_listeners();
        } 
    }
})