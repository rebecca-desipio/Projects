
// SVG drawing area

let margin = {top: 40, right: 10, bottom: 60, left: 60};

let width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

let svg = d3.select("#chart-area").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
	//.style("background-color", '#EEE')
  	.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

let selectedOption = "stores"

// Scales
let x = d3.scaleBand()
    .rangeRound([0, width])
	.paddingInner(0.1);

let y = d3.scaleLinear()
    .range([height, 0]);

let xAxis = d3.axisBottom(x)
let yAxis = d3.axisLeft(y)

// draw the axis
let xGroup = svg.append("g")
	.attr("class", "x-axis")
	.attr("transform", "translate(" + (margin.right - margin.left + x.bandwidth()/16) + "," + (height) + ")")
	.call(xAxis)

let yGroup = svg.append("g")
	.attr("class", "y-axis")
	.call(yAxis)

let ylabel = svg.append("text")
	.attr("x", -margin.left+margin.right+10)
	.attr("y", -margin.top/4)
	.attr("fill", "gray")
	.attr("font-size", 12)
	.text("stores")

// Initialize data
loadData();

let buttonVal = 1



// Create a 'data' property under the window object
// to store the coffee chain data
Object.defineProperty(window, 'data', {
	// data getter
	get: function() { return _data; },
	// data setter
	set: function(value) {
		_data = value;
		// update the visualization each time the data property is set by using the equal sign (e.g. data = [])
		updateVisualization()
	}
});

// Load CSV file
function loadData() {
	d3.csv("data/coffee-house-chains.csv").then(csv=> {

		csv.forEach(function(d){
			d.revenue = +d.revenue;
			d.stores = +d.stores;
		});

		// Store csv data in global variable
		data = csv;

        // updateVisualization gets automatically called within the data = csv call;
		// basically(whenever the data is set to a value using = operator);
		// see the definition above: Object.defineProperty(window, 'data', { ...
	});
}

// Render visualization
function updateVisualization() {
  	console.log(data);

	// initialize dataset to display data for stores
	dispData(selectedOption, buttonVal)

	// get the value of the select box
	d3.select("#ranking-type").on("change", function() {
		console.log(selectedOption)
		console.log(buttonVal)

		if (d3.select("#ranking-type").property("value") === "revenue") {
			selectedOption = "revenue"

		} else {
			selectedOption = "stores"

		}

		dispData(selectedOption, buttonVal)

	});

	// check if button was clicked
	document.getElementById("change-sorting").onclick = () => {
		if (buttonVal === 1){
			buttonVal = 0
			//console.log(buttonVal)
		}else {
			buttonVal = 1
			//console.log(buttonVal)
		}

		dispData(selectedOption, buttonVal)
	}

  	// call function to display the appropriate bar chart data based on the selected dropdown value
	function dispData(selectedOption, buttonVal) {
		// sort the data (descending order)
		if (buttonVal === 1) {
			data.sort((a, b) => b[selectedOption] - a[selectedOption]);
		}else{
			data.sort((a, b) => a[selectedOption] - b[selectedOption]);
		}

		// define the domains of the axis
		x.domain(data.map(d => d.company))
		y.domain([0, d3.max(data, d => d[selectedOption])])

		svg.select(".x-axis")
			.transition()
			.duration(2000)
			.call(xAxis)

		svg.select(".y-axis")
			//.transition()
			//.duration(2000)
			.call(yAxis)

		if (selectedOption === "stores"){
			ylabel.text("Stores")
		}else{
			ylabel.text("Billion USD")
		}



		// draw the bars for the barchart
		let rect = svg.selectAll("rect")
			//.data(data, function(d) {return d[selectedOption]["company"]; })
			.data(data, d => d[selectedOption])



		rect.enter().append("rect")
			.attr("class", "bar")
			.merge(rect)
			.style("opacity", 0.5)
			.transition()
			.duration(2000)
			.style("opacity", 1)
			.attr("x", d => x(d.company))
			.attr("y", d => y(d[selectedOption]))
			.attr("width", x.bandwidth())
			.attr("height", d => height - y(d[selectedOption]))

		rect.exit().remove();
	}

}