/* * * * * * * * * * * * * *
*      class BarVis        *
* * * * * * * * * * * * * */


class BarVis {

    constructor(parentElement, covidData, usaData, order){

        this.parentElement = parentElement;
        this.covidData = covidData;
        this.usaData = usaData;
        this.descending = order;

        console.log(this.descending)

        // define colors
        this.colors = ['#D5F4F6', '#BFEEF2','#A9DADE' ,'#8BC7CC', '#5DA5AB', '#377D83',  '#1F595E', '#0E474C', '#072C2F']

        this.initVis()

        this.parseDate = d3.timeParse("%m/%d/%Y");
    }

    initVis(){
        let vis = this;

        vis.margin = {top: 20, right: 20, bottom: 20, left: 40};
        vis.width = document.getElementById(vis.parentElement).getBoundingClientRect().width - vis.margin.left - vis.margin.right;
        vis.height = document.getElementById(vis.parentElement).getBoundingClientRect().height - vis.margin.top - vis.margin.bottom;

        console.log("height: ", vis.height)

        // init drawing area
        vis.svg = d3.select("#" + vis.parentElement).append("svg")
            .attr("width", vis.width + vis.margin.left + vis.margin.right)
            .attr("height", vis.height + vis.margin.top + vis.margin.bottom)
            .append('g')
            .attr('transform', `translate (${vis.margin.left}, ${vis.margin.top})`);

        // add title
        vis.svg.append('g')
            .attr('class', 'title bar-title')
            .append('text')
            .text('Stats by State')
            .attr('transform', `translate(${vis.width / 2}, 0)`)
            .attr('text-anchor', 'middle');

        // tooltip
        vis.tooltip = d3.select("body").append('div')
            .attr('class', "tooltip")
            .attr('id', 'barTooltip')

        // Scales and axes
        vis.x = d3.scaleBand()
            .range([0, (vis.width - vis.margin.right)]);

        vis.y = d3.scaleLinear()
            .range([vis.height, 0]);

        vis.yAxis = d3.axisLeft()
            .scale(vis.y)
            .ticks(6);

        vis.xAxis = d3.axisBottom()
            .scale(vis.x)
            .ticks(6);

        vis.svg.append("g")
            .attr("class", "y-axis axis")
            .attr("id", "area-axis")
            .attr("transform", "translate(" + vis.margin.left/3 + "," + 0 + ")");

        vis.svg.append("g")
            .attr("class", "x-axis axis")
            .attr("id", "area-axis")
            .attr("transform", "translate(" + vis.margin.left/3 + "," + (vis.height) + ")");

        this.wrangleData();
    }

    wrangleData(selectedOption){
        let vis = this

        if (selectedOption === undefined){
            selectedOption = "absCases"
        }

        vis.tempStateInfo = {}

        // Pulling this straight from dataTable.js
        let filteredData = [];

        // if there is a region selected
        if (selectedTimeRange.length !== 0) {
            //console.log('region selected', vis.selectedTimeRange, vis.selectedTimeRange[0].getTime() )

            // iterate over all rows the csv (dataFill)
            vis.covidData.forEach(row => {
                // and push rows with proper dates into filteredData
                if (selectedTimeRange[0].getTime() <= vis.parseDate(row.submission_date).getTime() && vis.parseDate(row.submission_date).getTime() <= selectedTimeRange[1].getTime()) {
                    filteredData.push(row);
                }
            });
        } else {
            filteredData = vis.covidData;
        }

        // prepare covid data by grouping all rows by state
        let covidDataByState = Array.from(d3.group(filteredData, d => d.state), ([key, value]) => ({key, value}))
        
        // init final data structure in which both data sets will be merged into
        vis.stateInfo = []

        // merge
        covidDataByState.forEach(state => {

            // get full state name
            let stateName = nameConverter.getFullName(state.key)

            // init counters
            let newCasesSum = 0;
            let newDeathsSum = 0;
            let population = 0;

            // look up population for the state in the census data set
            vis.usaData.forEach(row => {
                if (row.state === stateName) {
                    population += +row["2020"].replaceAll(',', '');
                }
            })

            // calculate new cases by summing up all the entries for each state
            state.value.forEach(entry => {
                newCasesSum += +entry['new_case'];
                newDeathsSum += +entry['new_death'];
            });

            // populate the final data structure
            if (stateName === ('US Virgin Islands')) {
                //console.log('skip state')
            }else if (stateName === ('Guam')) {
                //console.log('skip state')
            }else if(stateName === ('American Samoa')) {
                //console.log('skip state')
            }else {
                vis.stateInfo.push(
                    {
                        state: stateName,
                        population: population,
                        absCases: newCasesSum,
                        absDeaths: newDeathsSum,
                        relCases: (newCasesSum / population * 100),
                        relDeaths: (newDeathsSum / population * 100)
                    }
                )
            }
        })
        // TODO: Sort and then filter by top 10
        // maybe a boolean in the constructor could come in handy ?

        console.log("bar chart data: ", vis.stateInfo)
        console.log('selected option', selectedOption)

        if (vis.descending){
            vis.stateInfo.sort((a,b) => {return b[selectedOption] - a[selectedOption]})
        } else {
            vis.stateInfo.sort((a,b) => {return a[selectedOption] - b[selectedOption]})
        }

        console.log('pre final data structure', vis.stateInfo);

        // add color to each of the states to correspond with the map
        let colorDiv = 6, colorIdx = 8;

        vis.stateInfo.forEach((d, index) => {
            if (index < colorDiv){
                console.log("d", d)
                let correctColor = {
                    color: vis.colors[colorIdx]
                }
                Object.assign(d, correctColor)
            }else{
                let correctColor = {
                    color: vis.colors[colorIdx]
                }
                Object.assign(d, correctColor)
                colorDiv = colorDiv + 6
                colorIdx = colorIdx - 1
            }

        })

        vis.topTenData = vis.stateInfo.slice(0, 10)

        console.log('final data structure', vis.topTenData);



        vis.updateVis(selectedOption)

    }

