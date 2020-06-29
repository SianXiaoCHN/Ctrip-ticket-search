from json import dumps
from os import system

from bs4 import BeautifulSoup
from prettytable import PrettyTable
from requests import post


def searchTrain(dcity: str, acity: str, date: str):
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Content-Type": "application/json"}
    url = "https://trains.ctrip.com/pages/booking/searchTrainList"

    request_payload = {"departCityName": dcity,
                       "arriveCityName": acity, "departDate": "2020-07-02", "trainNum": ""}

    r = post(url, data=dumps(request_payload), headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    table = PrettyTable(["车次", "发车时间", "到达时间", "用时", "坐席", "票价", "余票"])
    table.padding_width = 1
    trains = soup.jsonresult.data.find_all('trainlist')
    if not trains:
        print("\n=========未查询到车次数据！============")
        return

    for train in trains:
        info = {}
        # 车次
        info['TrainName'] = str(train.trainname.string)
        info['StartTime'] = str(train.starttime.string)
        info['EndTime'] = str(train.endtime.string)
        info['TakeTime'] = str(train.taketime.string)
        info['SeatName'] = ""
        info['Price'] = ""
        info['Inventory'] = ""

        seats = train.seatbookingitem.contents
        for seat in seats:
            info['SeatName'] += str(seat.seatname.string) + "\n"
            info['Price'] += str(seat.price.string) + "\n"
            info['Inventory'] += str(seat.inventory.string) + "\n"
        table.add_row(list(info.values()))
    system('cls')
    print(dcity, '------->', acity, date)
    print(table)


if __name__ == "__main__":
    while True:
        print('输入起点、终点、日期，以空格分开，举例：')
        print('北京 上海 20200629')
        print('直接回车即可退出')
        raw_data = input()

        if not raw_data:
            break
        try:
            dcity, acity, date = raw_data.split(' ')
            searchTrain(dcity, acity, date)
        except:
            print('输入内容有误')
