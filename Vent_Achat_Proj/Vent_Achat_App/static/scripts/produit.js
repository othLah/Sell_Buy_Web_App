function check_date(i){
	if(i < 10){
		i = "0" + i;
	}
	return i;
}
function set_date(){
	var date = new Date();
	day = check_date(date.getDate());
	month = check_date(date.getMonth()+1);
	year = date.getFullYear();

	hour = check_date(date.getHours());
	minute = check_date(date.getMinutes());
	second = check_date(date.getSeconds());

	document.getElementById("date").innerHTML = day + "/" + month + "/" + year;
	document.getElementById("temps").innerHTML = hour + ":" + minute + ":" + second;

	var repeat = setTimeout(set_date, 500);
}

function upload_page(){
	var butt = document.getElementById("search_butt");
	butt.style.left = "430px";

	set_date();
	
	var image = document.getElementById("small_img1").src;
	document.getElementById("big_one").src = image;
	document.getElementById("small_p1").style.border = '2px solid black';

	var txt = document.getElementById("txt");
	var curr_len = txt.value.length;
	var len = 1500 - curr_len;
	document.getElementById("s3").innerText = "(" + len + ")";
}
function change_pic(nbre){
	if(nbre<=0 || nbre>=6){
		alert("Don't play with us -_-");
		return false;
	}

	var image = document.getElementById("small_img" + nbre).src;
	document.getElementById("big_one").src = image;

	for(var i=1; i<=5; i++){
		document.getElementById("small_p" + i).style.border = 'none';
	}
	document.getElementById("small_p" + nbre).style.border = '2px solid black';

	scroll(140, 140);
}
function go_achat(prod){
	var link = "affecte_achat/" + prod;
	window.location.href = link;
}