    updateVis(selectedOption){
        let vis = this;

        if (selectedOption === undefined){
            selectedOption = "absCases"
        }


        console.log('here')
        console.log(selectedOption)

        // define the domains of the axis
        vis.x.domain(vis.topTenData.map(d => d.state))
        vis.y.domain([0, d3.max(vis.topTenData, function(d) {
            return d[selectedOption]}

        )])

        vis.svg.select(".x-axis")
            .transition()
            .duration(5000)
            .call(vis.xAxis)

        vis.svg.select(".y-axis")
            .transition()
            .duration(5000)
            .call(vis.yAxis)


        // -------------------------------------------------------------------------------------------------------------
        // (2) Draw rectangles
        let drawBars = vis.svg.selectAll("rect")
            .data(vis.topTenData)

        drawBars.enter().append("rect")
            .attr("class", "bars")
            .merge(drawBars)
            .transition()
            .duration(1000)
            .attr("x", d => vis.x(d.state) + vis.margin.left/3)
            .attr("y", d => vis.y(d[selectedOption]))
            .attr("width", vis.x.bandwidth())
            .attr("height", function(d) {
                //console.log(selectedOption)
                //console.log("ss", d[selectedOption])
                return (vis.height - vis.y(d[selectedOption]))
            })
            .attr("fill", d => d.color)
            //.attr("stroke", "black")
            //.attr("stroke-width", 1.5)

        drawBars.exit().transition().remove();
        // -------------------------------------------------------------------------------------------------------------

        // Add the tool tip
        drawBars.on('mouseover', function(event, d){
            vis.tooltip
                .style("opacity", 1)
                .style("left", event.pageX + 20 + "px")
                .style("top", event.pageY + "px")
                .html(`
                 <div style="border: thin solid grey; border-radius: 5px; background: lightgrey; padding: 15px; font-size: 5px;">
                     <h4 style="font-weight: bold">${d.state}<h4>
                     <p style="font-size: 15px"> 
                     State:  ${d.state} <br> 
                     absCases:  ${d.absCases} <br> 
                     absDeaths:  ${d.absDeaths} <br> 
                     Population:  ${d.population} <br> 
                     relCases:  ${(d.relCases).toFixed(3)}  % <br> 
                     relDeaths:  ${(d.relDeaths).toFixed(3)} % 
                     </p>                    
                 </div>`)
            d3.select(this).attr("fill", "indianred")
        })


        drawBars.on('mouseout', function(event, d) {
            vis.tooltip
                .style("opacity", 0)
                .style("left", 0)
                .style("top", 0)
                .html(``);
            d3.select(this).attr("fill", function (d) {
                return d.color
            })
        })

        // Update axes
        vis.svg.select(".y-axis")
            .transition()
            .duration(1500)
            .call(vis.yAxis);
        vis.svg.selectAll(".x-axis").transition().duration(1500).call(vis.xAxis)
            .selectAll("text")
            .attr("transform", "rotate(-15)");

    }



}