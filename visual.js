csvFile = document.getElementById('csvFileName').value;
var parseTime;
if ( csvFile.search('daily') != -1 ){
    // parse the Date / time
    parseTime = d3.timeParse("%m-%d-%Y");
}
else if( csvFile.search('montly') != -1 ){
    parseTime = d3.timeParse("%m-%Y");
}
// set the dimensions and margins of the graph
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 1200 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;



// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// define the area
var area = d3.area()
    .x(function(d) {  return x(d.Date); })
    .y0(height)
    .y1(function(d) { return y(d.Price); });

// define the line
var valueline = d3.line()
    .x(function(d) { return x(d.Date); })
    .y(function(d) { return y(d.Price); });

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// get the data
d3.csv("../"+csvFile, function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {
      d.Date = parseTime(d.Date);
      d.Price = +d.Price;
  });

  // scale the range of the data
  x.domain(d3.extent(data, function(d) { return d.Date; }));
  y.domain([0, d3.max(data, function(d) { return d.Price; })]);

  // add the area
    svg.append("path")
       .data([data])
       .attr("class", "area")
       .attr("d", area);

  // add the valueline path.
  svg.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", valueline);

  // add the X Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  // add the Y Axis
  svg.append("g")
      .call(d3.axisLeft(y));

});