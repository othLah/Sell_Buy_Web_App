var user = 0;

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
function go_first(){
	var butt = document.getElementById("search_butt");
	butt.style.left = "430px";

	set_date();
}
function display_supp(id){
	var supp = document.getElementById("div_supp");
	supp.style.left = "0px";
	scroll(0, 0);
	document.getElementById("body_id").style.overflow = "hidden";
	user = id;		
}
function click_oui(){
	var link = "/supprimer_compte/" + user;
	window.location.href = link;
}
function click_non(){
	var supp = document.getElementById("div_supp");
	supp.style.left = "-10000px";
	document.getElementById("body_id").style.overflow = "auto";
}