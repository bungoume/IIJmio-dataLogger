
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
          'columns': [0, 4]
        },
        // 1 day in milliseconds = 24 * 60 * 60 * 1000 = 86,400,000
        'minRangeSize': 86400000
        }
      },
      // Initial range: 2012-02-09 to 2012-03-20.
      //'state': {'range': {'start': new Date(2012, 1, 9), 'end': new Date(2012, 2, 20)}}
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
         //{
         //  'calc': function(dataTable, rowIndex) {
         //    return dataTable.getFormattedValue(rowIndex, 0);
         //  },
         //  'type': 'string'
         //}
         0, 1, 2, 3, 4]
     }
    });

    dashboard.bind(control, chart);
    _drawChart();
  }

  function _drawChart() {
    //var data = _getData();
    //var dataTable = google.visualization.arrayToDataTable(data);
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Topping');
    data.addColumn('number', 'Slices');
    data.addColumn('number', 'hoge');
    data.addColumn('number', 'foo');
    data.addColumn('number', 'bar');
    data.addRows([
      [1, 5,3,9,15],
      [2, 4,4,11,12],
      [3, 3,5,13,9],
      [4, 2,6,15,6],
      [5, 2,6,15,6],
      [6, 2,6,15,6],
      [7, 2,6,15,6],
      [8, 2,6,15,6],
      [9, 2,6,15,6],
      [10, 2,6,15,6],
      [11, 2,6,15,6],
      [12, 2,6,15,6],
      [13, 2,6,15,6],
      [14, 2,6,15,6],
      [15, 2,6,15,6],
      [16, 2,6,15,6],
      [17, 2,6,15,6],
      [18, 2,6,15,6],
      [19, 2,6,15,6],
      [20, 2,6,15,6],
      [21, 2,6,15,6],
      [22, 2,6,15,6],
      [23, 2,6,15,6],
      [24, 2,6,15,6],
      [25, 2,6,15,6],
      [26, 2,6,15,6],
      [27, 2,6,15,6],
      [28, 2,6,15,6],
      [29, 2,6,15,6],
      [30, 2,6,15,6],
      [31, 2,6,15,6],
      [32, 2,6,15,6],
      [33, 2,6,15,6],
      [34, 2,6,15,6],
      [35, 2,6,15,6],
      [36, 2,6,15,6],
      [37, 2,6,15,6],
      [38, 2,6,15,6],
      [39, 2,6,15,6],
      [40, 2,6,15,6],
      [41, 2,6,15,6],
      [42, 2,6,15,6],
      [43, 2,6,15,6],
      [44, 2,6,15,6],
      [45, 2,6,15,6],
      [46, 2,6,15,6],
      [47, 1,7,17,3]
    ]);
    dashboard.draw(data);
  }

  function _getData(){
    var data = [];
    data.push(['収入',　'実質手取', '税額', '保険料']);
    //data.push([income, income-totalTax-insuranceTax, totalTax, insuranceTax]);
    return data;
  }

  function update(){}

  return {
    init: init,
    update: update,
  };
})();

Graph.init();

