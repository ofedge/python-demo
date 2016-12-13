// startup sequence game script
var GameSS = {
    _init: function(){
        GameSS.fillHtml();
        GameSS.drawTable();
        GameSS.drawReset();
        GameSS.resetSnapshot();
        GameSS.snapshotToHtml();
    },
    init: function(){
        $('#resetCanvas').on('click', function(){
            GameSS.drawReset();
            GameSS.resetSnapshot();
            GameSS.snapshotToHtml();
        });
        $('#resetCanvas').on('dblclick', function(){
            GameSS.display();
        });
        $('img').on('click', function(){
            if ($(this).css('width') == '0px')
                return;
            var value = parseInt($(this).attr('data'));
            GameSS.click(value);
        });
    },
    fillHtml: function(){
        $('td').append('<img src="static/piece.png">');
        for (var i = 0; i < $('img').size(); i++){
            $('img').eq(i).attr('data', i).css('width', '0px');
        }
    },
    drawReset: function(){
        var ctx = document.getElementById('resetCanvas').getContext('2d');
        ctx.clearRect(0, 0, 100, 100);
        ctx.beginPath();
        ctx.arc(50, 50, 50, 0, 2 * Math.PI, true);
        ctx.closePath();
        ctx.fillStyle='#8ac007';
        ctx.fill();
        ctx.fillStyle='#ffffff';
        ctx.font = '30px Consolas';
        ctx.fillText('Reset', 10, 60);
    },
    drawSuccess: function(){
        var ctx = document.getElementById('resetCanvas').getContext('2d');
        ctx.clearRect(0, 0, 100, 100);
        ctx.beginPath();
        ctx.arc(50, 50, 50, 0, 2 * Math.PI, true);
        ctx.closePath();
        ctx.fillStyle='#8ac007';
        ctx.fill();
        ctx.fillStyle='#ffffff';
        ctx.font = '20px Consolas';
        ctx.fillText('YOU WIN!', 10, 60);
    },
    drawTable: function(){
        var ctx = document.getElementById('myCanvas').getContext('2d');
        ctx.beginPath();
        for(var i = 0; i < 5; i++){
            ctx.moveTo(0, i * 100 + 2);
            ctx.lineTo(400, i* 100 + 2);
        }
        for(var j = 0; j < 5; j++){
            ctx.moveTo(j * 100 + 2, 0);
            ctx.lineTo(j * 100 + 2, 400);
        }
        ctx.closePath();
        ctx.lineWidth=4;
        ctx.strokeStyle = '#8ac007'; 
        ctx.stroke();
    },
    resetSnapshot: function(){
        GameSS.snapshot = {table:{}, step:[]};
        for(var i = 0; i < 25; i++){
            GameSS.snapshot.table[i] = false;
        }
        var showPic = [0, 4, 7, 11, 12, 13, 17, 20, 24]
        for(var j = 0; j < showPic.length; j++){
            GameSS.snapshot.table[showPic[j]] = true;
        }
    },
    snapshotToHtml: function(){
        for(var i = 0; i < 25; i++){
            var $this = $('img[data=' + i + ']');
            if ($this.css('width') == '64px' && !GameSS.snapshot.table[i]){
                $this.animate({width: '0'}, 200);
            } else if ($this.css('width') == '0px' && GameSS.snapshot.table[i]){
                $this.animate({width: '64px'}, 200);
            }
        }
    },
    roundNum: function(n){
        if (n >= 0 && n < 25){
            return n;
        } else if (n < 0){
            return GameSS.roundNum(25 + n);
        } else {
            return GameSS.roundNum(n - 25);
        }
    },
    check: function(){
        for(var i = 0; i < 25; i++){
            if (i == 12){
                if (!GameSS.snapshot.table[i]){
                    return false;
                }
            } else {
                if (GameSS.snapshot.table[i]){
                    return false;
                }
            }
        }
        return true;
    },
    click: function(i){
        if (GameSS.check()){
            GameSS.drawSuccess();
        } else {
            var left = i % 5 == 0 ? i + 4 : i - 1;
            var right = (i + 1) % 5 == 0 ? i - 4 : i + 1;
            var up = GameSS.roundNum(i - 5);
            var down = GameSS.roundNum(i + 5);
            GameSS.snapshot.table[left] = GameSS.snapshot.table[left] ? false : true;
            GameSS.snapshot.table[right] = GameSS.snapshot.table[right] ? false : true;
            GameSS.snapshot.table[up] = GameSS.snapshot.table[up] ? false : true;
            GameSS.snapshot.table[down] = GameSS.snapshot.table[down] ? false : true;
        }
        GameSS.snapshot.table[i] = GameSS.snapshot.table[i] ? false : true;
        GameSS.snapshot.step.push(i);
        GameSS.snapshotToHtml();
    },
    destroy: function(){
        $('#resetCanvas').off('click');
        $('#resetCanvas').off('dblclick');
        $('img').off('click');
        for (var i = 0; i < 25; i++){
            $('img[data=' + i + ']').css('width', '0px');
        }
        GameSS.drawReset();
    },
    display: function(){
        GameSS.destroy();
        GameSS.drawReset();
        GameSS.resetSnapshot();
        GameSS.snapshotToHtml();
        var order = [0, 24, 4, 20, 7, 17, 11, 13, 1, 23, 5, 19, 12];
        for(var i = 0; i < order.length; i++){
            setTimeout('GameSS.click(' + order[i] + ')', (i + 1) * 1000);
        }
        setTimeout('GameSS.init()', order.length * 1000);
    }
}
GameSS._init();
GameSS.init();