(function(){

	"use strict";

	// Websocket address
	const myWebSocket = "ws://localhost:8888/ws";

// Websocket variable
	var socket = new WebSocket(myWebSocket);
	socket.onerror = socketErrorAlert;



// Websocket event handlers
	if (socket){
		socket.onopen = function() {
			console.log("Server is ready");
		}
		socket.onmessage = function(msg){
			console.log("Got message from server - calling processResponse");
			processResponse(msg);
		}
		socket.onclose = function() {
			console.log("Server connection closed");
		}
	}
	else {
		console.log("Invalid websocket");
	}

// Json requests
	var jsonSingleString = '{"action":"single"}';
	var jsonStatsString = '{"action":"stats", "samples":10}';

// Misc variables
	const spinBoxH = document.getElementById("spinh");
	const spinBoxT = document.getElementById("spint");
	var temp = 0;
	var hum = 0;
	var tAlarm = 100;
	var hAlarm = 100;
	var hMin, hMax, hAvg, tMin, tMax, tAvg;
	var myChart;

// Button handlers
	const singleRequestButton = document.getElementById("singlereq");
	const multiRequestButton = document.getElementById("multireq");
	const statsButton = document.getElementById("statsreq");
	const closeButton = document.getElementById("closeb");

	singleRequestButton.addEventListener("click", function(event){
		read1();
	});

	multiRequestButton.addEventListener("click", function(event){
		read1();
		for(let i=0; i<9; i++){
			setTimeout(read1,1000);
		}
	});

	statsButton.addEventListener("click", function(event){
		socket.send(jsonStatsString);
	});

	closeButton.addEventListener("click", function(event){
		socket.close();
		alert("Server connection closed - Close tab manually");
	});


	function socketErrorAlert(event){
		alert("Server/socket error: " + event.data);
	}


	function read1(){
		if (socket.readyState !== WebSocket.CLOSED && socket.readyState !== WebSocket.CLOSING) {
			socket.send(jsonSingleString);
		}
		else {
			alert("Server or socket not available");
		}
	}

	function processResponse(jsonText){
		console.log(jsonText);
		const jsonObject = JSON.parse(jsonText.data);
		const response = jsonObject["response"];
		if (response == "reading"){
			const ts = jsonObject["timestamp"];
			const hum = jsonObject["humidity"];
			const temp = jsonObject["temperature"];
			const text1 = `+++ At timestamp ${ts} Humidity: ${hum} % +++ Temperature: ${temp} Fahrenheit +++`;
			showResults(text1);
			const hAlarm = spinBoxH.value;
			const tAlarm = spinBoxT.value;
			if (hum > hAlarm) {
				showResults("<b>Alarm: humidity level exceeded!</b>");
			}
			if (temp > tAlarm) {
				showResults("<b>Alarm: temperature level exceeded!</b>");
			}
			console.log(`Got Humidity ${hum} Temperature ${temp}`);
		}
		else if (response == "stats"){
			console.log("Processing sensor stats");
			const hMin = jsonObject["humidity-min"];
			const hMax = jsonObject["humidity-max"];
			const hAvg = jsonObject["humidity-avg"];
			const tMin = jsonObject["temperature-min"];
			const tMax = jsonObject["temperature-max"];
			const tAvg = jsonObject["temperature-avg"];
			var text2 = `+++ Minimum Humidity ${hMin} +++ Maximum Humidity ${hMax} +++ Average Humidity ${hAvg}`;
			showResults(text2);
			text2 = `+++ Minimum Temperature ${tMin} +++ Maximum Temperature ${tMax} +++ Average Temperature ${tAvg}`;
			showResults(text2);
			var dataHum = jsonObject["humidity-array"];
			var dataTemp = jsonObject["temperature-array"];
			showGraph(dataHum,dataTemp);
		}
		else {
			console.log("Unknown response");
		}

	}

	function showResults(texto){
		var par = document.createElement('p');
		par.innerHTML = texto;
		document.getElementById("results").appendChild(par);
	}

	function showGraph(dataHum,dataTemp) {
//Graph configuration and setup

		console.log("Processing graph");

		var labls=[];
		for(let i=1;i<dataTemp.length+1;i++){
			labls.push(i);
		}

		const data = {
		  labels: labls,
		  datasets: [{
		  	label: 'humidity',
		  	backgroundColor: 'rgb(0, 255, 0)',
		  	borderColor: 'rgb(0, 255, 0)',
		  	data: dataHum,
		  },
		  {
		  	label: 'temperature',
		  	backgroundColor: 'rgb(255, 0, 0)',
		  	borderColor: 'rgb(255, 0, 0)',
		  	data: dataTemp,

		  }]
		};

		const config = {
	  		type: 'line',
	  		data,
	  		options: {}
		};

	
		if (myChart) {
			myChart.destroy();
		}
		myChart = new Chart(document.getElementById('myChart'),config);
	}

})();