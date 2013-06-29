function drawGraph(data, latIndex, longitude) {
    rs = data[latIndex + 13];
    var w = 900;
    var h = 400;
    var scaleHeight = 24;
    var scaleWidth = 13;

    var OMEGA = 360 / 86164.0905;

    var xFunc = d3.scale.linear().domain([1, scaleWidth]).range([1, w]);
    var yFunc = d3.scale.linear().domain([0, scaleHeight]).range([h, 0]);

    var getUTCOffset = function(longitude) {
        var longOffset = null;
        if (longitude <= 0) {
            longOffset = longitude + 7.5;
        }
        else {
            longOffset = longitude - 7.5;
        }
        var UTCOffset = Math.floor(longOffset / 15); 
        return UTCOffset;
    };

    var getLongCorrection = function(longitude) {
        var correctionSeconds = -longitude / OMEGA;
        var correctionHours = correctionSeconds / 3600;
        return correctionHours;
    };

    var normalizeTime = function(time) {
        if (time < 0) {
            time += 24;
        }
        return time % 24;
    }

    d3.select('svg').remove();

    var chart = d3.select('#chart1')
        .append('svg')
        .attr('width', w + 130)
        .attr('height', h + 130)
        .append('svg:g')
        .attr('transform', function(d) { return 'translate(130, 20)' });

    var riseLine = d3.svg.line()
        .x(function(d) { return xFunc(12*d.day/366 + 1) })
        .y(function(d) { 
            return yFunc(normalizeTime(d.rise + getLongCorrection(longitude) + getUTCOffset(longitude))) 
        })
        .interpolate('linear');

    var setLine = d3.svg.line()
        .x(function(d) { return xFunc(12*d.day/366 + 1) })
        .y(function(d) { 
            return yFunc(normalizeTime(d.set + getLongCorrection(longitude)+ getUTCOffset(longitude))) 
        })
        .interpolate('linear');

    var dayLightLine = d3.svg.line()
        .x(function(d) { return xFunc(12*d.day/366 + 1) })
        .y(function(d) { return yFunc(d.set - d.rise) })
        .interpolate('linear');

    var yTicks = chart.selectAll('.ticky')
        .data(yFunc.ticks(24))
        .enter()
        .append('svg:g')
        .attr('transform', function(d) { return 'translate(0, ' + yFunc(d) + ')' })
        .attr('class', function(d) { return 'ticky index' + d });

    yTicks.append('svg:line')
        .attr('y1', 0)
        .attr('y2', 0)
        .attr('x1', 0)
        .attr('x2', w)
        .attr('stroke', '#000000')
        .attr('stroke-width', function(d) {
            if (d % 6 == 0) {
                return 2.5;
            }
            return 1;
        });

    yTicks.append('svg:text')
        .text(function(d) { return d })
        .attr('text-anchor', 'end')
        .attr('dy', 2)
        .attr('dx', -4)
        .attr('fill', '#000000')
        .attr('font-size', '14px')
        .attr('color', '#000000');

    var xAxis = chart.selectAll('.ticky.index0');
    xAxis.append('svg:text')
        .text('Date (Month/Day)')
        .attr('dy', 50)
        .attr('dx', 400)
        .attr('font-size', '20px')
        .attr('fill', '#000000')
        .attr('color', '#000000');

    var latIndices = [];
    for (i = 0; i < 27; i++) {
        latIndices[i] = i;
    }

    var latTicks = chart.selectAll('.latTick')
        .data(latIndices)
        .enter()
        .append('svg:g')
        .attr('transform', function(d) { 
            return 'translate(-90, ' + (200 + ((13 - d) * 5) * 200 / 65) + ')' 
        });

    latTicks.append('svg:g')
        .attr('transform', function(d) {
            return 'translate(-30, 0)';
        })
        .append('svg:line')
        .attr('x1', 0)
        .attr('y1', 0) 
        .attr('x2', -10)
        .attr('y2', 0)
        .attr('stroke', '#CCC')
        .attr('stroke-width', 1)

    latTicks.append('svg:text')
        .text(function(d) {
            return (d - 13) * 5;
        })
        .attr('text-anchor', 'end')
        .attr('dy', 5)
        .attr('fill', '#CCC')
        .attr('font-size', '12px')
        .attr('color', '#000')
        .attr('class', function(d) {
            var result = 'latTick index' + d;
            return result;
        });
    
    var longIndices = [];
    for (i = 0; i < 37; i++) {
        longIndices[i] = i;
    }

    var longTicks = chart.selectAll('.longTick')
        .data(longIndices)
        .enter()
        .append('svg:g')
        .attr('transform', function(d) { 
            return 'translate(' + (450 + ((18 - d) * 10) * 450 / 180 - 5) + ', 490)' 
        });

    longTicks.append('svg:line')
        .attr('x1', 0)
        .attr('y1', 0) 
        .attr('x2', 0)
        .attr('y2', -10)
        .attr('stroke', '#777')
        .attr('stroke-width', 1)

    longTicks.append('svg:g')
        .attr('transform', function(d) {
            return 'translate(3, 0)';
        })
        .append('svg:text')
        .text(function(d) {
            return (18 - d) * 10;
        })
        .attr('text-anchor', 'end')
        .attr('dy', 10)
        .attr('dx', 0)
        .attr('fill', '#777')
        .attr('font-size', '10px')
        .attr('color', '#000')
        .attr('class', function(d) {
            var result = 'longTick index' + d;
            return result;
        });

    var curLongTick = chart.selectAll('.curLongTick')
        .data([0]).enter()
        .append('svg:g')
        .attr('transform', function(d) { 
            return 'translate(' + (450 + ((18 - d) * 10) * 450 / 180 -5) + ', 490)' 
        })
        .attr('class', 'curLongTick');

    curLongTick.append('svg:line')
        .attr('x1', 0)
        .attr('y1', 0) 
        .attr('x2', 0)
        .attr('y2', -20)
        .attr('stroke', '#000')
        .attr('stroke-width', 1)

    var xTicks = chart.selectAll('.tickx')
        .data(xFunc.ticks(13))
        .enter()
        .append('svg:g')
        .attr('transform', function(d) { return 'translate(' + xFunc(d) + ' , 0)' })
        .attr('class', function(d) {
            return 'tickx index' + d;
        });

    xTicks.append('svg:line')
        .attr('y1', 0)
        .attr('y2', h)
        .attr('x1', 0)
        .attr('x2', 0)
        .attr('stroke', '#000000')
        .attr('stroke-width', function(d) {
            if (d % 6 == 0) {
                return 1;
            }
            return 1;
        });

    xTicks.append('svg:text')
        .text(function(d) {
            if (d == 13) {
                return '';
            }
            return d + '/1';
        })
        .attr('text-anchor', 'end')
        .attr('dy', 20)
        .attr('dx', 9)
        .attr('fill', '#000000')
        .attr('font-size', '14px')
        .attr('color', '#000000')
        .attr('y', h);
   
    var yAxis = d3.select('.tickx.index1');
    yAxis.append('svg:g')
        .attr('transform', 'translate(-35, 150)')
        .append('svg:g')
        .attr('transform', 'rotate(-90)')
        .append('svg:text')
        .text('Time (24 Hours)')
        .attr('text-anchor', 'end')
        .attr('fill', '#000000')
        .attr('font-size', '20px')
        .attr('color', '#000000');

    chart.append('path')
        .attr('d', riseLine(rs)) 
        .attr('stroke', 'blue')
        .attr('stroke-width', 3)
        .attr('fill', 'none');

    chart.append('path')
        .attr('d', setLine(rs))
        .attr('stroke', 'red')
        .attr('stroke-width', 3)
        .attr('fill', 'none');

    chart.append('path')
        .attr('d', dayLightLine(rs))
        .attr('stroke', 'green')
        .attr('stroke-width', 3)
        .attr('fill', 'none');
}
