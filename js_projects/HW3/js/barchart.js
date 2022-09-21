

/*
 * BarChart - Object constructor function
 * @param _parentElement 	-- the HTML element in which to draw the bar charts
 * @param _data						-- the dataset 'household characteristics'
 * @param _config					-- variable from the dataset (e.g. 'electricity') and title for each bar chart
 */


class BarChart {

	constructor(parentElement, data, config) {
		this.parentElement = parentElement;
		this.data = data;
		this.config = config;
		this.displayData = data;

		console.log(this.displayData);

		this.initVis();
	}




	/*
	 * Initialize visualization (static content; e.g. SVG area, axes)
	 */

	initVis() {
		let vis = this;


		// * TO-DO *

		vis.margin = {top: 40, right: 20, bottom: 15, left: 75}

		vis.width = document.getElementById(vis.parentElement).getBoundingClientRect().width - vis.margin.left - vis.margin.right;
		vis.height = document.getElementById(vis.parentElement).getBoundingClientRect().height - vis.margin.top - vis.margin.bottom;

		// svg drawing area
		vis.svg = d3.select("#" + vis.parentElement).append("svg")
			.attr("width", vis.width + vis.margin.left + vis.margin.right)
			.attr("height", vis.height/5 + vis.margin.top + vis.margin.bottom)
			.append("g")
			.attr("transform", "translate(" + vis.margin.left + "," + vis.margin.top + ")")

		// Scales and axes
		vis.x = d3.scaleLinear()
			.range([0, vis.width - vis.margin.right - vis.margin.left])
			.domain([0,d3.max(vis.data, function(d){
				return d.value
			})]);

		vis.y = d3.scaleBand()
			.range([0, vis.height/4])
			.domain(d3.map(vis.data, function(d){
				return d.key
			}));

		vis.yAxis = d3.axisLeft()
		 	.scale(vis.y);

		vis.svg.append("g")
			.attr("class", "y-axis axis")
			.attr("id", "bar-axis")
			.attr("transform", "translate(" + vis.margin.left + "," + 0 + ")")
			.call(d3.axisLeft(vis.y));

		vis.svg.append("text")
			.attr("class", "bar-titles")
			.attr("x", vis.margin.left)
			.attr("y", vis.height - vis.margin.top)
			.attr("y", -vis.margin.top/4)
			.text(vis.config.title)

		// (Filter, aggregate, modify data)
		vis.wrangleData();


	}


	/*
	 * Data wrangling
	 */

	wrangleData() {
		let vis = this;

		// (1) Group data by key variable (e.g. 'electricity') and count leaves
		// (2) Sort columns descending


		// * TO-DO *

		let currentConfig = vis.config.key
		let currentData = vis.displayData
		let groupedData = d3.group(currentData, d=>d[currentConfig])
		//console.log(groupedData)

		let countConfig = d3.rollup(currentData, groupedData=>groupedData.length, d=>d[currentConfig])
		let arrayConfig = Array.from(countConfig, ([key, value]) => ({key, value}))

		// sort in descending order
		vis.sortedConfig = arrayConfig.sort((a,b)=>d3.descending(a.value,b.value))
		//console.log(vis.sortedConfig)


		// Update the visualization
		vis.updateVis();
	}



	/*
	 * The drawing function - should use the D3 update sequence (enter, update, exit)
	 */

	updateVis() {
		let vis = this;

		// (1) Update domains
		vis.x.domain([0, d3.max(vis.sortedConfig, function(d){
			return d.value
		})]);

		vis.y.domain(d3.map(vis.sortedConfig, function(d){
			return d.key
		}));

		// (2) Draw rectangles
		let drawBars = vis.svg.selectAll("rect")
			.data(vis.sortedConfig)

		drawBars.enter().append("rect")
			.attr("class", "bars")
			.merge(drawBars)
			.transition()
			.duration(150)
			.attr("x", vis.margin.left)
			.attr("y", function(d){return vis.y(d.key); })
			.attr("width", function(d){return vis.x(d.value); })
			.attr("height", vis.y.bandwidth()-2.5)
			.attr("stroke", "black")
			.attr("stroke-width", 1.5)

		drawBars.exit().transition().remove();

		// (3) Draw labels
		let drawValues = vis.svg.selectAll(".text")
			.data(vis.sortedConfig);

		drawValues.enter().append("text")
			.attr("class", "label text")
			.attr("id", "value-labels")
			.merge(drawValues)
			.transition()
			.duration(150)
			.text(function(d){return d.value})
			.attr("x", function(d){return vis.x(d.value) + vis.margin.left + vis.margin.right;}) // vis.width-vis.margin.right)
			.attr("y", function(d){return vis.y(d.key) + 15; })
			.attr('text-anchor', 'middle')
			.attr("fill", "black")
			.attr("font-family", "calibri light")

		drawValues.exit().transition().remove();


		// * TO-DO *


		// Update the y-axis
		vis.svg.select(".y-axis")
			.transition()
			.duration(250)
			.call(vis.yAxis);
	}



	/*
	 * Filter data when the user changes the selection
	 * Example for brushRegion: 07/16/2016 to 07/28/2016
	 */

	selectionChanged(brushRegion) {
		let vis = this;



		// Filter data accordingly without changing the original data
		vis.displayData = vis.data.filter(d => ((d.survey > brushRegion[0]) && (d.survey < brushRegion[1])))

		// * TO-DO *
		console.log(vis.displayData)

		// Update the visualization
		vis.wrangleData();
	}
}
