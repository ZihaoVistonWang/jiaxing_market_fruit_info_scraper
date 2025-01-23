import time
import pandas as pd
from DataRecorder import Recorder
from DrissionPage import SessionPage
from loguru import logger
from tqdm.auto import tqdm

logger.add("log.log", rotation="10 MB", level="INFO")


def scrape_domestic_fruit_data(
    date: str,
):
    url = "http://jxzgsgzs.com/jia-xing-fruit-webapi/stage"
    params = {
        "reportCycle": "10",
        "rawDataIsPublish": "true",
        "pageSize": "1",
        "orderBy": "-reportTimeStart",
        "reportTimeStart": date,
    }

    try_times = 0
    session = SessionPage()

    while True:
        session.get(url=url, params=params)
        json_data = session.json

        if json_data["success"] == 1:
            break
        else:
            try_times += 1
            logger.warning(f"Request failed. Attempt {try_times} for domestic fruit data in date '{date}' when we get 'date_id'. Waiting for 5 seconds before retrying.")
            time.sleep(5)
            if try_times >= 3:
                logger.error(f"Failed 3 times for domestic fruit data in date '{date}' when we get 'date_id'. Waiting for 5 minutes before retrying.")
                try_times = 0
                time.sleep(60 * 5)

    date_id = json_data["data"][0]["id"]

    data_list = []
    for pageNo in range(1, 100):
        url = "http://jxzgsgzs.com/jia-xing-fruit-webapi/rawDataExpansion"
        params = {
            "stageId": f"{date_id}",
            "orderBy": "-struct.sortNum,category,kind,placeOfOrigin,city",
            "parentStructId": "1",
            "pageNo": f"{pageNo}",
            "pageSize": "1000",
        }
        session = SessionPage()
        session.get(url=url, params=params)
        json_data = session.json

        while True:
            if json_data["success"] == 1:
                break
            else:
                logger.warning(f"Request failed. Attempt {try_times} for domestic fruit data in date '{date}' when we get 'data'. Waiting for 5 seconds before retrying.")
                time.sleep(5)
                if try_times >= 3:
                    logger.error(f"Failed 3 times for domestic fruit data in date '{date}' when we get 'data'. Waiting for 5 minutes before retrying.")
                    try_times = 0
                    time.sleep(60 * 5)

        data = json_data["data"]
        data_list += data

        if json_data["total"] <= 1000:
            break

    for data in data_list:
        data["date"] = date

    return data_list

def main(
    date_end: str,
    date_start: str = "2018-01-01",
):
    domestic_fruit_recorder = Recorder("domestic_fruit_info.csv")
    domestic_fruit_recorder.set.cache_size(10000)
    domestic_fruit_recorder.set.show_msg(False)
    domestic_fruit_recorder.set.encoding("utf-8-sig")

    date_list = pd.date_range(start=date_start, end=date_end, freq="D").strftime("%Y-%m-%d").tolist()
    date_list_with_tqdm_bar = tqdm(date_list)

    for date in date_list_with_tqdm_bar:
        try:
            data = scrape_domestic_fruit_data(date)
            domestic_fruit_recorder.add_data(data)
        except Exception as e:
            logger.error(f"Failed to scrape domestic fruit data in date '{date}'. Error: {e}")
        date_list_with_tqdm_bar.set_postfix_str(f"Date: {date}")

    domestic_fruit_recorder.record()


if __name__ == "__main__":
    main(date_end="2018-01-05")