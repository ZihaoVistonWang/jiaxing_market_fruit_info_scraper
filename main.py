import time
import pandas as pd
from DataRecorder import Recorder
from DrissionPage import SessionPage
from loguru import logger
from tqdm.rich import tqdm

logger.add("log.log", rotation="10 MB", level="INFO")


def get_date_id(
    date: str
) -> str:
    """Get date_id from the website.

    Args:
        date (str): The date to get date_id.

    Returns:
        str: The date_id.
    """
    # API endpoint for getting date_id
    url = "http://jxzgsgzs.com/jia-xing-fruit-webapi/stage"

    # API request parameters
    params = {
        "reportCycle": "10",  # Report cycle duration
        "rawDataIsPublish": "true",  # Only get published data
        "pageSize": "1",  # Get only one record
        "orderBy": "-reportTimeStart",  # Order by report time descending
        "reportTimeStart": date,  # Target date
    }

    try_times = 0  # Initialize retry counter
    session = SessionPage()  # Create new session

    # Retry loop for API requests
    while True:
        # Make API request
        session.get(url=url, params=params)
        json_data = session.json  # Get JSON response

        # Check if request was successful
        if json_data["success"] == 1:
            break  # Exit loop on success
        else:
            try_times += 1
            # Log warning and wait before retrying
            logger.warning(f"Request failed. Attempt {try_times} for domestic fruit data in date '{date}' when we get 'date_id'. Waiting for 5 seconds before retrying.")
            time.sleep(5)
            # If failed 3 times, wait longer
            if try_times >= 3:
                logger.error(f"Failed 3 times for domestic fruit data in date '{date}' when we get 'date_id'. Waiting for 5 minutes before retrying.")
                try_times = 0
                time.sleep(60 * 5)

    # Return the date_id from the first record
    return json_data["data"][0]["id"]

def scrape_domestic_fruit_data(
    date: str,
    date_id: str,
) -> list[dict]:
    """Get domestic fruit data from the website.

    Args:
        date (str): The date.
        date_id (str): The id of date.

    Returns:
        list[dict]: The domestic fruit data.
    """
    data_list = []  # Initialize list to store all data

    # Loop through pages (max 100 pages to prevent infinite loops)
    for pageNo in range(1, 100):
        # API endpoint for domestic fruit data
        url = "http://jxzgsgzs.com/jia-xing-fruit-webapi/rawDataExpansion"

        # API request parameters
        params = {
            "stageId": f"{date_id}",  # Date identifier
            "orderBy": "-struct.sortNum,category,kind,placeOfOrigin,city",  # Sorting order
            "parentStructId": "1",  # Parent structure ID
            "pageNo": f"{pageNo}",  # Current page number
            "pageSize": "1000",  # Number of records per page
        }

        # Create new session and make API request
        session = SessionPage()
        session.get(url=url, params=params)
        json_data = session.json  # Get JSON response

        # Retry loop for failed requests
        while True:
            if json_data["success"] == 1:
                break  # Exit loop on success
            else:
                try_times += 1
                # Log warning and wait before retrying
                logger.warning(f"Request failed. Attempt {try_times} for domestic fruit data in date '{date}' when we get 'data'. Waiting for 5 seconds before retrying.")
                time.sleep(5)
                # If failed 3 times, wait longer
                if try_times >= 3:
                    logger.error(f"Failed 3 times for domestic fruit data in date '{date}' when we get 'data'. Waiting for 5 minutes before retrying.")
                    try_times = 0
                    time.sleep(60 * 5)

        # Add current page data to list
        data = json_data["data"]
        data_list += data

        # Check if we've reached the last page
        if json_data["total"] <= 1000:
            break

    # Add date field to each record
    for data in data_list:
        data["date"] = date

    return data_list

