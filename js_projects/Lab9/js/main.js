
let chartmap;

d3.csv("data/florentine-family-attributes.csv").then(data => {
    // * TO-DO *
    let dataMarriages = [
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0],
        [0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,1,1,0,0,0,0,0,1,0,1,0,0,0],
        [0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0]
    ];

    let dataBusiness = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0],
        [0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,1],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
    ];

    console.log("Family Attributes: ", data)
    console.log("Marriages: ", dataMarriages)
    console.log("Business Relations: ", dataBusiness)

    chartmap = new ChartMap("chart-map", data, dataMarriages, dataBusiness)
});

// update visualization based on selected dropdown
document.getElementById("sort-by").onchange = function() {

    chartmap.updateVis(this.value)

}

    // if (vis.selectedOption === "businessTies") {
    //     vis.displayData.sort((a, b) => b[vis.selectedOption] - a[vis.selectedOption]);
    // }else if (vis.selectedOption === "marriages") {
    //     vis.displayData.sort((a, b) => b[vis.selectedOption] - a[vis.selectedOption]);
    // }else if (vis.selectedOption === "allRelations") {
    //     vis.displayData.sort((a, b) => b[vis.selectedOption] - a[vis.selectedOption]);
    // }else if (vis.selectedOption === "Wealth") {
    //     vis.displayData.sort((a, b) => b[vis.selectedOption] - a[vis.selectedOption]);
    // }else if (vis.selectedOption === "Priorates") {
    //     vis.displayData.sort((a, b) => b[vis.selectedOption] - a[vis.selectedOption]);
    // }else{
    //     vis.displayData.sort((a, b) => a[vis.selectedOption] - b[vis.selectedOption]);
    // }
    //
    // console.log("sorted disp data: ", vis.displayData)
    //
    // vis.updateVis()
