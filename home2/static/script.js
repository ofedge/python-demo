$(function(){
    $('.item.toc.mainmenu').on('click', function(){
        $('.ui.sidebar.mainmenu').sidebar('show');
    });
    $('#login').on('click', function(){
        $('.modal.login').modal('show');
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
                $.ajax({
                    url: url,
                    type: 'get',
                    dataType: 'html',
                    success: function(data){
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
                    }
                });
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