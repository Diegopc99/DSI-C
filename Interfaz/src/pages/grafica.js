var chart;

console.log("Starting grafico.js");

chart = new Highcharts.Chart({

	chart: {
		renderTo: "grafico",
		defaultSeriesType: 'spline'
	},

	title: {
	text: 'Weather Cape Luminosity Plot'},
	xAxis: {
		type: 'datetime',
		tickPixelInterval: 150,
		maxZoom: 20 * 1000,
	title: {
		text: 'Luminosity',
		margin: 15
	}
	},
	yAxis: {
		minPadding: 0.2,
		maxPadding: 0.2,
	title: {
		text: 'Luminosity (lux)',
		margin: 15
	}
	},
	series: [{
		name: 'Weather cape luminosity sensor',
		data: []
		}]
});

var cont = 0;
var lux=0;
var socket=new io.connect();
socket.on('lux',function(data){
	cont = cont+1;
	if(cont <= 40){
		var myData= parseFloat(data);
		lux=myData;
		point = [Date.now(), lux];
		chart.series[0].addPoint(point, true, false);
	} else {
		var myData = parseFloat(data);
		lux=myData;
		poitn = [Date.now(), lux];
		chart.series[0].addPoint(point, true, true);
	}
});
