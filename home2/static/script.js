$(function(){
    SignIn.btn();
    $('.item.toc.mainmenu').on('click', function(){
        $('.ui.sidebar.mainmenu').sidebar('show');
    });
    $('#signin').on('click', function(){
        $('.modal.signin').modal('show');
    });
    // click function
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
    btn: function(){
        $('.modal.signin input[name=username], .modal.signin input[name=password]').on('blur', function(){
            $(this).val($.trim($(this).val()));
        });
        $('.modal.signin div[name=signin]').on('click', function(){
            var username = $('.modal.signin input[name=username]').val();
            var password = $('.modal.signin input[name=password]').val();
            $.ajax({
                url: '/signin',
                type: 'post',
                data: {'username': username, 'password': password},
                success: function(data){
                    console.log(data);
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