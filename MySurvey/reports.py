from report_tools.reports import Report
from report_tools.chart_data import ChartData
from report_tools.renderers.googlecharts import GoogleChartsRenderer
from report_tools import charts


class MyReport(Report):
    renderer = GoogleChartsRenderer
    
    pie_chart = charts.PieChart(
            title="A nice, simple pie chart",
            width=400,
            height=300
            )
    multiseries_line_chart = charts.LineChart(title="Pony Populations - 2009-2012", width="500")
    
    def get_data_for_pie_chart(self):
        data = ChartData()
                    
        data.add_column("Pony Type")
        data.add_column("Population")
                            
        data.add_row(["Blue", 20])
        data.add_row(["Pink", 20])
        data.add_row(["Magical", 1])
                                        
        return data

    def get_data_for_multiseries_line_chart(self):
        data = ChartData()
        
        data.add_column("Test Period")
        data.add_column("Blue Pony Population")
        data.add_column("Pink Pony Population")
        data.add_column("Magical Pony Population")
        
        data.add_row(["2009-10", 20, 10, 50])
        data.add_row(["2010-11", 18, 8, 60])
        data.add_row(["2011-12", 100, 120, 2])
        
        return data
