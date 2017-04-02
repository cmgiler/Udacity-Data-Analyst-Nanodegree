
Element.prototype.getElementById = function(id) {
    return document.getElementById(id);
}

// Main drawing function (draws both map and chart)
function draw(data) {
    "use_strict";
    
    //Initialize Map (based on current window height and width)
    var map_margin = 0
    element = document.getElementById('plot-map')
    var map_width = element.clientWidth
    var map_height = element.clientHeight

    var svg_map = d3.select('#plot-map')
                    .append('svg')
                    .attr('width', map_width)
                    .attr('height', map_height)
                    .append('g')
                    .attr('class', 'map');

    //Initialize Chart (also based on current window height and width)
    var ch_margin = 65
    ch_element = document.getElementById('plot-line')
    var ch_width = ch_element.offsetWidth+ch_margin/1.2
    var ch_height = ch_element.offsetHeight-ch_margin

    var svg_chart = d3.select('#plot-line')
                      .append('svg')
                      .attr('width', ch_width)
                      .attr('height', ch_height)
                      .on('click', handleMouseClick)
                      .append('g')
                      .attr('class','chart');

    // List of carriers open to user selection
    var carrier_options = {
        'AA' : 'American Airlines',
        'AS' : 'Alaska Airlines',
        'B6' : 'JetBlue Airways',
        'DL' : 'Delta Airlines',
        'F9' : 'Frontier Airlines',
        'HA' : 'Hawaiian Airlines',
        'NW' : 'Northwest Airlines',
        'US' : 'US Airways',
        'VX' : 'Virgin America',
        'WN' : 'Southwest Airlines'
    }

    // List of metrics open to user selection
    var metric_options = {
        'arr_del15_pct' : 'All Flight Delays',
        'arr_cancelled_pct' : 'Flights Cancelled',
        'carrier_delay_pct' : 'Carrier Delays',
        'late_aircraft_delay_pct' : 'Late Aircraft Delays',
        'nas_delay_pct' : 'NAS Delays',
        'security_delay_pct' : 'Security Delays',
        'weather_delay_pct' : 'Weather Delays',
        'arr_flights_sum' : 'Total Flights'
    };
    
    // Initialize selection to first carrier and metric in lists
    keys = [];
    for (var k in carrier_options) keys.push(k);
    var carrier = keys[0];
    keys = [];
    for (var k in metric_options) keys.push(k);
    var metric = keys[0];


    // Create Event Handlers for mouse
    function handleMouseOver(d, i) {  // Add interactivity

        // Use D3 to select element, change color and size
        d3.select(this).attr({
          r: this.getAttribute('r') * 1.2
        });

        // Specify where to put label of text (tooltip)
        d3.select('.main-panel').append("div").attr({
           id: "map_tooltip"
        })
        .style("opacity", 0.9)
        .style('font', '16px sans-serif')
        .html(d.values.airport)
        .style("left", (d3.event.clientX) + "px")
        .style("top", (d3.event.clientY) + "px");
        
    }

    function handleMouseClick(d, i) {
        // Toggles opacity for chart lines based on which carrier is selected

        // If clicking in empty space within map or chart area, reset opacity for all chart paths
        if (this.tagName != 'circle' && this.getElementsByClassName('d3-dp-line')[0] == undefined) {
            var carrier_options = {
                'AA' : 'American Airlines',
                'AS' : 'Alaska Airlines',
                'B6' : 'JetBlue Airways',
                'DL' : 'Delta Airlines',
                'F9' : 'Frontier Airlines',
                'HA' : 'Hawaiian Airlines',
                'NW' : 'Northwest Airlines',
                'US' : 'US Airways',
                'VX' : 'Virgin America',
                'WN' : 'Southwest Airlines'
            }
            d3.selectAll('.scatterPlotGroup')
                .selectAll('path')
                .transition()
                .ease('linear')
                .duration('500')
                .style('stroke-opacity', function(d) {
                    return 1;
                });

            d3.selectAll('.scatterPlotGroup')
                .selectAll('circle')
                .transition()
                .ease('linear')
                .duration('500')
                .style('visibility', function(d) {
                    return 'visible';
                });
            
            var cur_carrier = document.getElementsByClassName('btn-link')[0].id;
            document.getElementById('active-hubs').innerHTML = 
                    document.getElementById('active-carrier').innerHTML;
        }
        // If circle is selected, highlight corresponding path line in chart
        else if (this.tagName == 'circle') {
            selected_airport = this.id;
            if (this.id == "") {
                selected_airport = d.airport;
            }
            d3.selectAll('.scatterPlotGroup')
                .selectAll('path')
                .transition()
                .ease('linear')
                .duration('250')
                .style('stroke-opacity', function(d) {
                    if (d.key != selected_airport) {
                        return 0.1;
                    }
                    else {
                        return 0.95;
                    };
                })
            d3.selectAll('.scatterPlotGroup')
                .selectAll('circle')
                .transition()
                .ease('linear')
                .duration('250')
                .style('visibility', function(d) {
                    if (d.airport != selected_airport) {
                        return 'hidden';
                    }
                })
            if (d.key == undefined) {
                document.getElementById('active-hubs').innerHTML = 
                    d.airport_name + ' (' + selected_airport + ')';
            }
            else {
                document.getElementById('active-hubs').innerHTML = 
                    d.values.airport_name + ' (' + selected_airport + ')';
            }
        }
    }

    function handleMouseOut(d, i) {

        // Use D3 to select element, change color back to normal
        d3.select(this).attr({
          r: this.getAttribute('r') / 1.2
        });

        // Select text by id and then remove tooltip
        d3.select("#map_tooltip").remove();  // Remove text location

    }

    function handleMouseOverChart(d, i) {
        // Manage drawing/animating tooltips and drop lines for chart
        var d3Chart = d3.select('#plot-line svg');
        var dpX1 = this.getAttribute('cx');
        var dpY1 = this.getAttribute('cy');
        var dpY2 = document.getElementsByClassName('x axis')[0].getAttribute('y');
        var dpX2 = document.getElementsByClassName('y axis')[0].getAttribute('x');
        
        var myLine_x = d3Chart.append("svg:line")
            .attr("class", 'd3-dp-line')
            .attr("x1", dpX1)
            .attr("y1", dpY1)
            .attr("x2", dpX1)
            .attr("y2", dpY1)
            .style("stroke-dasharray", ("5, 3"))
            .style("stroke-opacity", 0.9)
            .style("stroke", 'black')
            .transition()
            .duration(200)
            .ease('linear')
            .attr("y2", dpY2);
            

        var myLine_y = d3Chart.append("svg:line")
            .attr("class", 'd3-dp-line')
            .attr("x1", dpX1)
            .attr("y1", dpY1)
            .attr("x2", dpX1)
            .attr("y2", dpY1)
            .style("stroke-dasharray", ("5, 3"))
            .style("stroke-opacity", 0.9)
            .style("stroke", 'black')
            .transition()
            .duration(200)
            .ease('linear')
            .attr("x2", dpX2);

        if (document.getElementsByClassName('btn-link')[1].id == 'arr_flights_sum') {
                var tooltip_text = d.x + "\n" + Math.round(d.y)
                if (tooltip_text[tooltip_text.length - 4] != '\n') {
                    tooltip_text = tooltip_text.substring(0, tooltip_text.length - 3) +
                                   ',' + 
                                   tooltip_text.substring(tooltip_text.length - 3, tooltip_text.length)
               }
            }
            else {
                var tooltip_text = d.x + "\n" + Math.round(d.y*100)/100 + '%'
            }
        this.setAttribute('r', this.getAttribute('r')*1.5)
        d3.select('.main-panel').append("div").attr({
           id: "map_tooltip"
        })
        .style("opacity", 0.9)
        .html(tooltip_text)
        .style("left", (d3.event.clientX) + "px")
        .style("top", (d3.event.clientY) + "px");  // Value of the text
        // debugger;

        // Highlight circle on map for selected data point
        d3.selectAll('.bubble')
                .selectAll('circle')
                .transition()
                .ease('linear')
                .duration('250')
                .attr('fill-opacity', function(elem) {
                    // debugger;
                    if (d.airport == elem.key) {
                        return 1;
                    }
                    else {
                        return 0.1;
                    };
                })
                .attr('stroke-opacity', function(elem) {
                    if (d.airport == elem.key) {
                        return 1;
                    }
                    else {
                        return 0.1;
                    }
                });
    }

    function handleMouseOutChart(d, i) {
        // Remove tooltips and drop lines from chart
        var d3Chart = d3.select('#plot-line svg');
        d3Chart.selectAll('.d3-dp-line').remove();
        this.setAttribute('r', this.getAttribute('r')/1.5)

        // Select text by id and then remove
        d3.select("#map_tooltip").remove();  // Remove text location

        // Reset circles on map
        d3.selectAll('.bubble')
                .selectAll('circle')
                .transition()
                .ease('linear')
                .duration('250')
                .attr('fill-opacity', 1)
                .attr('stroke-opacity', 1);
    }

    // Creating map
    var projection = d3.geo.albersUsa()
                            .scale(map_width-map_margin)
                            .translate([map_width/2-map_margin/2, map_height/2-map_margin/2]);
    var path = d3.geo.path().projection(projection);
    var map = svg_map.selectAll('path')
                  .data(data.features)
                  .enter()
                  .append('path')
                  .attr('d', path)
                  .style('fill', 'rgb(200,200,170)')
                  .style('stroke', 'black')
                  .style('stroke-width', 1)
                  .on('click',handleMouseClick);



    function plot_points_chart(data) {

        // Function for aggregating airport names based on airline selection
        
        // Key data by carrier and airport
        var nested_map = d3.nest()
                      .key(function(d) {
                        return d['carrier'];
                      })
                      .key(function(d) {
                        return d['airport'];
                      })
                      .rollup(function(leaves) {
                        var coords = leaves.map(function(d) {
                            // Modify longitude for plotting on map to avoid JFK/LGA overlap
                            if (d.airport == 'JFK') {
                                d.long = +d.long + 0.5;
                            }
                            else if (d.airport == 'LGA') {
                                d.long = +d.long - 0.5;
                            }
                            
                          return projection([+d.long, +d.lat]);
                        })
                        return {
                          'airport' : leaves[0].airport,
                          'airport_name' : leaves[0].airport_name,
                          'carrier_name' : leaves[0].carrier_name,
                          'x' : coords[0][0],
                          'y' : coords[0][1]
                        };

                      })
                      .entries(data);

        function update_map(carrier, airports) {
            // Draw circles for selected carrier on map
            var carriers = d3.set();
            for (var i = 0; i < nested_map.length; i++) {
                carriers.add(nested_map[i].key);
            }
            carriers = carriers.values()
            var nested_filt = nested_map.filter(function(d) { return d['key'] === carrier})[0];

            document.getElementById('active-carrier').innerHTML = 
                        'For ' + nested_filt.values[0].values.carrier_name + ' Hubs';

            var color = d3.scale.category10()

            svg_map.selectAll('circle').data(data, function(d) {return d['key'];}).exit().remove();
            var circles = svg_map.selectAll('circle').data(nested_filt.values, function(d) {return d['key'];})

            svg_map.append('g')
              .attr('class','bubble')
              .selectAll('circle')
              .data(nested_filt.values)
              .enter()
              .append('circle')
              .attr('cx', function(d) { return d.values['x']; })
              .attr('cy', function(d) { return d.values['y']; })
              .attr('id', function(d) { return d.key;})
              .attr('fill', function(d, i) { return color(d.key); })
              .attr('r', 7)
              .on('mouseover', handleMouseOver)
              .on('mouseout', handleMouseOut)
              .on('click', handleMouseClick);
        };    

        function initAxis() {
            // Initialize chart axis
            var x1 = new Date("2003").getFullYear()+1;
            var x2 = new Date("2003").getFullYear()+1;
            var x = d3.time.scale()
                                .range([ch_margin, ch_width-ch_margin])
                                .domain([x1, x2]),
                y = d3.scale.linear()
                                .range([ch_height-ch_margin, ch_margin])
                                .domain([0,1]),
                xAxis = d3.svg.axis().scale(x).orient('bottom').tickFormat(d3.time.format('%Y')),
                yAxis = d3.svg.axis().scale(y).orient('left');

            d3.select('.chart')
              .append('g')
              .attr('class', 'x axis')
              .attr('transform', 'translate(0,' + (ch_height-ch_margin) + ')')
              .attr('y', ch_height-ch_margin)
              .call(xAxis);

            d3.select('.chart')
              .append('g')
              .attr('class', 'y axis')
              .attr('transform', 'translate(' + ch_margin + ',0)')
              .attr('x', ch_margin)
              .call(yAxis);

            d3.select('.chart').append('text').attr('text-anchor', 'middle')
                              .attr('transform', 'translate(' + (ch_width/2) + ',' + (ch_height) + ')')
                              .text('YEAR')
        }

        initAxis();

        function agg_year(leaves) {
            var arr_flights_sum = d3.sum(leaves, function(d) {
                return d['arr_flights'];
            });
            var arr_del15_sum = d3.sum(leaves, function(d) {
                return d['arr_del15'];
            });
            var arr_cancelled_sum = d3.sum(leaves, function(d) {
                return d['arr_cancelled'];
            });
            var carrier_delay_sum = d3.sum(leaves, function(d) {
                return d['carrier_ct'];
            });
            var weather_delay_sum = d3.sum(leaves, function(d) {
                return d[' weather_ct'];
            });
            var nas_delay_sum = d3.sum(leaves, function(d) {
                return d['nas_ct'];
            });
            var security_delay_sum = d3.sum(leaves, function(d) {
                return d['security_ct'];
            });
            var late_aircraft_delay_sum = d3.sum(leaves, function(d) {
                return d['late_aircraft_ct'];
            });

            if (arr_flights_sum == 0) {
                arr_del15_pct = 0;
                arr_cancelled_pct = 0;
                carrier_delay_pct = 0;
                weather_delay_pct = 0;
                nas_delay_pct =0;
                security_delay_pct = 0;
                late_aircraft_delay_pct = 0;
            }
            else {
                arr_del15_pct = arr_del15_sum / arr_flights_sum * 100;
                arr_cancelled_pct = arr_cancelled_sum / arr_flights_sum * 100;
                carrier_delay_pct = carrier_delay_sum / arr_del15_sum * 100;
                weather_delay_pct = weather_delay_sum / arr_del15_sum * 100;
                nas_delay_pct =nas_delay_sum / arr_del15_sum * 100;
                security_delay_pct = security_delay_sum / arr_del15_sum * 100;
                late_aircraft_delay_pct = late_aircraft_delay_sum / arr_del15_sum * 100;
            }

            return {
                'airport' : leaves[0].airport,
                'airport_name' : leaves[0].airport_name,
                'carrier' : leaves[0].carrier,
                'carrier_name' : leaves[0].carrier_name,
                'year' : leaves[0].year,
                'arr_flights_sum' : arr_flights_sum,
                'arr_del15_sum' : arr_del15_sum,
                'arr_del15_pct' : arr_del15_pct,
                'arr_cancelled_sum' : arr_cancelled_sum,
                'arr_cancelled_pct' : arr_cancelled_pct,
                'carrier_delay_sum' : carrier_delay_sum,
                'carrier_delay_pct' : carrier_delay_pct,
                'weather_delay_sum' : weather_delay_sum,
                'weather_delay_pct' : weather_delay_pct,
                'nas_delay_sum' : nas_delay_sum,
                'nas_delay_pct' : nas_delay_pct,
                'security_delay_sum' : security_delay_sum,
                'security_delay_pct' : security_delay_pct,
                'late_aircraft_delay_sum' : late_aircraft_delay_sum,
                'late_aircraft_delay_pct' : late_aircraft_delay_pct
            };
        }

        function update_chart(carrier, metric, airports) {
            // Draw circles and paths for selected carrier and metric on map
            var metric_options = {
                'arr_del15_pct' : 'All Flight Delays',
                'arr_cancelled_pct' : 'Flights Cancelled',
                'carrier_delay_pct' : 'Carrier Delays',
                'late_aircraft_delay_pct' : 'Late Aircraft Delays',
                'nas_delay_pct' : 'NAS Delays',
                'security_delay_pct' : 'Security Delays',
                'weather_delay_pct' : 'Weather Delays',
                'arr_flights_sum' : 'Total Flights'
            };

            // Key data by carrier, airport, and year for plotting
            var nested_chart = d3.nest()
                        .key(function(d) {
                            return d['carrier'];
                        })
                        .key(function(d) {
                            return d['airport'];
                        })
                        .key(function(d) {
                            return d['year'];
                        })
                        .rollup(agg_year)
                        .entries(data);

            // Filter nested data by selected carrier
            nested_filt = nested_chart.filter(function(d) {
                return d['key'] == carrier;
            })[0]

            var all_x = []
            var all_y = []
            nested_filt.values.forEach(function(item) {
                item.values.forEach(function(item2) {
                    all_x = all_x.concat(item2.key);
                    all_y = all_y.concat(item2.values[metric])
                });
            });

            // Set time scale (x axis) for selected carrier and metric
            var time_extent = d3.extent(all_x)
            time_extent[0] = new Date(time_extent[0]).getFullYear()+1;
            time_extent[1] = new Date(time_extent[1]).getFullYear()+1;
            var time_scale = d3.time.scale()
                                    .range([ch_margin, ch_width-ch_margin])
                                    .domain(time_extent);
            var time_axis = d3.svg.axis()
                                  .scale(time_scale)
                                  .orient('bottom')
                                  .ticks(time_extent[1]-time_extent[0]+1)
                                  .innerTickSize(-(ch_height-2*ch_margin))
                                  .outerTickSize(0)
                                  .tickPadding(5)
                                  .tickFormat(d3.format('04d'));
            
            // Set delay scale (y axis) for selected carrier and metric
            var delay_extent = d3.extent(all_y)
            delay_extent[0] = 0;
            delay_extent[1] = delay_extent[1]*1.1;
            var delay_scale = d3.scale.linear()
                                .range([ch_height-ch_margin, ch_margin])
                                .domain(delay_extent);
            var delay_axis = d3.svg.axis()
                               .scale(delay_scale)
                               .orient('left')
                               .ticks(6)
                               .innerTickSize(-(ch_width-2*ch_margin))
                               .outerTickSize(5)
                               .tickPadding(15);

            // Animate change in x and y axes when changing metric or carrier
            d3.select('.chart').transition().duration(1000).selectAll('g.x.axis').call(time_axis);
            d3.select('.chart').transition().duration(1500).selectAll('g.y.axis').call(delay_axis);

            // Rotate time axis labels
            d3.select('.chart').selectAll('.x.axis text').attr('transform', function(d) {
                // debugger;
                return 'translate(' + (this.getBBox().height*-1 + 10) + ',' + (this.getBBox().height-5)  + ')rotate(-30)';
            });

            // Map values from filtered nested data
            data_plot = nested_filt.values.map(function(d) {
                return {
                    key: d.key,
                    points: d.values.map(function(l, i) {
                        return {
                            x: l.key,
                            y: l.values[metric],
                            carrier: l.values['carrier'],
                            airport: l.values['airport'],
                            airport_name: l.values['airport_name'],
                            metric_name: metric
                        };
                    })
                };
            });

            // Add '%' to y labels if metric is percentage value
            if (delay_extent[1] < 100) {
                d3.select('.y.axis').selectAll('.tick').select('text').html(function(d) {
                    return d + '%';
                });
            }

            // Remove circles and paths from chart
            d3.select('.chart').selectAll('.scatterPlotGroup').data(data, function(d){return d['key'];}).exit().remove()
            d3.select('.chart').selectAll('path').data(data, function(d){return d['key'];}).exit().remove()
            
            // Create plot groups for circles (id by airport)
            var circleGroups = d3.select('.chart').selectAll('.scatterPlotGroup')
                                 .data(data_plot)
                                 .enter()
                                 .append('g')
                                 .attr('class', 'scatterPlotGroup')
                                 .attr('id', function(d) {
                                    return d.key;
                                 });

            // Draw and animate paths
            var valueline = d3.svg.line()
                .x(function(d) {
                    return time_scale(d['x']);
                })
                .y(function(d) {
                    return delay_scale(d['y']);
                });

            var path = d3.select('.chart').selectAll('.scatterPlotGroup')
                .data(data_plot)
                .append('path')
                .attr('class', 'line')
                .attr('d', valueline)
                .attr('d', function(d) {return valueline(d.points);})
                .style('fill','none')
                .style('stroke', function(d) {
                    return document.getElementById('plot-map')
                                    .getElementById(d.key)
                                    .getAttribute('fill');
                })
                .style('stroke-width','3px');

            path.attr('stroke-dasharray', function(d, i) {
                    return path[0][i].getTotalLength() + " " + path[0][i].getTotalLength();
                })
                .attr('stroke-dashoffset', function(d, i) {
                    return path[0][i].getTotalLength();
                })
                .transition()
                .duration(1000)
                .ease('linear')
                .attr('stroke-dashoffset', 0);
            
            // Draw and animate circles
            var circles = circleGroups.selectAll('circle')
                .data(function(d) {
                return d.points;
                })
                .enter()
                .append('circle')
                .on('mouseover', handleMouseOverChart)
                .on('mouseout', handleMouseOutChart)
                .on('click', handleMouseClick);
            
            circles.transition()
                    .delay(1000)
                    .ease('linear')
                    .duration(500)
                    .attr('cx', function(d) {
                        return time_scale(d['x']);
                    })
                    .attr('cy', function(d) {
                        return delay_scale(d['y']);
                    })
                    .attr('fill',function(d, i) {
                        var airport_cur = d['airport'];
                        // debugger;
                        return document.getElementById('plot-map')
                                        .getElementById(airport_cur)
                                        .getAttribute('fill')
                    })
                    .attr('r',5);

            // Update HTML text for active years (under page title)
            document.getElementById('active-years').innerHTML = 
                    'Years ' + time_extent[0] + ' to ' + time_extent[1];

            // Update chart title
            if (metric == "arr_del15_pct") {
                chart_title = "Flights Delayed (Percentage of All Scheduled Arrivals)";
            }
            else if (metric == "arr_cancelled_pct") {
                chart_title = "Flights Cancelled (Percentage of All Scheduled Arrivals)"
            }
            else if (metric == "arr_flights_sum") {
                chart_title = "Total Number of Scheduled Arrivals (By Year)";
            }
            else {
                chart_title = metric_options[metric] + " (Percentage of All Flight Delays)";
            }
            document.getElementById('active-metric').innerHTML = 
                    chart_title;


            // Update chart sub-title
            document.getElementById('active-hubs').innerHTML = 
                    'For ' + nested_filt.values[0].values[0].values.carrier_name + ' Hubs';

            if (airports != undefined && airports[0] != undefined) {
                d3.selectAll('.scatterPlotGroup')
                    .selectAll('path')
                    .style('stroke-opacity', function(d) {
                        if (!airports.includes(d.key)) {
                            return 0.05;
                        }
                        else {
                            return 0.95;
                        };
                    })
                d3.selectAll('.scatterPlotGroup')
                    .selectAll('circle')
                    .style('visibility', function(d) {
                        if (!airports.includes(d.airport)) {
                            return 'hidden';
                        }
                        else {
                            return 'visible';
                        }
                    })
            }

        }

        // Change button classes to show selected carrier and metric
        carrier_data = [];
        for (var key in carrier_options) {
            carrier_data.push(key);
        }

        var carrier_buttons = d3.select('.stats-map')
                                .append('div')
                                .attr('class', 'carrier_buttons')
                                .selectAll('div')
                                .data(carrier_data)
                                .enter()
                                .append('button')
                                .attr('class', function(d, i) {
                                    if (i === 0)
                                        return 'btn-link btn-block';
                                    else
                                        return 'btn-primary btn-block';
                                })
                                .attr('id', function(d) {
                                    return d;
                                })
                                .style('display', 'none')
                                .text(function(d, i) {
                                    return d;
                                });

        for (var i = 0; i < carrier_buttons[0].length; i++) {
            carrier_buttons[0][i].innerHTML = carrier_options[carrier_buttons[0][i].id];
        }

        carrier_buttons.on('click', function(d) {
            d3.select('.carrier_buttons')
                .selectAll('button')
                // .transition()
                // .duration(500)
                .classed('btn-link', false)
                .classed('btn-primary', true);
            d3.select(this)
                .classed('btn-link', true);
            update_map(d);
            cur_metric = document.getElementsByClassName('btn-link')[1].id;
            update_chart(d, cur_metric);
        })

        metric_data = [];
        for (var key in metric_options) {
            metric_data.push(key);
        }
        
        var metric_buttons = d3.select('.stats-line')
                        .append('div')
                        .attr('class', 'metric_buttons')
                        .selectAll('div')
                        .data(metric_data)
                        .enter()
                        .append('button')
                        .attr('class', function(d, i) {
                            if (i == 0)
                                return 'btn-link';
                            else
                                return 'btn-primary';
                        })
                        .attr('id', function(d) {
                            return d;
                        })
                        .style('display','none')
                        .text(function(d, i) {
                            return d;
                        });
        
        for (var i = 0; i < metric_buttons[0].length; i++) {
            metric_buttons[0][i].innerHTML = metric_options[metric_buttons[0][i].id];
        }

        metric_buttons.on('click', function(d) {
            d3.select('.metric_buttons')
                .selectAll('button')
                .classed('btn-link', false)
                .classed('btn-primary', true);
            d3.select(this)
                .classed('btn-link', true);
            var cur_carrier = document.getElementsByClassName('btn-link')[0].id;
            update_chart(cur_carrier, d);
        })

        
        // Show case study for Delta/Northwest Merger to start
        var pagination = d3.select('.pagination')
                           .selectAll('li a')
                           .on('click', function(d, i) {
                                var story_name = this.parentElement.parentElement.classList[0];
                                var page = this.id;
                                var page_num = i;
                                if (page == 'page-end') {
                                    // Go to free exploration
                                    d3.select('#story-container').remove()
                                    document.getElementById('active-years').innerHTML = 'Explore the Data!'
                                    // update_map('AA')
                                    // update_chart('AA','arr_del15_pct')
                                    d3.select('.metric_buttons')
                                      .selectAll('button')
                                      .style('display', 'initial')
                                    d3.select('.carrier_buttons')
                                      .selectAll('button')
                                      .style('display', 'initial')
                                }
                                else if (story_name == 'delta_northwest_merger') {
                                    // Page 1: Show Northwest Data (arr_flights_sum for NW)
                                    if (i == 0) {
                                        document.getElementById('NW').click()
                                        document.getElementById('arr_flights_sum').click()
                                        update_map('NW')
                                        update_chart('NW', 'arr_flights_sum', ['MSP','DTW','MEM'])
                                        document.getElementById('active-years').innerHTML = 
                                            'Case Study: The Delta / Northwest Airlines Merger'
                                        document.getElementById('story-description').innerHTML = 
                                            'On April 15, 2008, a merger agreement was announced between Northwest \
                                            and Delta Airlines. Operating certificates were merged between the two airlines \
                                            by the end of 2009, and in 2010 Northwest ceased to exist as an independent carrier.'
                                    }
                                    else if (i == 1) {
                                        document.getElementById('DL').click()
                                        update_map('DL')
                                        update_chart('DL', 'arr_flights_sum', ['MSP','DTW','MEM'])
                                        document.getElementById('active-years').innerHTML = 
                                            'Case Study: The Delta / Northwest Airlines Merger'
                                        document.getElementById('story-description').innerHTML = 
                                            "In 2010, as a result of the merger, Delta airlines acquired new hubs in Detroit, MI (DTW), \
                                            Minneapolis, MN (MSP), and Memphis, TN (MEM). Minneapolis and Detroit are now Delta's second \
                                            and third largest hubs by total flights, respectively, and Detroit also serves as Delta's Asian gateway \
                                            for the northeastern United States. Hub status for Memphis was removed in 2013 after several rounds of budget cuts."
                                    }
                                    else if (i == 2) {
                                        document.getElementById('DL').click()
                                        document.getElementById('carrier_delay_pct').click()
                                        update_map('DL')
                                        update_chart('DL', 'carrier_delay_pct', ['MSP', 'DTW', 'MEM'])
                                        document.getElementById('active-years').innerHTML = 
                                            'Case Study: The Delta / Northwest Airlines Merger'
                                        document.getElementById('story-description').innerHTML = 
                                            "The same year that the merger was put into action (2010), there was a spike in the percentage \
                                            of flight delays that were a result of circumstances within the airline's control. \
                                            This jump was observed for MSP and MEM, as well as other hubs that were not formerly hubs for Northwest. \
                                            However, this trend was not observed for DTW, which showed an improvement in this metric."
                                    }
                                    else if (i == 3) {
                                        document.getElementById('DL').click()
                                        document.getElementById('late_aircraft_delay_pct').click()
                                        update_map('DL')
                                        update_chart('DL', 'late_aircraft_delay_pct', ['MSP','DTW', 'MEM'])
                                        document.getElementById('active-years').innerHTML = 
                                            'Case Study: The Delta / Northwest Airlines Merger'
                                        document.getElementById('story-description').innerHTML = 
                                            "There was a similar increase in delays that were attributed to aircraft operating behind schedule over \
                                            multiple consecutive flights. This trend was observed at all three former Northwest hubs, but were most \
                                            apparent for MSP and DTW flight arrivals."
                                    }
                                    else if (i == 4) {
                                        document.getElementById('US').click()
                                        document.getElementById('arr_flights_sum').click()
                                        document.getElementById('active-years').innerHTML = 
                                            'Additional Exploration (American/US Airways & Frontier/Midwest Airlines Mergers'
                                        document.getElementById('story-description').innerHTML = 
                                            "This visualization shows flight delay data for 10 major US airlines at their hub airports. There are \
                                            two other mergers that can be explored further in this dataset. US Airways (shown) merged with \
                                            American Airlines by the end of 2015. Frontier Airlines merged with Midwest Airlines (not included) \
                                            by late 2011, resulting in Frontier beginning operation in CLE, CVG, and ORD in 2012."
                                    }
                                    // Page 2: Show Delta Acquisition for Northwest Hubs (arr_flights_sum for DL at NW hubs)
                                    // Page 3: Show Carrier Delays for Northwest Hubs (carrier_delay_pct for DL at NW hubs)
                                    // Page 4: Show Late Aircraft Delays for Northwest Hubs (late_aircraft_delay_pct for DL at NW hubs)
                                }

                           })
        
        // Initialize Story
        document.getElementById('page-1').click()
        
    };

    d3.csv('airline_delay_loc.csv', plot_points_chart);
};