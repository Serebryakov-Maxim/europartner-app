var mytime = mytime_const = 3600;
document.onmousemove = document.onkeydown = document.onscroll = function(){mytime = mytime_const};

setInterval(function(){
    //console.log(mytime);
    mytime --;
    if (mytime<=0)location.href = window.location.protocol + "//" + window.location.host + "/pressforms/media/?" + location.href;
}, 1000);