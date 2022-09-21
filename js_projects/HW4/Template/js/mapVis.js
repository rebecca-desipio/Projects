/* * * * * * * * * * * * * *
*          MapVis          *
* * * * * * * * * * * * * */


class MapVis {

    constructor(parentElement, geoData, covidData, usaData) {
        this.parentElement = parentElement;
        this.geoData = geoData;
        this.covidData = covidData;
        this.usaData = usaData;

        this.parseDate = d3.timeParse("%m/%d/%Y");

        // define colors
        this.colors = ['#D5F4F6', '#BFEEF2','#A9DADE' ,'#8BC7CC', '#5DA5AB', '#377D83',  '#1F595E', '#0E474C', '#072C2F']

        this.initVis()
    }

    initVis(){
        let vis = this;
        vis.selectedOption = "relCases"

        vis.margin = {top: 20, right: 20, bottom: 20, left: 20};
        vis.width = document.getElementById(vis.parentElement).getBoundingClientRect().width - vis.margin.left - vis.margin.right;
        vis.height = document.getElementById(vis.parentElement).getBoundingClientRect().height - vis.margin.top - vis.margin.bottom;

        // init drawing area
        vis.svg = d3.select("#" + vis.parentElement).append("svg")
            .attr("width", vis.width)
            .attr("height", vis.height)
            .attr('transform', `translate (${vis.margin.left}, ${vis.margin.top})`);

        // Display the map
        vis.projection = d3.geoAlbersUsa()
            .scale((vis.height/150) * 249.5)
            .translate([vis.width / 2, vis.height / 2])

        vis.path = d3.geoPath()
            .projection(vis.projection);

        vis.usa = topojson.feature(vis.geoData, vis.geoData.objects.states).features

        vis.states = vis.svg.selectAll(".states")
            .data(vis.usa)
            .enter().append("path")
            .attr('class', 'country')
            .attr("d", vis.path)

        // Add the tool-tip
        vis.map_tt = d3.select("body").append('div')
            .attr('class', "tooltip")
            .attr('id', 'mapTooltip')

        // Add legend
        // define scale
        vis.legendScale = d3.scaleLinear()
            .range([0, 180])


        // define axis
        vis.legendAxis = d3.axisBottom()
            .scale(vis.legendScale)
            .ticks(3)

        vis.legend = vis.svg.append("g")
            .attr('class', 'legend')
            .attr('transform', `translate(${vis.width * 2.8 / 5.5}, ${vis.height - 20})`)
            //.call(vis.legendAxis)

        vis.legend.selectAll('.bar')
            .data(vis.colors)
            .enter()
            .append("rect")
            .attr("x", (d,i)=> i*20)
            .attr('y', -20)
            .attr("width", 20)
            .attr('height', 19)
            .attr("fill", d => d)

        vis.wrangleData()



    }

    wrangleData(selectedOption){
        let vis = this;

        if (selectedOption === undefined){
            selectedOption = "relCases"
        }

        // first, filter according to selectedTimeRange, init empty array
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

        // have a look
        // console.log(covidDataByState)

        // init final data structure in which both data sets will be merged into
        vis.stateDataMap = {}
        vis.tempStateData = []

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
                vis.tempStateData.push(
                    {
                        state: stateName,
                        population: population,
                        absCases: newCasesSum,
                        absDeaths: newDeathsSum,
                        relCases: (newCasesSum / population * 100),
                        relDeaths: (newDeathsSum / population * 100),
                        color: "green"

                    }
                )
            }





        })

        vis.tempStateData.sort((a, b) => b[selectedOption] - a[selectedOption])

        vis.tempMaxData = d3.max(vis.tempStateData, d => d[selectedOption])
        console.log("max value", vis.tempMaxData)

        let colorDiv = 6, colorIdx = 8, correctColor;

        vis.tempStateData.forEach((d, index) => {
            if (index < colorDiv){
                correctColor = vis.colors[colorIdx]
            }else{
                colorDiv = colorDiv + 6
                colorIdx = colorIdx - 1
            }

                vis.stateDataMap[d.state] = {
                    state: d.state,
                    population: d.population,
                    absCases: d.absCases,
                    absDeaths: d.absDeaths,
                    relCases: (d.absCases / d.population * 100),
                    relDeaths: (d.absDeaths / d.population * 100),
                    color: correctColor

                }


        })


        console.log("temp Data", vis.tempStateData)

        vis.updateVis()
    }

    updateVis(){
        let vis = this;

        console.log('State Info: ', vis.stateDataMap)

        // update legend domain
        vis.legendScale.domain([0, vis.tempMaxData])
        vis.legend.call(vis.legendScale)


        vis.states
            .attr("fill", function(d, index) {
                //console.log(d)
                if (d.properties.name === ('Commonwealth of the Northern Mariana Islands')) {
                    //console.log('skip again')
                }else if (d.properties.name === 'Guam') {
                    //console.log('skip again')
                }else if (d.properties.name === 'American Samoa') {
                    //console.log('skip again')
                }else if (d.properties.name ==='US Virgin Islands') {
                    //console.log('skip again')
                }else{
                    if (d.properties.name !== 'United States Virgin Islands') {
                        return vis.stateDataMap[d.properties.name].color
                    }
                }
            })

        // tool tip feature
        vis.states.on('mouseover', function(event, d){
            vis.map_tt
                .style("opacity", 1)
                .style("left", event.pageX + 20 + "px")
                .style("top", event.pageY + "px")
                .html(`
                 <div style="border: thin solid grey; border-radius: 5px; background: lightgrey; padding: 15px; font-size: 5px;">
                     <h4 style="font-weight: bold">${vis.stateDataMap[d.properties.name].state}<h4>
                     <p style="font-size: 15px"> 
                     State:  ${vis.stateDataMap[d.properties.name].state} <br> 
                     absCases:  ${vis.stateDataMap[d.properties.name].absCases} <br> 
                     absDeaths:  ${vis.stateDataMap[d.properties.name].absDeaths} <br> 
                     Population:  ${vis.stateDataMap[d.properties.name].population} <br> 
                     relCases:  ${(vis.stateDataMap[d.properties.name].relCases).toFixed(3)}  % <br> 
                     relDeaths:  ${(vis.stateDataMap[d.properties.name].relDeaths).toFixed(3)} % 
                     </p>                    
                 </div>`)
            d3.select(this).attr("fill", "indianred")
        })


        vis.states.on('mouseout', function(event, d){
            vis.map_tt
                .style("opacity", 0)
                .style("left", 0)
                .style("top", 0)
                .html(``);
            d3.select(this).attr("fill", function(d){
                return vis.stateDataMap[d.properties.name].color
            })
        })

        vis.svg.select(".legend").transition().duration(500).call(vis.legendAxis)

    }




}