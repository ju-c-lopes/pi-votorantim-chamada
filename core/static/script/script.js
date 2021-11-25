var menu = document.getElementById('btmenu');
var show = true;

function apontar() {
    menu.style.background = '#494949';
}

function sair() {
    menu.style.background = '#292929';
}

function apertar() {
    if (show) {
        document.getElementById('login').style.visibility = 'visible';
        menu.src = "/static/cancel.png";
        show = !show;
    }
    else {
        document.getElementById('login').style.visibility = 'hidden';
        menu.src = "/static/menu.png";
        show = !show;
    }
}
