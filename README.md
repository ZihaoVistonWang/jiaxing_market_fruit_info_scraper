# Jiaxing Market Fruit Info Scraper

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Project Description

This repository contains a web scraper designed to extract the average prices of domestic and imported fruits from the Jiaxing market. The scraper targets the website [Jiaxing Fruit Market](http://jxzgsgzs.com/price.html) to retrieve and process relevant pricing data.

## Key Features

- Scrapes both domestic and imported fruit data
- Automatic pagination handling
- Built-in request retry mechanism
- Data saved in CSV format
- Supports custom date range scraping

## Usage

1. Setup environment

   ```bash
   # Clone repository
   git clone https://github.com/your_username/jiaxing_market_fruit_info_scraper.git
   cd jiaxing_market_fruit_info_scraper

   # Install dependencies
   pip install -r requirements.txt
   ```

2. Run the scraper

   ```python
   # Default: scrapes data from 2018-01-01 to 2018-01-05
   python main.py
   ```

## Data Output

The scraper generates two CSV files:

1. `domestic_fruit_info.csv` - Contains domestic fruit data
2. `imported_fruit_info.csv` - Contains imported fruit data

Both files have the same columns (if available):

- id
- stageId
- structId
- price
- totalSalesVolume
- totalTurnover
- category
- kind
- placeOfOrigin
- city
- specification
- date

If any errors occur during execution, please check the `log.log` file for detailed error messages.

## Dependencies

- Python 3.10
- pandas==2.2.1
- DataRecorder==3.4.12
- DrissionPage==4.1.0.12
- loguru==0.7.3
- tqdm==4.66.2

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
