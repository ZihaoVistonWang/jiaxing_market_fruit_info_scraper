# Jiaxing Market Fruit Info Scraper

This repository contains a web scraper designed to extract the average prices of domestic and imported fruits from the Jiaxing market. The scraper targets the website (<http://jxzgsgzs.com/price.html>), where it retrieves and processes the relevant pricing data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ZihaoVistonWang/jiaxing_market_fruit_info_scraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd jiaxing_market_fruit_info_scraper
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scraper using the following command:

```bash
python main.py
```

## Output

The script will save the scraped fruit information data to `domestic_fruit_info.csv` with the following columns (if available):

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
