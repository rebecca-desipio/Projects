// Bar chart configurations: data keys and chart titles
let configs = [
    {key: "ownrent", title: "Own or Rent"},
    {key: "electricity", title: "Electricity"},
    {key: "latrine", title: "Latrine"},
    {key: "hohreligion", title: "Religion"}
];


// Initialize variables to save the charts later
let barcharts = [];
let areachart;


// Date parser to convert strings to date objects
let parseDate = d3.timeParse("%Y-%m-%d");


// (1) Load CSV data
// 	(2) Convert strings to date objects
// 	(3) Create new bar chart objects
// 	(4) Create new are chart object

d3.csv("data/household_characteristics.csv",(d)=> {
        d.survey = parseDate(d.survey);
        return d;
    }).then(data => {


    // * TO-DO *
    console.log(data)
    let OwnOrRent   = new BarChart("four-bar-chart", data, configs[0])
    let Electricity = new BarChart("four-bar-chart", data, configs[1])
    let Latrine     = new BarChart("four-bar-chart", data, configs[2])
    let Religion    = new BarChart("four-bar-chart", data, configs[3])

    barcharts = [OwnOrRent, Electricity, Latrine, Religion];

    areachart = new AreaChart("area-chart", data)



});


// React to 'brushed' event and update all bar charts
function brushed() {

    let selectionRange = d3.brushSelection(d3.select(".brush").node());
    let selectionDomain = (selectionRange.map(areachart.x.invert));

    barcharts[0].selectionChanged(selectionDomain)
    barcharts[0].x.domain(selectionRange.map(areachart.x.invert));
    barcharts[0].wrangleData()

    barcharts[1].selectionChanged(selectionDomain)
    barcharts[1].x.domain(selectionRange.map(areachart.x.invert));
    barcharts[1].wrangleData()

    barcharts[2].selectionChanged(selectionDomain)
    barcharts[2].x.domain(selectionRange.map(areachart.x.invert));
    barcharts[2].wrangleData()

    barcharts[3].selectionChanged(selectionDomain)
    barcharts[3].x.domain(selectionRange.map(areachart.x.invert));
    barcharts[3].wrangleData()

}
