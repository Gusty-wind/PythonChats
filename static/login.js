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
        $("#conform_username").on('click', () => {
            if (validateLoginData()) {
                let config = {
                    url: '/',
                    // current_user: $("#username_cur")[0].value,
                    // password: $("#password")[0].value
                }
                // $('form').submit(config);
                // handleGetRequest(config);
                return;
            } else {
                console.log('account && password not be empty.')
            }
        })
    };

    const getCookie = (name) => {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }
    const handlePostRequest = (e) => {

    }

    const handleGetRequest = (config) => {
        // config._xsrf = getCookie("_xsrf");
        config._xsrf = "2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3B=";
        $.ajax({
            type:'POST',
            url:config.url,
            data: $.param(config),
            success: (data)=>{

            },
            complete: (response) => {
                console.log(response)
            },
            dataType: 'json'
        })
        
    }

    const validateLoginData = () => {
        if ($("#password")[0].value == '' &&  $("#username_cur")[0].value == '') {
            $("#password").addClass('error_login_style');
            $("#username_cur").addClass('error_login_style');
            return false;
        } else  if ($("#password")[0].value == ''){
            $("#password").addClass('error_login_style');
            return false;
        } else  if ($("#username_cur")[0].value == '') {
            $("#username_cur").addClass('error_login_style');
            return false;
        } else {
            if ($("#password").hasClass("error_login_style")) {
                $("#password").removeClass('error_login_style');
            }
            if ($("#username_cur").hasClass("error_login_style")) {
                $("#username_cur").removeClass('error_login_style');
            }
            return true;
        }
    }
    document.onreadystatechange = function () {  
        if(document.readyState=="complete") { 
            // default hide the enable show pwd
            $('#disable_hide_psw').hide();
            _init_bind_listeners();
        } 
    }
})