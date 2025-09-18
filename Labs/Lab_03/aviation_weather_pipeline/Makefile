.PHONY: all fetch analyze clean

# Default target
all: analyze

fetch:
	@echo ">>> Starting fetching METAR data..."
	./fetch_metars.sh
	@echo ">>> Finished fetching METAR data. Data saved in raw_metars/"

analyze: fetch
	@echo ">>> Starting analyzing METAR data..."
	analyze_data.sh
	@echo ">>> Finished analyzing. Results written to weather_report.csv"

clean:
	@echo ">>> Cleaning up generated files..."
	rm -rf raw_metars/ weather_report.csv
	@echo ">>> Cleanup complete."