def scrape_imported_fruit_data(
    date: str,
    date_id: str,
) -> list[dict]:
    """Get imported fruit data from the website.

    Args:
        date (str): The date.
        date_id (str): The id of date.

    Returns:
        list[dict]: The imported fruit data.
    """
    data_list = []  # Initialize list to store all data

    # Loop through pages (max 100 pages to prevent infinite loops)
    for pageNo in range(1, 100):
        # API endpoint for imported fruit data
        url = "http://jxzgsgzs.com/jia-xing-fruit-webapi/importRawDataExpansion"

        # API request parameters
        params = {
            "stageId": f"{date_id}",  # Date identifier
            "orderBy": "-struct.sortNum,category,kind,placeOfOrigin,city",  # Sorting order
            "parentStructId": "1",  # Parent structure ID
            "pageNo": f"{pageNo}",  # Current page number
            "pageSize": "1000",  # Number of records per page
        }

        # Create new session and make API request
        session = SessionPage()
        session.get(url=url, params=params)
        json_data = session.json  # Get JSON response

        # Retry loop for failed requests
        while True:
            if json_data["success"] == 1:
                break  # Exit loop on success
            else:
                try_times += 1
                # Log warning and wait before retrying
                logger.warning(f"Request failed. Attempt {try_times} for imported fruit data in date '{date}'. Waiting for 5 seconds before retrying.")
                time.sleep(5)
                # If failed 3 times, wait longer
                if try_times >= 3:
                    logger.error(f"Failed 3 times for imported fruit data in date '{date}'. Waiting for 5 minutes before retrying.")
                    try_times = 0
                    time.sleep(60 * 5)

        # Add current page data to list
        data = json_data["data"]
        data_list += data

        # Check if we've reached the last page
        if json_data["total"] <= 1000:
            break

    # Add date field to each record
    for data in data_list:
        data["date"] = date

    return data_list

def main(
    date_end: str,
    date_start: str = "2018-01-01",
):
    """Main function to scrape data from the website.

    Args:
        date_end (str): The end date.
        date_start (str, optional): The start date. Defaults to "2018-01-01".
    """
    # Initialize data recorders for domestic and imported fruit data
    domestic_fruit_recorder = Recorder("domestic_fruit_info.csv")  # Recorder for domestic fruit data
    imported_fruit_recorder = Recorder("imported_fruit_info.csv")  # Recorder for imported fruit data

    # Configure domestic fruit recorder settings
    domestic_fruit_recorder.set.cache_size(10000)  # Set cache size to 10,000 records
    domestic_fruit_recorder.set.show_msg(False)    # Disable console messages
    domestic_fruit_recorder.set.encoding("utf-8-sig")  # Set encoding to UTF-8 with BOM

    # Configure imported fruit recorder settings
    imported_fruit_recorder.set.cache_size(10000)  # Set cache size to 10,000 records
    imported_fruit_recorder.set.show_msg(False)    # Disable console messages
    imported_fruit_recorder.set.encoding("utf-8-sig")  # Set encoding to UTF-8 with BOM

    # Generate date range from start to end date
    date_list = pd.date_range(start=date_start, end=date_end, freq="D").strftime("%Y-%m-%d").tolist()
    # Initialize progress bar for date processing
    date_list_with_tqdm_bar = tqdm(date_list)

    # Process each date in the range
    for date in date_list_with_tqdm_bar:
        try:
            # Get date_id for current date
            date_id = get_date_id(date)
        except Exception as e:
            # Log error if date_id retrieval fails
            logger.error(f"Failed to get date_id for date '{date}'. Error: {e}")
            continue  # Skip to next date if current date fails

        try:
            # Scrape domestic fruit data for current date
            domestic_data = scrape_domestic_fruit_data(date, date_id)
            # Add domestic data to recorder
            domestic_fruit_recorder.add_data(domestic_data)
        except Exception as e:
            # Log error if domestic data scraping fails
            logger.error(f"Failed to scrape domestic fruit data for date '{date}'. Error: {e}")

        try:
            # Scrape imported fruit data for current date
            imported_data = scrape_imported_fruit_data(date, date_id)
            # Add imported data to recorder
            imported_fruit_recorder.add_data(imported_data)
        except Exception as e:
            # Log error if imported data scraping fails
            logger.error(f"Failed to scrape imported fruit data for date '{date}'. Error: {e}")

        # Update progress bar with current date
        date_list_with_tqdm_bar.set_postfix_str(f"Date: {date}")

    # Save all collected domestic fruit data to CSV
    domestic_fruit_recorder.record()
    # Save all collected imported fruit data to CSV
    imported_fruit_recorder.record()


if __name__ == "__main__":
    main(date_end="2025-01-23")
