import warnings

import billboard
import csv
from vars import BILLBOARD_YEAR_SERIES

CHART_TITLES = billboard.charts(year_end=True)
filename = f'data/billboard/year_end.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerow(["chart", "year", "rank", "title", "artist", "image"])
    for chart_title in CHART_TITLES:
        for year in BILLBOARD_YEAR_SERIES:
            try:
                with warnings.catch_warnings(record=True) as w:
                    chart = billboard.ChartData(chart_title, year=year)
                    if len(w) > 0 and issubclass(w[-1].category, billboard.UnsupportedYearWarning):
                        continue
                    for entry in chart.entries:
                        entry: billboard.YearEndChartEntry
                        writer.writerow([chart_title, year, entry.rank, entry.title, entry.artist, entry.image])
                    print(f"Done year {year} chart {chart_title}")
            except billboard.BillboardNotFoundException:
                pass
    print(f"Done writing {filename}")
