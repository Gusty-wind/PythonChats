$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    window.cVersion = "3.1.2";
    // setting single user chat config date module
    let _golabConfig = new Map([
        ['chatFrom', $("#currnetUser").html().trim()],
        ['chatTo', ''],
        ['unread_msg_num', []]
    ]);
    let imageFiles  = [];
    let currentUser = $("#currnetUser").html().trim(),
        send_url = "ws://127.0.0.1:9008/chat?username_cur="+currentUser,
        ws = new WebSocket(send_url);

    // action bar tools
    class Actionbar {
        constructor() {
            this.set = (key, val) => {
                this[key] = val;
                _golabConfig.set(key, val);
                return key;
            }

            this.get = (key) =>{
                return _golabConfig.get(key);
            }

            this.format_icon = (icon_name, icon_id) => {
                return "<iconpark-icon name='"+icon_name+"' id='"+icon_id+"' ></iconpark-icon>"
            }
            // upload type of images 
            this.upload_files = (e) => {
                let file_ojb = $('.upload_files')[0].files[0];
                let imageTypes = ['image', 'png', 'jpg', 'gif'];
                if (!file_ojb.type && file_ojb.type !=undefined && imageTypes.includes(file_ojb.type)) return false;                
                const getObjectUrl = (file) => {
                    let url = null ;
                    if (window.createObjectURL!= undefined) { 
                        url = window.createObjectURL(file) ;
                    } else if (window.URL!= undefined) {
                        url = window.URL.createObjectURL(file) ;
                    } else if (window.webkitURL!= undefined) { 
                        url = window.webkitURL.createObjectURL(file) ;
                    }

                    let upload_img_obj = {
                        'img_name': file_ojb.name,
                        'img_type': file_ojb.type,
                        'img_size': imageTypes.size,
                        'img_tmp_base64': ''
                    }
                    let reader = new FileReader();
                        reader.readAsDataURL(file)
                        reader.onload = function() {
                            upload_img_obj.img_tmp_base64 = reader.result
                            // console.log(upload_img_obj.img_tmp_base64)
                        }
                    imageFiles.push(upload_img_obj);
                    return url ;
                }
                // when image not exist display a default image
                // img_create.onerror = display_default_img(this);
                const display_default_img = (img)=>{
                    img.src = './static/images/logo_2.png';
                    img.onerror = null
                }
                // create new image obj and add it to the dom element
                if (file_ojb.name)  {
                    let img_create = document.createElement("img");
                        img_create.src = getObjectUrl(file_ojb);
                        img_create.className = "upload_image_style";
                    document.getElementsByClassName("emojionearea-editor")[0].append(img_create);
                }
            }

            this.createActionbut = function(paramtList) {
                let butTmp = "";

                if (paramtList.get('displayIcon')) {
                     if (paramtList.get('eventAction') == 'upload') {
                        butTmp = "<div class='comment_bar_style' title='"+paramtList.get('titleName')+"'>"+ this.format_icon(paramtList.get('icon_name'), paramtList.get('icon_id')) + "<input type='file' class='upload_files'></div>";
                     } else {
                        butTmp = "<div class='comment_bar_style' title='"+paramtList.get('titleName')+"'>"+ this.format_icon(paramtList.get('icon_name'), paramtList.get('icon_id')) + "</div>";
                     }
                } else {
                    butTmp = "<div  title='"+paramtList.get('titleName')+"'>"+paramtList.get('displayName')+"</div>";
                }
                // if (paramtList.get(eventAction) !='') {
                //     this.handleBindDomListener(paramtList.get(icon_id), paramtList.get(eventAction))
                // }
                return butTmp
            }
            this.handleBindDomListener = (nodeId, action) => {
                document.getElementById(nodeId).addEventListener (action, ()=>{

                })
            }
        }
    }

    let actionClass = new Actionbar();

    // emojio config
    $("#msg").emojioneArea({
        autoHideFilters: true,
        pickerPosition:'top',
        searchPosition: "bottom",
        tones: false,
        shortnames: true,
        events:{
            emojibtn_click: function (button, event) {
                let emoji_area = $("#msg").emojioneArea();
                    emoji_area.data("emojioneArea").hidePicker();
            },
            change: function(e) {
                // fix bug when blur input . emoji js will clear the input content
                let emoji_area_edito = $('.emojionearea-editor');
                if (emoji_area_edito.children().length > 0) {
                    return;
                }
            },
        }
    });

    /**/

    let resize = document.getElementById("splitDiv");
    let left = document.getElementById("current_login_users");
    let right = document.getElementById("chat_iframe");
    let box = document.getElementById("content_box");
    resize.onmousedown = function(e){
        //Drag and drop chat area
        var startX = e.clientX;
        resize.left = resize.offsetLeft;

        document.onmousemove = function(e){
            var endX = e.clientX;

            var moveLen = resize.left + (endX - startX);
            var maxT = box.clientWidth - resize.offsetWidth;
            if(moveLen<59) moveLen = 59;
            if(moveLen>maxT-500) moveLen = maxT-500;

            resize.style.left = moveLen;
            left.style.width = moveLen + "px";
            right.style.width = (box.clientWidth - moveLen - 5) + "px";
        }
        document.onmouseup = function(evt){
            evt.stopPropagation()
            document.onmousemove = null;
            document.onmouseup = null;
            resize.releaseCapture && resize.releaseCapture();
        }
        resize.setCapture && resize.setCapture();
        return false;
    };

    /**/

    const emoji_close_picker = () => {
        let emojiPicker = $('.emojionearea-picker'),
            emoji_but = $('.emojionearea-button');
        if (!emojiPicker.hasClass('hidden')) {
            emojiPicker.addClass('hidden');
        }
        if (emoji_but.hasClass('active')) {
            emoji_but.removeClass('active');
        }
    }

    $("#messageFrom").on('keypress', function(e){
        if (e.key == 'Enter') {
            sendMsg();
            e.preventDefault();
            e.stopPropagation();
            emoji_close_picker();
        }
    });


    const formatEmojiToString = (domItems) => {
        let final_dom = [];
        if (domItems.childElementCount > 0) {
            for(let i = 0; i < domItems.childElementCount; i++) {
                if (domItems.children[i].tagName == 'IMG') {
                    final_dom.push(domItems.children[i]);
                } else if (domItems.children[i].tagName == 'DIV') {
                    formatEmojiToString(domItems.children[i]);
                }
            }
        }
        return final_dom;
    }

    const  _initListener = () => {
        document.getElementById('add_actions_a').addEventListener('click',()=>{
            if (!$(".actions_bar_show_div").hasClass('active')) {
                $(".actions_bar_show_div").fadeIn('slow');
                $(".actions_bar_show_div").addClass('active');
            } else {
                $(".actions_bar_show_div").fadeOut('slow');
                $(".actions_bar_show_div").removeClass('active');
            }   
        });
    }

    document.onreadystatechange = function () {   
        
        if(document.readyState=="complete") { 

            let congigDom = new Map([
                ['displayIcon', true],
                ['icon_name', 'pic'],
                ['icon_id', 'pic_action_bar'],
                ['displayName', ''],
                ['titleName', 'upload a image'],
                ['eventAction', 'upload']
            ]);

            let action_1  = actionClass.createActionbut(congigDom);
            let send_6 ="<div class='action_bar_spen6_6' title='Show More Actions'><iconpark-icon name='config' id='add_actions_a' ></iconpark-icon></div>";
            let spen6 = "<div class='action_bar_spen6'>"+send_6+"</div><div class='actions_bar_show_div' style='display:none'>"+action_1+"</div>";
            $('.emojionearea-button').before("<div class='action_bar'>"+spen6+"</div>");
            _initListener();
            if (congigDom.get('eventAction') == 'upload') {
                document.getElementsByClassName('upload_files')[0].addEventListener('change', (e)=> {
                        actionClass.upload_files(e);
                });
            }
         }   
     }

    const sendMsg = (flow_user = false) => {
        if (_golabConfig.get('chatTo') == '') {
            alert("必须选取一个联系人开始聊天.")
            clear_cache_data_modules();
            return;
        }
        // click the flow user
        let pointerList = {
            "chatFrom": _golabConfig.get('chatFrom'),
            "chatTo": _golabConfig.get('chatTo'),
        }
        if (flow_user) {
            handleUserHistoryMessage.clearChatViewMessage();
            // get history data from the log files
            let send_history_apply = {
                get_history_flg: true,
                user: flow_user, // current chat objects
                current_view_user:  currentUser // current login user
            }
            ws.send(JSON.stringify(send_history_apply));
        } else { 
            let inputval = $(".emojionearea-editor")[0];
            data = {
                pointer:pointerList,
                msg:inputval.getInnerHTML(),
                imagefile: imageFiles
            };
            ws.send(JSON.stringify(data));
            clear_cache_data_modules();
        }
    }

    const clear_cache_data_modules = () => {
        let inputval = $(".emojionearea-editor")[0];
            inputval.innerText = '';
            // clear the image cache
            imageFiles = [];
    }


    // for chinese word trans
    String.prototype.getBytes = function() {       
        let cArr = this.match(/[^\x00-\xff]/ig);       
        return this.length + (cArr == null ? 0 : cArr.length);    
    }

    const get_current_login_users = (users) => {
        let currentUsers ='';
        if (users != undefined && users.length > 0) {
            users.forEach((user) => {
                currentUsers +="<div class='exist_user_list_p'>"+user+"</div>";
            });
        }
        return currentUsers
    }
    // remove all the  single user click style bg
    const remove_all_click_class = () => {
        if ($('.exist_user_list_p').length > 0) {
            for (let i = 0; i< $('.exist_user_list_p').length; i++) {
                if ($('.exist_user_list_p')[i].className.includes('options_click_bg')) {
                    $('.exist_user_list_p')[i].className = $('.exist_user_list_p')[i].className.replace('options_click_bg', '');
                }
            }
        }
    }

    /*when user click a customer user to chat
        1. clear display view
        2. get the history chat log
        3. re-render view and display the history(what they chat) message.
    */

    class HandleUserHistoryMessage {

        constructor(props) {
            this.get_flow_user_chat_hoisty = (chat_to_user) => {
                sendMsg(chat_to_user);
            }
            this.clearChatViewMessage = () => {
                if ($('.item_chat_list').children().length > 0) {
                    for (let i = $('.item_chat_list').children().length-1;  i >= 0; i--) {
                        $('.item_chat_list').children()[i].remove();
                    }
                }
            }
        }
    }

    let handleUserHistoryMessage = new HandleUserHistoryMessage();

    const handled_single_user_click = () => {
        // bind click single user to chat
        $('.exist_user_list_p').bind('click',(e)=>{
            if ( e.target.innerText == actionClass.get("chatTo")) {
                //  cannel continuous click the same user to chat
                return;
            }
            actionClass.set("chatTo", e.target.innerText);
            remove_all_click_class();
            if  (e.target.className.includes('append_unread_meassages')) {
                e.target.className = e.target.className.replace('append_unread_meassages', '');
            }
            e.target.className +=' options_click_bg';
            // do the dipplay single chat action
            handleUserHistoryMessage.get_flow_user_chat_hoisty(e.target.innerText);
        });
    }

    // un-read message numbers
    const get_unread_msg_number = (unread_user) => {
        let unread_msg_obj = _golabConfig.get('unread_msg_num');
        if (Object.keys(unread_msg_obj).includes(unread_user)) {
            unread_msg_obj[unread_user] = unread_msg_obj[unread_user] +1
        } else {
            unread_msg_obj[unread_user] = 1;
        }
        _golabConfig.set('unread_msg_num', unread_msg_obj);
        return Object.values(unread_msg_obj)[0];
    }

    const handle_unread_message = (unread_user) => {
        if ($('.exist_user_list_p').length > 1) {
            for (let i = 0; i< $('.exist_user_list_p').length; i++) {
                /*
                    un-read user && not current chat user. 
                    add a flg to mark un-read message
                */
                if ($('.exist_user_list_p')[i].innerHTML.toString().trim() == unread_user
                    && !$('.exist_user_list_p')[i].className.includes('options_click_bg')
                ) {
                    $('.exist_user_list_p')[i].className += ' append_unread_meassages ';
                }
            }
        }
    }

    ws.onmessage = function(recv) {
        let _id = recv.timeStamp.toString().replace(".", "-");
        let datas = JSON.parse(recv.data);
        let  dom = "";
        if (datas.isHeaderData == "true") {
            let joinOrLeft =  datas.joinData?" Weclome -["+ datas.name +"] join to":"["+ datas.name +"] have left the";
            dom = "<div id="+_id+" class='span-12 item-single-line'> ["+datas.date+"] "+ joinOrLeft+ " chat room. </div>";
            $(".channel_box").html(get_current_login_users(datas.summary_users));
            handled_single_user_click();
        } else {
            let meg_font_css = 'msg_font_div';
            let msg_len = datas.message.length + datas.message.getBytes();
            if (msg_len > 25) {
                meg_font_css += ' extend_font_site';
            }
            if ($('#currnetUser').html() == datas.name) {
                dom = "<div class='span-10-after' id="+_id+"> <div class='msg_font'><div class='"+meg_font_css+"'>"+ datas.message + "</div></div></div><div class='span-11-after'><div class='dis_cur_name'>-[ You ]</div></div>";
            } else {
                dom ="<div class='span-12' id="+_id+" > <div class='dis_cur_name'>["+ datas.name +"]</div> <div  class='msg_font_o'><div  class='"+meg_font_css+"'>"+ datas.message + "</div></div></div></div></div>";
                handle_unread_message(datas.name)
            }
        }
        $(".item_chat_list").append(dom);

        document.getElementById('chat_iframe_footer').scrollIntoView(true);

    };
})