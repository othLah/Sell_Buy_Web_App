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