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
	for(var i=2; i<=5; i++)
		document.getElementById("del_p" + i).value = 0;

	var butt = document.getElementById("search_butt");
	butt.style.left = "430px";

	for(var i=2; i<=5; i++)
		document.getElementById("del_p" + i).value = 0;
	
	scroll(200, 200);

	set_date();
}
function upload_pic(nbre){
	if(nbre<=0 || nbre>=6){
		alert("Don't play with us -_-");
		return false;
	}

	var image = document.getElementById("small_in" + nbre);
	var ext = [".png", ".tif", ".tiff", ".jpg", ".jpge", ".jpe", ".jfif", ".bmp", ".dib"];
	var upload = false;

	for(var x=0; x < ext.length; x++){
		if(image.value.toLowerCase().endsWith(ext[x])){
			upload = true;
			break;
		}
	}

	if(upload){
		image = image.files[0];
		document.getElementById("big_one").src = window.URL.createObjectURL(image);
		document.getElementById("small_img" + nbre).src = window.URL.createObjectURL(image);
		for(var i=1; i<=5; i++){
			document.getElementById("small_p" + i).style.border = 'none';
		}
		document.getElementById("small_p" + nbre).style.border = '2px solid black';
		scroll(200, 200);
		if(nbre != 1)
			document.getElementById("del_p" + nbre).value = 0;
	}else{
		alert("Not a supported image format");
		image.value = null;
	}
}
function change_pic(nbre){
	if(nbre<=0 || nbre>=6){
		alert("Don't play with us -_-");
		return false;
	}

	image = document.getElementById("small_img" + nbre).src;
	document.getElementById("big_one").src = image;

	for(var i=1; i<=5; i++){
		document.getElementById("small_p" + i).style.border = 'none';
	}
	document.getElementById("small_p" + nbre).style.border = '2px solid black';
}
function follow_textarea(){
	var txt = document.getElementById("txt");
	var curr_len = txt.value.length;
	var len = 1500 - curr_len;

	document.getElementById("s3").innerText = "(" + len + ")";
}
function annuler_tout(){
	window.location.href="{% url 'vendre_page' %}";
}
function del_photo(nbre){
	if(nbre<2 || nbre>5){
		alert("Don't Play With Us -_-");
		return false;
	}
	
	document.getElementById("small_img" + nbre).src = "http://maiamthienan.org/public/images/no_image.png";
	document.getElementById("big_one").src = "http://maiamthienan.org/public/images/no_image.png";
	document.getElementById("del_p" + nbre).value = 1;
}