
var Graph = (function() {
  var dashboard;
  var chartElement;

  function init(){
    google.load('visualization', '1.1', {packages:['corechart', 'controls']});
    chartElement = document.getElementById('dashboard_div');
    google.setOnLoadCallback(_callback);
  }

  function _callback(){
    dashboard = new google.visualization.Dashboard(chartElement);

    var control = new google.visualization.ControlWrapper({
      'controlType': 'ChartRangeFilter',
      'containerId': 'control_div',
      'options': {
        // Filter by the date axis.
        'filterColumnIndex': 0,
        'ui': {
          'chartType': 'LineChart',
          'chartOptions': {
            'chartArea': {'height': '30%', 'width': '90%'},
            'hAxis': {'baselineColor': 'none'}
          },
          // Display a single series that shows the closing value of the stock.
          // Thus, this view has two columns: the date (axis) and the stock value (line series).
          'chartView': {
            'columns': [0, 3]
          },
          // 1 day in milliseconds = 24 * 60 * 60 * 1000 = 86,400,000
          'minRangeSize': 86400000
        }
      },
      // Initial range: 2012-02-09 to 2012-03-20.
      //'state': {'range': {'start': new Date(2012, 1, 9), 'end': new Date(2013, 1, 20)}}
    });

    var chart = new google.visualization.ChartWrapper({
      'chartType': 'LineChart',
      'containerId': 'chart_div',
      'options': {
        // Use the same chart area width as the control for axis alignment.
        'chartArea': {'height': '80%', 'width': '90%'},
        'hAxis': {'slantedText': false},
        'vAxis': {'viewWindow': {'min': 0, 'max': 20}},
        'legend': {'position': 'none'}
      },
      // Convert the first column from 'date' to 'string'.
      'view': {
        'columns': [
          {
            'calc': function(dataTable, rowIndex) {
              return dataTable.getFormattedValue(rowIndex, 0);
            },
            'type': 'string'
          }, 1, 2, 3]
      }
    });

    dashboard.bind(control, chart);
    $.getJSON('/list_log',   _drawChart);
  }

  function _drawChart(json) {
    //var data = _getData();
    var data = [];
    var iccidList = ["datetime"];
    for (var i in json.data){
      var d = new Date();
      d.setTime(Number(i))
      var temp = [Number(i)];
      for (var j in json.data[i]){
        var num = _.indexOf(iccidList,j);
        if(num === -1){
          iccidList.push(j);
          num = _.indexOf(iccidList,j);
        }
        temp[num] = json.data[i][j];
      }
      data.push(temp);
    }
    data.unshift(iccidList);

    var dataTable = google.visualization.arrayToDataTable(data);
    dashboard.draw(dataTable);
  }

  function update(){}

  return {
    init: init,
    update: update,
  };
})();

Graph.init();

