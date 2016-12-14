$(function(){
    // sign in
    SignIn.btn();
    // main menu sidebar
    $('.item.toc.mainmenu').on('click', function(){
        $('.ui.sidebar.mainmenu').sidebar('show');
    });
    // menu item click function
    $('a[name=home]').on('click', function(){
        window.history.pushState(PageSwitch.pages[0], '', '/');
        PageSwitch.home();
    });
    $('a[name=game]').on('click', function(){
        window.history.pushState(PageSwitch.pages[1], '', '/game');
        PageSwitch.game();
    });
    // window history function
    window.onpopstate = function(event){
        if(event.state){
            if (event.state == PageSwitch.pages[0]){
                PageSwitch.home();
            } else if (event.state == PageSwitch.pages[1]) {
                PageSwitch.game();
            }
        }
    }
});
// sign in
var SignIn = {
    regExp: /^[0-9a-zA-z_]{4,18}$/,
    check: function(string){
        return SignIn.regExp.test(string);
    },
    addError: function($dom){
        $dom.addClass('error');
        $('.modal.signin .content .red.message').removeClass('hidden').addClass('visible');
    },
    removeError: function($dom){
        $dom.removeClass('error');
        $('.modal.signin .content .red.message').removeClass('visible').addClass('hidden');
    },
    btn: function(){
        // sign in modal
        $('.modal.signin').modal({
            onHidden: function(){
                $('.modal.signin input').val('');
                SignIn.removeError($('.modal.signin input').parent());
            }
        });
        $('.modal.basic.signin').on('keydown', function(event){
            if(event.keyCode == 13){
                $('.modal.basic.signin div[name=signin]').click();
            }
        });
        $('.secondary.pointing.menu').on('click', '#signin', function(){
            $('.modal.signin').modal('show');
        });
        // sign in
        $('.modal.signin div[name=signin]').on('click', function(){
            var $username = $('.modal.signin input[name=username]');
            var username = $username.val();
            if (SignIn.check(username)){
                SignIn.removeError($username.parent());
            } else {
                SignIn.addError($username.parent());
                $username.focus();
                return;
            }
            var $password = $('.modal.signin input[name=password]');
            var password = $password.val();
            if (SignIn.check(password)){
                SignIn.removeError($password.parent());
            } else {
                SignIn.addError($password.parent());
                $password.focus();
                return;
            }
            $.ajax({
                url: '/signin',
                type: 'post',
                data: {'username': username, 'password': password},
                success: function(data){
                    $('.basic.modal.sysinfo .content').html('<h3>' + data.msg + '</h3>');
                    $('.basic.modal.sysinfo').modal('show');
                    if(data.rtcode == 1){
                        var btnHtml = '<a class="item" name="user">' + data.data.username + '</a><a class="item" name="signout">Sign out</a>';
                        $('.ui.secondary.pointing.menu .right.menu').html(btnHtml);
                    }
                }
            });
        });
        $('.secondary.pointing.menu').on('click', 'a[name=signout]', function(){
            $.ajax({
                url: '/signout',
                type: 'get',
                success: function(data){
                    $('.basic.modal.sysinfo .content').html('<h3>' + data.msg + '</h3>');
                    $('.basic.modal.sysinfo').modal('show');
                    var btnHtml = '<button class="ui inverted button" id="signin">Sign in</button>';
                    $('.ui.secondary.pointing.menu .right.menu').html(btnHtml);
                }
            });
        });
    }
}
// page switch function
var PageSwitch = {
    // all the pages
    pages: {
        0: 'Home',
        1: 'Game',
        2: 'Well Read',
        3: 'Artifact Knowledge'
    },
    pageDisappear: function(func){
        $('#content_body').animate({'height': '0'}, 'fast', function(){
            $('#content_body').remove();
            if(func)
                func();
        });
    },
    pageAppear: function(){
        $('#content_body').animate({'height': '719px'}, 'fast');
    },
    loadPage: function(pageIndex, url){
        PageSwitch.pageDisappear(
            function(){
                $.get(url, function(data){
                    for(var i = 0; i < $(data).length; i++){
                        if($(data)[i].tagName && $(data)[i].tagName.toLowerCase() == 'title'){
                            $('title').html($(data).eq(i).html());
                        }
                        if($(data).eq(i).find('#wrap_content').length > 0){
                            var $wrap_content = $(data).eq(i).find('#wrap_content');
                            $wrap_content.find('#content_body').css('height','0');
                            $('#wrap_content').html($wrap_content.html());
                            break;
                        }
                    }
                    PageSwitch.pageAppear();
                    $('.ui.sidebar.mainmenu').sidebar('hide');
                }, 'html');
            }
        );
    },
    home: function(){
        $('a.item').removeClass('active');
        $('a[name=home]').addClass('active');
        PageSwitch.loadPage(0, '/');
    },
    game: function(){
        $('a.item').removeClass('active');
        $('a[name=game]').addClass('active');
        PageSwitch.loadPage(1, '/game');
    }
}