class ChartMap {

    constructor(parentElement, data, dataMarriages, dataBusiness) {
        this.parentElement = parentElement;
        this.data = data;
        this.marriageData = dataMarriages;
        this.businessData = dataBusiness;

        this.displayData = data;

        this.initVis();
    }


    /*
     * Initialize visualization (static content; e.g. SVG area, axes, brush component)
     */

    initVis() {
        let vis = this;

        vis.margin = {top: 50, right: 10, bottom: 20, left: 60};

        // TODO: #9 - Change hardcoded width to reference the width of the parent element
        vis.width = document.getElementById(vis.parentElement).getBoundingClientRect().width - vis.margin.left - vis.margin.right;
        vis.height = document.getElementById(vis.parentElement).getBoundingClientRect().height - vis.margin.top - vis.margin.bottom;

        vis.selectedOption = "index"


        // SVG drawing area
        vis.svg = d3.select("#" + vis.parentElement).append("svg")
            .attr("width", vis.width + vis.margin.left + vis.margin.right)
            .attr("height", vis.height + vis.margin.top + vis.margin.bottom)
            .append("g")
            .attr("transform", "translate(" + vis.margin.left + "," + vis.margin.top + ")")
            .style("background-color", "#EEE");

        // append top labels
        for (let m=0; m < vis.data.length; m++){
            vis.svg.append("text")
                .text(vis.data[m].Family)
                .attr("x", vis.margin.top*1.25)
                .attr("y", m*30 + vis.margin.left*2.25)
                .attr("transform", "translate(" + vis.margin.left + "," + vis.margin.top*5.2 + ") rotate(-90)");
        }



        // (Filter, aggregate, modify data)
        this.wrangleData();
    }


    /*
     * Data wrangling
     */

    wrangleData() {
        let vis = this;

        // Loop through all families and add the index, marriages array (& count), business array (& count)
        vis.displayData.forEach(addElements);

        function addElements(item, index, arr){
            //console.log(item)
            let numMarriages  = vis.marriageData.filter(row => row[index]==1).length;
            let numBusinesses = vis.businessData.filter(row => row[index]==1).length;

            item['index']          = index
            item['marriageValues'] = vis.marriageData[index]
            item['marriages']      = numMarriages
            item['businessValues'] = vis.businessData[index]
            item['businessTies']   = numBusinesses
            item['allRelations']   = numMarriages + numBusinesses

        }
        console.log(vis.displayData)




        // Update the visualization
        vis.updateVis();
    }



    /*
     * The drawing function
     */

    updateVis(selectedOption) {
        let vis = this;

        vis.displayData.sort((a, b) => b[selectedOption] - a[selectedOption]);

        vis.cellHeight = 20;
        vis.cellWidth = 20;
        vis.cellPadding = 10;

        vis.dataRow = vis.svg.selectAll(".matrix-row")
            .data(vis.displayData, function(d){
                return d.Family
            })

        vis.row = vis.dataRow.enter()
            .append("g")
            .attr("class", "matrix-row")

        vis.row.append("text")
            .attr("class", "label text")
            .text(function(d, index){
                console.log("here")
                return d.Family
            })
            .attr("x", vis.margin.left)
            .attr("y", 0)
            .attr('text-anchor', 'end')
            .attr("fill", "black")
            .attr("transform", "translate(" + vis.margin.left*1.8 + "," + vis.margin.top*4.55 + ")")


        vis.row.merge(vis.dataRow)  // merge ENTER + UPDATE groups
            .style('opacity', 0.5)
            .transition()
            .duration(500)
            .style('opacity', 1)
            .attr("transform", function (d, index) {
                return "translate(0," + (vis.cellHeight + vis.cellPadding) * index + ")";
            });

        // draw family names
        // let drawNames = vis.row.selectAll(".text")
        //     .data(function(d){
        //         //console.log(d.Family)
        //         return [d.Family]
        //     })
        // drawNames.enter().append("text")
        //     .attr("class", "label text")
        //     .text(function(d){return d})
        //     .attr("x", vis.margin.left)
        //     .attr("y", function(d, index) {
        //         console.log(d)
        //         return (vis.cellHeight + vis.cellPadding) * index })
        //     .attr('text-anchor', 'end')
        //     .attr("fill", "black")
        //     .attr("transform", "translate(" + vis.margin.left*1.8 + "," + vis.margin.top*4.55 + ")")


        vis.cellMatrix = vis.row.selectAll(".matrix-cells")
            //.data(function (d, i) {
            //    return d;
            //})
            .data(vis.displayData)
            .enter().append("rect")
            .attr("class", "matrix-cell")
            .attr("height", vis.cellHeight)
            .attr("width", vis.cellWidth)
            .attr("x", function (d, index) {
                return (vis.cellWidth + vis.cellPadding) * index
            })
            .attr("fill", "#ddd")
            .attr("transform", "translate(" + vis.margin.left*3 + "," + vis.margin.top*4.25 + ")");

        // draw marriage triangles
        vis.cellMarriage = vis.row.selectAll(".matrix-cell-marriage")
            .data(function(d){
                return d.marriageValues
            })
            .enter().append("path")
            .attr("class", "matrix-cell matrix-cell-marriage")
            .attr("height", vis.cellHeight)
            .attr("width", vis.cellWidth)
            .attr("fill", "#8686bf")
            .attr("d", function (d, index) {
                //console.log(d)
                //console.log("index", index)
                if (d === 1){
                    let x = (vis.cellWidth + vis.cellPadding)* index;
                    let y = 0;
                    return ('M ' + x + ' ' + y + ' l ' + vis.cellWidth + ' 0 l 0 ' + vis.cellHeight + ' z')
                }


            })
            .attr("transform", "translate(" + vis.margin.left*3 + "," + vis.margin.top*4.25 + ")");

        // draw business triangles
        vis.cellBusiness = vis.row.selectAll(".matrix-cell-business")
            .data(function(d){
                return d.businessValues
            })
            .enter().append("path")
            .attr("class", "matrix-cell matrix-cell-business")
            .attr("height", vis.cellHeight)
            .attr("width", vis.cellWidth)
            .attr("fill", "orange")
            .attr("d", function (d, index) {
                if (d === 1){
                    let x = (vis.cellWidth + vis.cellPadding)*index;
                    let y = vis.cellHeight;
                    return ('M ' + x + ' ' + y + ' l ' + (-vis.cellWidth) + ' 0 l 0 ' + (-vis.cellHeight) + ' z')
                }


            })
            .attr("transform", "translate(" + vis.margin.left*3.34 + "," + vis.margin.top*4.25 + ")");



    }
}


