import tkinter as tk
import tkinter.ttk as tt
import csv
from tkinter import messagebox
import pandas as pd



# 計算位置的計數器 每按一次確認button會加一
count_transport = 0
# 使用交通工具次數
count_day1 = 0
count_day2 = 0
count_day3 = 0
count_day4 = 0
count_day5 = 0
count_day6 = 0
count_day7 = 0
# 計算今天是星期幾
day = 1

comtransport_day2 = 0
comtransport_day3 = 0
comtransport_day4 = 0
comtransport_day5 = 0
comtransport_day6 = 0
comtransport_day7 = 0
varsection_day1 = dict()
entsection_day1 = dict()
vardeparture_day1 = dict()
entdeparture_day1 = dict()
vardestination_day1 = dict()
entdestination_day1 = dict()

varsection_day2 = dict()  # 用dict去做動態變數命名
entsection_day2 = dict()
vardeparture_day2 = dict()
entdeparture_day2 = dict()
vardestination_day2 = dict()
entdestination_day2 = dict()

varsection_day3 = dict()
entsection_day3 = dict()
vardeparture_day3 = dict()
entdeparture_day3 = dict()
vardestination_day3 = dict()
entdestination_day3 = dict()


varsection_day4 = dict()
entsection_day4 = dict()
vardeparture_day4 = dict()
entdeparture_day4 = dict()
vardestination_day4 = dict()
entdestination_day4 = dict()

varsection_day5 = dict()
entsection_day5 = dict()
vardeparture_day5 = dict()
entdeparture_day5 = dict()
vardestination_day5 = dict()
entdestination_day5 = dict()

varsection_day6 = dict()
entsection_day6 = dict()
vardeparture_day6 = dict()
entdeparture_day6 = dict()
vardestination_day6 = dict()
entdestination_day6 = dict()


varsection_day7 = dict()
entsection_day7 = dict()
vardeparture_day7 = dict()
entdeparture_day7 = dict()
vardestination_day7 = dict()
entdestination_day7 = dict()

# 計算用到的變數(這些都用總額累計就好！)
mrt_trips = 0  # 7天搭了幾趟捷運
accumulated_mrt_fare = 0  # 7天常客優惠的計算金額(原價)-->算優惠用的
total_ticket_fare = 0  # 7天現金花費(實際)
total_expense = 0
# 票價資訊
ticket_type = ""
bus_fare = 0
discount_bus = 0
difference = 0  # diff是轉乘優惠的金額
# 紀錄使用的工具(以組為單位)
sequence_list = list()
# 用來動態get section, begin station, final station
list_get = dict()
for i in range(1, 8):
    list_get[i] = [0]




import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def count_mrt_fare(begin, final):
    """ 給予起迄站，找出原本票價 """
    # file_input = entName.get()
    # file = open(file_input, "r", encoding='utf-8')
    url = "https://drive.google.com/uc?export=download&id=1ts6h34cldZrA16HESR3keD1y9j7bxZg7"
    file = urllib.request.urlopen(url).read().decode('utf-8')
    csvFile = csv.DictReader(file)
    for row in csvFile:
        if row["Departure_Station"] == begin and row["Destination_Station"] == final:
            fare = row["Adult/Full Fare Tickets"]

    return fare  # fare會是原本票價







def get_ticket_type():
    """獲取票種資訊"""
    global ticket_type
    global bus_fare
    global discount_bus
    global difference

    ticket_type = comTicket.get()

    if ticket_type == "全票":
        bus_fare = 15
        discount_bus = 7
        difference = bus_fare - discount_bus
    else:
        bus_fare = 12
        discount_bus = 6
        difference = bus_fare - discount_bus
# 計算票價使用的函數


def this_sche1():
    """ 計算此行程(組)票價資訊(用在按下結束行程)，並小心捷運趟數、原價要累積(算優惠要用)，算完之後會
    清掉當前的交通工具list """
    global sequence_list
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global bus_fare
    global discount_bus
    global difference
    global list_get
    global day
    global entsection_day1
    global entdeparture_day1
    global entdestination_day1

    list_get[day].append(len(sequence_list))
    place2variable = sum(list_get[day][:-1])
    for no_trans_type in range(len(sequence_list)):

        trans_type = sequence_list[no_trans_type]
        if trans_type == "公車":
            sections = int(entsection_day1[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "捷運"
                                        or sequence_list[no_trans_type-1] == "幹線"):
                # 如果已經搭過別的交通工具(也就是trans_type的位置不是0)，且是可以有折扣的
                if sections > 1:  # 若段數超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price    # 其實也可以直接用total來加就好

                else:  # 只有一段
                    price = discount_bus
                    total_ticket_fare += price
            else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                total_ticket_fare += bus_fare * sections

        elif trans_type == "幹線":
            sections = int(entsection_day1[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if no_trans_type != 0:  # 如果前面搭過任何交通工具(亦即，這項交通工具的位置非0)，都能享有優惠
                if sections > 1:  # 搭超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price
                else:  # 搭一段而已
                    total_ticket_fare += discount_bus
            else:  # 若沒搭過別的交通工具
                total_ticket_fare += bus_fare * sections

        elif trans_type == "捷運":
            begin_station = entdeparture_day1[no_trans_type +
                                              place2variable + 1].get()
            final_station = entdestination_day1[no_trans_type +
                                                place2variable + 1].get()
            mrt_fare = count_mrt_fare(begin_station, final_station)
            mrt_trips += 1
            # 是否有轉乘優惠
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "公車" or
                                        sequence_list[no_trans_type - 1] == "幹線"):
                new_fare = mrt_fare - difference    # diff是轉乘優惠的金額
                total_ticket_fare += new_fare     # 實際花費了多少錢
                accumulated_mrt_fare += mrt_fare    # one_day_mrt fare是原價，最後算優惠的時候用
            else:   # 沒有優惠就都是加上原價
                total_ticket_fare += mrt_fare
                accumulated_mrt_fare += mrt_fare
    sequence_list = []
    print(total_ticket_fare)


def this_sche2():
    """ 計算此行程(組)票價資訊(用在按下結束行程)，並小心捷運趟數、原價要累積(算優惠要用)，算完之後會
    清掉當前的交通工具list """
    global sequence_list
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global bus_fare
    global discount_bus
    global difference
    global list_get
    global day
    global entsection_day2
    global entdeparture_day2
    global entdestination_day2

    list_get[day].append(len(sequence_list))
    place2variable = sum(list_get[day][:-1])
    for no_trans_type in range(len(sequence_list)):

        trans_type = sequence_list[no_trans_type]
        if trans_type == "公車":
            sections = int(entsection_day2[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "捷運"
                                        or sequence_list[no_trans_type-1] == "幹線"):
                # 如果已經搭過別的交通工具(也就是trans_type的位置不是0)，且是可以有折扣的
                if sections > 1:  # 若段數超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price    # 其實也可以直接用total來加就好

                else:  # 只有一段
                    price = discount_bus
                    total_ticket_fare += price
            else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                total_ticket_fare += bus_fare * sections

        elif trans_type == "幹線":
            sections = int(entsection_day2[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if no_trans_type != 0:  # 如果前面搭過任何交通工具(亦即，這項交通工具的位置非0)，都能享有優惠
                if sections > 1:  # 搭超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price
                else:  # 搭一段而已
                    total_ticket_fare += discount_bus
            else:  # 若沒搭過別的交通工具
                total_ticket_fare += bus_fare * sections

        elif trans_type == "捷運":
            begin_station = entdeparture_day2[no_trans_type +
                                              place2variable + 1].get()
            final_station = entdestination_day2[no_trans_type +
                                                place2variable + 1].get()
            mrt_fare = count_mrt_fare(begin_station, final_station)
            mrt_trips += 1
            # 是否有轉乘優惠
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "公車" or
                                        sequence_list[no_trans_type - 1] == "幹線"):
                new_fare = mrt_fare - difference    # diff是轉乘優惠的金額
                total_ticket_fare += new_fare     # 實際花費了多少錢
                accumulated_mrt_fare += mrt_fare    # one_day_mrt fare是原價，最後算優惠的時候用
            else:   # 沒有優惠就都是加上原價
                total_ticket_fare += mrt_fare
                accumulated_mrt_fare += mrt_fare
    sequence_list = []
    print(total_ticket_fare)


def this_sche3():
    """ 計算此行程(組)票價資訊(用在按下結束行程)，並小心捷運趟數、原價要累積(算優惠要用)，算完之後會
    清掉當前的交通工具list """
    global sequence_list
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global bus_fare
    global discount_bus
    global difference
    global list_get
    global day
    global entsection_day3
    global entdeparture_day3
    global entdestination_day3

    list_get[day].append(len(sequence_list))
    place2variable = sum(list_get[day][:-1])
    for no_trans_type in range(len(sequence_list)):

        trans_type = sequence_list[no_trans_type]
        if trans_type == "公車":
            sections = int(entsection_day3[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "捷運"
                                        or sequence_list[no_trans_type-1] == "幹線"):
                # 如果已經搭過別的交通工具(也就是trans_type的位置不是0)，且是可以有折扣的
                if sections > 1:  # 若段數超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price    # 其實也可以直接用total來加就好

                else:  # 只有一段
                    price = discount_bus
                    total_ticket_fare += price
            else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                total_ticket_fare += bus_fare * sections

        elif trans_type == "幹線":
            sections = int(entsection_day3[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if no_trans_type != 0:  # 如果前面搭過任何交通工具(亦即，這項交通工具的位置非0)，都能享有優惠
                if sections > 1:  # 搭超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price
                else:  # 搭一段而已
                    total_ticket_fare += discount_bus
            else:  # 若沒搭過別的交通工具
                total_ticket_fare += bus_fare * sections

        elif trans_type == "捷運":
            begin_station = entdeparture_day3[no_trans_type +
                                              place2variable + 1].get()
            final_station = entdestination_day3[no_trans_type +
                                                place2variable + 1].get()
            mrt_fare = count_mrt_fare(begin_station, final_station)
            mrt_trips += 1
            # 是否有轉乘優惠
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "公車" or
                                        sequence_list[no_trans_type - 1] == "幹線"):
                new_fare = mrt_fare - difference    # diff是轉乘優惠的金額
                total_ticket_fare += new_fare     # 實際花費了多少錢
                accumulated_mrt_fare += mrt_fare    # one_day_mrt fare是原價，最後算優惠的時候用
            else:   # 沒有優惠就都是加上原價
                total_ticket_fare += mrt_fare
                accumulated_mrt_fare += mrt_fare
    sequence_list = []
    print(total_ticket_fare)


def this_sche4():
    """ 計算此行程(組)票價資訊(用在按下結束行程)，並小心捷運趟數、原價要累積(算優惠要用)，算完之後會
    清掉當前的交通工具list """
    global sequence_list
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global bus_fare
    global discount_bus
    global difference
    global list_get
    global day
    global entsection_day4
    global entdeparture_day4
    global entdestination_day4

    list_get[day].append(len(sequence_list))
    place2variable = sum(list_get[day][:-1])
    for no_trans_type in range(len(sequence_list)):

        trans_type = sequence_list[no_trans_type]
        if trans_type == "公車":
            sections = int(entsection_day4[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "捷運"
                                        or sequence_list[no_trans_type-1] == "幹線"):
                # 如果已經搭過別的交通工具(也就是trans_type的位置不是0)，且是可以有折扣的
                if sections > 1:  # 若段數超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price    # 其實也可以直接用total來加就好

                else:  # 只有一段
                    price = discount_bus
                    total_ticket_fare += price
            else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                total_ticket_fare += bus_fare * sections

        elif trans_type == "幹線":
            sections = int(entsection_day4[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if no_trans_type != 0:  # 如果前面搭過任何交通工具(亦即，這項交通工具的位置非0)，都能享有優惠
                if sections > 1:  # 搭超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price
                else:  # 搭一段而已
                    total_ticket_fare += discount_bus
            else:  # 若沒搭過別的交通工具
                total_ticket_fare += bus_fare * sections

        elif trans_type == "捷運":
            begin_station = entdeparture_day4[no_trans_type +
                                              place2variable + 1].get()
            final_station = entdestination_day4[no_trans_type +
                                                place2variable + 1].get()
            mrt_fare = count_mrt_fare(begin_station, final_station)
            mrt_trips += 1
            # 是否有轉乘優惠
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "公車" or
                                        sequence_list[no_trans_type - 1] == "幹線"):
                new_fare = mrt_fare - difference    # diff是轉乘優惠的金額
                total_ticket_fare += new_fare     # 實際花費了多少錢
                accumulated_mrt_fare += mrt_fare    # one_day_mrt fare是原價，最後算優惠的時候用
            else:   # 沒有優惠就都是加上原價
                total_ticket_fare += mrt_fare
                accumulated_mrt_fare += mrt_fare
    sequence_list = []
    print(total_ticket_fare)


def this_sche5():
    """ 計算此行程(組)票價資訊(用在按下結束行程)，並小心捷運趟數、原價要累積(算優惠要用)，算完之後會
    清掉當前的交通工具list """
    global sequence_list
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global bus_fare
    global discount_bus
    global difference
    global list_get
    global day
    global entsection_day5
    global entdeparture_day5
    global entdestination_day5

    list_get[day].append(len(sequence_list))
    place2variable = sum(list_get[day][:-1])
    for no_trans_type in range(len(sequence_list)):

        trans_type = sequence_list[no_trans_type]
        if trans_type == "公車":
            sections = int(entsection_day5[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "捷運"
                                        or sequence_list[no_trans_type-1] == "幹線"):
                # 如果已經搭過別的交通工具(也就是trans_type的位置不是0)，且是可以有折扣的
                if sections > 1:  # 若段數超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price    # 其實也可以直接用total來加就好

                else:  # 只有一段
                    price = discount_bus
                    total_ticket_fare += price
            else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                total_ticket_fare += bus_fare * sections

        elif trans_type == "幹線":
            sections = int(entsection_day5[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if no_trans_type != 0:  # 如果前面搭過任何交通工具(亦即，這項交通工具的位置非0)，都能享有優惠
                if sections > 1:  # 搭超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price
                else:  # 搭一段而已
                    total_ticket_fare += discount_bus
            else:  # 若沒搭過別的交通工具
                total_ticket_fare += bus_fare * sections

        elif trans_type == "捷運":
            begin_station = entdeparture_day5[no_trans_type +
                                              place2variable + 1].get()
            final_station = entdestination_day5[no_trans_type +
                                                place2variable + 1].get()
            mrt_fare = count_mrt_fare(begin_station, final_station)
            mrt_trips += 1
            # 是否有轉乘優惠
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "公車" or
                                        sequence_list[no_trans_type - 1] == "幹線"):
                new_fare = mrt_fare - difference    # diff是轉乘優惠的金額
                total_ticket_fare += new_fare     # 實際花費了多少錢
                accumulated_mrt_fare += mrt_fare    # one_day_mrt fare是原價，最後算優惠的時候用
            else:   # 沒有優惠就都是加上原價
                total_ticket_fare += mrt_fare
                accumulated_mrt_fare += mrt_fare
    sequence_list = []
    print(total_ticket_fare)


def this_sche6():
    """ 計算此行程(組)票價資訊(用在按下結束行程)，並小心捷運趟數、原價要累積(算優惠要用)，算完之後會
    清掉當前的交通工具list """
    global sequence_list
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global bus_fare
    global discount_bus
    global difference
    global list_get
    global day
    global entsection_day6
    global entdeparture_day6
    global entdestination_day6

    list_get[day].append(len(sequence_list))
    place2variable = sum(list_get[day][:-1])
    for no_trans_type in range(len(sequence_list)):

        trans_type = sequence_list[no_trans_type]
        if trans_type == "公車":
            sections = int(entsection_day6[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "捷運"
                                        or sequence_list[no_trans_type-1] == "幹線"):
                # 如果已經搭過別的交通工具(也就是trans_type的位置不是0)，且是可以有折扣的
                if sections > 1:  # 若段數超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price    # 其實也可以直接用total來加就好

                else:  # 只有一段
                    price = discount_bus
                    total_ticket_fare += price
            else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                total_ticket_fare += bus_fare * sections

        elif trans_type == "幹線":
            sections = int(entsection_day6[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if no_trans_type != 0:  # 如果前面搭過任何交通工具(亦即，這項交通工具的位置非0)，都能享有優惠
                if sections > 1:  # 搭超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price
                else:  # 搭一段而已
                    total_ticket_fare += discount_bus
            else:  # 若沒搭過別的交通工具
                total_ticket_fare += bus_fare * sections

        elif trans_type == "捷運":
            begin_station = entdeparture_day6[no_trans_type +
                                              place2variable + 1].get()
            final_station = entdestination_day6[no_trans_type +
                                                place2variable + 1].get()
            mrt_fare = count_mrt_fare(begin_station, final_station)
            mrt_trips += 1
            # 是否有轉乘優惠
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "公車" or
                                        sequence_list[no_trans_type - 1] == "幹線"):
                new_fare = mrt_fare - difference    # diff是轉乘優惠的金額
                total_ticket_fare += new_fare     # 實際花費了多少錢
                accumulated_mrt_fare += mrt_fare    # one_day_mrt fare是原價，最後算優惠的時候用
            else:   # 沒有優惠就都是加上原價
                total_ticket_fare += mrt_fare
                accumulated_mrt_fare += mrt_fare
    sequence_list = []
    print(total_ticket_fare)


def this_sche7():
    """ 計算此行程(組)票價資訊(用在按下結束行程)，並小心捷運趟數、原價要累積(算優惠要用)，算完之後會
    清掉當前的交通工具list """
    global sequence_list
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global bus_fare
    global discount_bus
    global difference
    global list_get
    global day
    global entsection_day7
    global entdeparture_day7
    global entdestination_day7

    list_get[day].append(len(sequence_list))
    place2variable = sum(list_get[day][:-1])
    for no_trans_type in range(len(sequence_list)):

        trans_type = sequence_list[no_trans_type]
        if trans_type == "公車":
            sections = int(entsection_day7[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "捷運"
                                        or sequence_list[no_trans_type-1] == "幹線"):
                # 如果已經搭過別的交通工具(也就是trans_type的位置不是0)，且是可以有折扣的
                if sections > 1:  # 若段數超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price    # 其實也可以直接用total來加就好

                else:  # 只有一段
                    price = discount_bus
                    total_ticket_fare += price
            else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                total_ticket_fare += bus_fare * sections

        elif trans_type == "幹線":
            sections = int(entsection_day7[no_trans_type +
                                           place2variable + 1].get())  # 需要去get，並轉成int
            if no_trans_type != 0:  # 如果前面搭過任何交通工具(亦即，這項交通工具的位置非0)，都能享有優惠
                if sections > 1:  # 搭超過一段
                    price = discount_bus + bus_fare * (sections - 1)
                    total_ticket_fare += price
                else:  # 搭一段而已
                    total_ticket_fare += discount_bus
            else:  # 若沒搭過別的交通工具
                total_ticket_fare += bus_fare * sections

        elif trans_type == "捷運":
            begin_station = entdeparture_day7[no_trans_type +
                                              place2variable + 1].get()
            final_station = entdestination_day7[no_trans_type +
                                                place2variable + 1].get()
            mrt_fare = count_mrt_fare(begin_station, final_station)
            mrt_trips += 1
            # 是否有轉乘優惠
            if (no_trans_type > 0) and (sequence_list[no_trans_type - 1] == "公車" or
                                        sequence_list[no_trans_type - 1] == "幹線"):
                new_fare = mrt_fare - difference    # diff是轉乘優惠的金額
                total_ticket_fare += new_fare     # 實際花費了多少錢
                accumulated_mrt_fare += mrt_fare    # one_day_mrt fare是原價，最後算優惠的時候用
            else:   # 沒有優惠就都是加上原價
                total_ticket_fare += mrt_fare
                accumulated_mrt_fare += mrt_fare
    sequence_list = []
    print(total_ticket_fare)

# day2系列


def end_schedule_2_day2():
    global count_transport
    global comtransport_day2
    global day
    global sequence_list
    sequence_list = []
    day += 1
    labtransport2 = tk.Label(
        frame, text="Day2", justify=tk.RIGHT, width=50)  # 設定標籤
    end_sche2 = tk.Button(frame, text="結束當日行程", bg="pink",
                          command=end_schedule_2_day3)  # 新增結束按鈕
    count_transport += 1  # 要算出新增的時候y要加多少
    labtransport2.place(x=10, y=100+count_transport*30, width=100, height=30)
    end_sche2.place(x=110, y=100+count_transport*30, width=120, height=30)
    end_this_sche2 = tk.Button(frame, text="結束行程", bg="pink",
                               command=this_sche2)
    end_this_sche2.place(x=250, y=100+count_transport*30, width=60, height=30)
    count_transport += 1
    labtransport_day2 = tk.Label(
        frame, text="交通工具", justify=tk.RIGHT, width=50)
    labtransport_day2.place(x=10, y=100+count_transport *
                            30, width=100, height=30)

    comtransport_day2 = tt.Combobox(
        frame, width=50, values=stdtransport, state="readonly")
    comtransport_day2.place(x=110, y=100+count_transport *
                            30, width=75, height=30)
    btn_day2 = tt.Button(
        frame, text="確認", command=checkcmbo_day2)  # 新增確定button
    btn_day2.place(x=190, y=100+count_transport *
                   30, width=75, height=30)


def checkcmbo_day2():
    # 確認鍵的函數執行，以取得下拉選單中的選取目標，並作後續判斷，進而提出問題'''
    global count_transport
    global comtransport_day2
    global count_day2
    global entsection_day2
    global entdeparture_day2
    global entdestination_day2
    count_transport += 1
    count_day2 += 1

    if comtransport_day2.get() == "公車" or comtransport_day2.get() == "幹線":
        labsection = tk.Label(
            frame, text="搭乘段數:", justify=tk.RIGHT, width=50)
        labsection.place(
            x=10, y=100+count_transport*30, width=100, height=30)
        varsection_day2[count_day2] = tk.StringVar()
        varsection_day2[count_day2].set("")
        entsection_day2[count_day2] = tk.Entry(
            frame, width=120, textvariable=varsection_day2[count_day2])  # 製作輸入的地方
        entsection_day2[count_day2].place(
            x=110, y=100+count_transport*30, width=120, height=30)

    elif comtransport_day2.get() == "捷運":
        labdeparture = tk.Label(frame, text="起始站站名:",
                                justify=tk.RIGHT, width=50)
        labdeparture.place(x=10, y=100+count_transport *
                           30, width=100, height=30)
        vardeparture_day2[count_day2] = tk.StringVar()
        vardeparture_day2[count_day2].set("")
        entdeparture_day2[count_day2] = tk.Entry(
            frame, width=120, textvariable=vardeparture_day2[count_day2])
        entdeparture_day2[count_day2].place(x=110, y=100+count_transport *
                                            30, width=120, height=30)

        labdestination = tk.Label(
            frame, text="目的地站名:", justify=tk.RIGHT, width=50)
        labdestination.place(x=210, y=100+count_transport *
                             30, width=100, height=30)
        vardestination_day2[count_day2] = tk.StringVar()
        vardestination_day2[count_day2].set("")
        entdestination_day2[count_day2] = tk.Entry(
            frame, width=120, textvariable=vardestination_day2[count_day2])
        entdestination_day2[count_day2].place(x=310, y=100+count_transport *
                                              30, width=120, height=30)
    sequence_list.append(comtransport_day2.get())
    print(sequence_list)

# day3系列


def end_schedule_2_day3():
    global count_transport
    global comtransport_day3
    global sequence_list
    global day
    sequence_list = []
    day += 1
    labtransport3 = tk.Label(frame, text="Day3", justify=tk.RIGHT, width=50)
    end_sche3 = tk.Button(frame, text="結束當日行程", bg="pink",
                          command=end_schedule_2_day4)
    count_transport += 1  # 要算出新增的時候y要加多少
    labtransport3.place(x=10, y=100+count_transport*30, width=100, height=30)
    end_sche3.place(x=110, y=100+count_transport*30, width=120, height=30)
    end_this_sche3 = tk.Button(frame, text="結束行程", bg="pink",
                               command=this_sche3)
    end_this_sche3.place(x=250, y=100+count_transport*30, width=60, height=30)
    count_transport += 1
    labtransport_day3 = tk.Label(
        frame, text="交通工具", justify=tk.RIGHT, width=50)
    labtransport_day3.place(x=10, y=100+count_transport *
                            30, width=100, height=30)
    comtransport_day3 = tt.Combobox(
        frame, width=50, values=stdtransport, state="readonly")
    comtransport_day3.place(x=110, y=100+count_transport *
                            30, width=75, height=30)
    btn_day3 = tt.Button(frame, text="確認", command=checkcmbo_day3)
    btn_day3.place(x=190, y=100+count_transport *
                   30, width=75, height=30)


def checkcmbo_day3():
    global count_transport
    global comtransport_day3
    global count_day3
    global entsection_day3
    global entdeparture_day3
    global entdestination_day3
    count_transport += 1
    count_day3 += 1

    if comtransport_day3.get() == "公車" or comtransport_day3.get() == "幹線":
        labsection = tk.Label(
            frame, text="搭乘段數:", justify=tk.RIGHT, width=50)
        labsection.place(
            x=10, y=100+count_transport*30, width=100, height=30)
        varsection_day3[count_day3] = tk.StringVar()
        varsection_day3[count_day3].set("")
        entsection_day3[count_day3] = tk.Entry(
            frame, width=120, textvariable=varsection_day3[count_day3])
        entsection_day3[count_day3].place(
            x=110, y=100+count_transport*30, width=120, height=30)

    elif comtransport_day3.get() == "捷運":
        labdeparture = tk.Label(frame, text="起始站站名:",
                                justify=tk.RIGHT, width=50)
        labdeparture.place(x=10, y=100+count_transport *
                           30, width=100, height=30)
        vardeparture_day3[count_day3] = tk.StringVar()
        vardeparture_day3[count_day3].set("")
        entdeparture_day3[count_day3] = tk.Entry(
            frame, width=120, textvariable=vardeparture_day3[count_day3])
        entdeparture_day3[count_day3].place(x=110, y=100+count_transport *
                                            30, width=120, height=30)

        labdestination = tk.Label(
            frame, text="目的地站名:", justify=tk.RIGHT, width=50)
        labdestination.place(x=210, y=100+count_transport *
                             30, width=100, height=30)
        vardestination_day3[count_day3] = tk.StringVar()
        vardestination_day3[count_day3].set("")
        entdestination_day3[count_day3] = tk.Entry(
            frame, width=120, textvariable=vardestination_day3[count_day3])
        entdestination_day3[count_day3].place(x=310, y=100+count_transport *
                                              30, width=120, height=30)
    sequence_list.append(comtransport_day3.get())
    print(sequence_list)


# day4系列
def end_schedule_2_day4():
    global count_transport
    global comtransport_day4
    global sequence_list
    global day
    sequence_list = []
    day += 1
    labtransport4 = tk.Label(frame, text="Day4", justify=tk.RIGHT, width=50)
    end_sche4 = tk.Button(frame, text="結束當日行程", bg="pink",
                          command=end_schedule_2_day5)
    count_transport += 1  # 要算出新增的時候y要加多少
    labtransport4.place(x=10, y=100+count_transport*30, width=100, height=30)
    end_sche4.place(x=110, y=100+count_transport*30, width=120, height=30)
    end_this_sche4 = tk.Button(frame, text="結束行程", bg="pink",
                               command=this_sche4)
    end_this_sche4.place(x=250, y=100+count_transport*30, width=60, height=30)
    count_transport += 1
    labtransport_day4 = tk.Label(
        frame, text="交通工具", justify=tk.RIGHT, width=50)
    labtransport_day4.place(x=10, y=100+count_transport *
                            30, width=100, height=30)
    comtransport_day4 = tt.Combobox(
        frame, width=50, values=stdtransport, state="readonly")
    comtransport_day4.place(x=110, y=100+count_transport *
                            30, width=75, height=30)
    btn_day4 = tt.Button(frame, text="確認", command=checkcmbo_day4)
    btn_day4.place(x=190, y=100+count_transport *
                   30, width=75, height=30)


def checkcmbo_day4():
    global count_transport
    global comtransport_day4
    global count_day4
    global entsection_day4
    global entdeparture_day4
    global entdestination_day4
    count_transport += 1
    count_day4 += 1

    if comtransport_day4.get() == "公車" or comtransport_day4.get() == "幹線":
        labsection = tk.Label(
            frame, text="搭乘段數:", justify=tk.RIGHT, width=50)
        labsection.place(
            x=10, y=100+count_transport*30, width=100, height=30)
        varsection_day4[count_day4] = tk.StringVar()
        varsection_day4[count_day4].set("")
        entsection_day4[count_day4] = tk.Entry(
            frame, width=120, textvariable=varsection_day4[count_day4])
        entsection_day4[count_day4].place(
            x=110, y=100+count_transport*30, width=120, height=30)

    elif comtransport_day4.get() == "捷運":
        labdeparture = tk.Label(frame, text="起始站站名:",
                                justify=tk.RIGHT, width=50)
        labdeparture.place(x=10, y=100+count_transport *
                           30, width=100, height=30)
        vardeparture_day4[count_day4] = tk.StringVar()
        vardeparture_day4[count_day4].set("")
        entdeparture_day4[count_day4] = tk.Entry(
            frame, width=120, textvariable=vardeparture_day4[count_day4])
        entdeparture_day4[count_day4].place(x=110, y=100+count_transport *
                                            30, width=120, height=30)

        labdestination = tk.Label(
            frame, text="目的地站名:", justify=tk.RIGHT, width=50)
        labdestination.place(x=210, y=100+count_transport *
                             30, width=100, height=30)
        vardestination_day4[count_day4] = tk.StringVar()
        vardestination_day4[count_day4].set("")
        entdestination_day4[count_day4] = tk.Entry(
            frame, width=120, textvariable=vardestination_day4[count_day4])
        entdestination_day4[count_day4].place(x=310, y=100+count_transport *
                                              30, width=120, height=30)
    sequence_list.append(comtransport_day4.get())
    print(sequence_list)

# day5系列


def end_schedule_2_day5():
    global count_transport
    global comtransport_day5
    global sequence_list
    global day
    sequence_list = []
    day += 1
    labtransport5 = tk.Label(frame, text="Day5", justify=tk.RIGHT, width=50)
    end_sche5 = tk.Button(frame, text="結束當日行程", bg="pink",
                          command=end_schedule_2_day6)
    count_transport += 1  # 要算出新增的時候y要加多少
    labtransport5.place(x=10, y=100+count_transport*30, width=100, height=30)
    end_sche5.place(x=110, y=100+count_transport*30, width=120, height=30)
    end_this_sche5 = tk.Button(frame, text="結束行程", bg="pink",
                               command=this_sche5)
    end_this_sche5.place(x=250, y=100+count_transport*30, width=60, height=30)
    count_transport += 1
    labtransport_day5 = tk.Label(
        frame, text="交通工具", justify=tk.RIGHT, width=50)
    labtransport_day5.place(x=10, y=100+count_transport *
                            30, width=100, height=30)
    comtransport_day5 = tt.Combobox(
        frame, width=50, values=stdtransport, state="readonly")
    comtransport_day5.place(x=110, y=100+count_transport *
                            30, width=75, height=30)
    btn_day5 = tt.Button(frame, text="確認", command=checkcmbo_day5)
    btn_day5.place(x=190, y=100+count_transport *
                   30, width=75, height=30)


def checkcmbo_day5():
    global count_transport
    global comtransport_day5
    global count_day5
    global entsection_day5
    global entdeparture_day5
    global entdestination_day5
    count_transport += 1
    count_day5 += 1

    if comtransport_day5.get() == "公車" or comtransport_day5.get() == "幹線":
        labsection = tk.Label(
            frame, text="搭乘段數:", justify=tk.RIGHT, width=50)
        labsection.place(
            x=10, y=100+count_transport*30, width=100, height=30)
        varsection_day5[count_day5] = tk.StringVar()
        varsection_day5[count_day5].set("")
        entsection_day5[count_day5] = tk.Entry(
            frame, width=120, textvariable=varsection_day5[count_day5])
        entsection_day5[count_day5].place(
            x=110, y=100+count_transport*30, width=120, height=30)

    elif comtransport_day5.get() == "捷運":
        labdeparture = tk.Label(frame, text="起始站站名:",
                                justify=tk.RIGHT, width=50)
        labdeparture.place(x=10, y=100+count_transport *
                           30, width=100, height=30)
        vardeparture_day5[count_day5] = tk.StringVar()
        vardeparture_day5[count_day5].set("")
        entdeparture_day5[count_day5] = tk.Entry(
            frame, width=120, textvariable=vardeparture_day5[count_day5])
        entdeparture_day5[count_day5].place(x=110, y=100+count_transport *
                                            30, width=120, height=30)

        labdestination = tk.Label(
            frame, text="目的地站名:", justify=tk.RIGHT, width=50)
        labdestination.place(x=210, y=100+count_transport *
                             30, width=100, height=30)
        vardestination_day5[count_day5] = tk.StringVar()
        vardestination_day5[count_day5].set("")
        entdestination_day5[count_day5] = tk.Entry(
            frame, width=120, textvariable=vardestination_day5[count_day5])
        entdestination_day5[count_day5].place(x=310, y=100+count_transport *
                                              30, width=120, height=30)
    sequence_list.append(comtransport_day5.get())
    print(sequence_list)


# day6系列


def end_schedule_2_day6():
    global count_transport
    global comtransport_day6
    global day
    global sequence_list
    sequence_list = []
    day += 1
    labtransport6 = tk.Label(frame, text="Day6", justify=tk.RIGHT, width=50)
    end_sche6 = tk.Button(frame, text="結束當日行程", bg="pink",
                          command=end_schedule_2_day7)
    count_transport += 1  # 要算出新增的時候y要加多少
    labtransport6.place(x=10, y=100+count_transport*30, width=100, height=30)
    end_sche6.place(x=110, y=100+count_transport*30, width=120, height=30)
    end_this_sche6 = tk.Button(frame, text="結束行程", bg="pink",
                               command=this_sche6)
    end_this_sche6.place(x=250, y=100+count_transport*30, width=60, height=30)
    count_transport += 1
    labtransport_day6 = tk.Label(
        frame, text="交通工具", justify=tk.RIGHT, width=50)
    labtransport_day6.place(x=10, y=100+count_transport *
                            30, width=100, height=30)
    comtransport_day6 = tt.Combobox(
        frame, width=50, values=stdtransport, state="readonly")
    comtransport_day6.place(x=110, y=100+count_transport *
                            30, width=75, height=30)
    btn_day6 = tt.Button(frame, text="確認", command=checkcmbo_day6)
    btn_day6.place(x=190, y=100+count_transport *
                   30, width=75, height=30)


def checkcmbo_day6():
    global count_transport
    global comtransport_day6
    global count_day6
    global entsection_day6
    global entdeparture_day6
    global entdestination_day6
    count_transport += 1
    count_day6 += 1

    if comtransport_day6.get() == "公車" or comtransport_day6.get() == "幹線":
        labsection = tk.Label(
            frame, text="搭乘段數:", justify=tk.RIGHT, width=50)
        labsection.place(
            x=10, y=100+count_transport*30, width=100, height=30)
        varsection_day6[count_day6] = tk.StringVar()
        varsection_day6[count_day6].set("")
        entsection_day6[count_day6] = tk.Entry(
            frame, width=120, textvariable=varsection_day6[count_day6])
        entsection_day6[count_day6].place(
            x=110, y=100+count_transport*30, width=120, height=30)

    elif comtransport_day6.get() == "捷運":
        labdeparture = tk.Label(frame, text="起始站站名:",
                                justify=tk.RIGHT, width=50)
        labdeparture.place(x=10, y=100+count_transport *
                           30, width=100, height=30)
        vardeparture_day6[count_day6] = tk.StringVar()
        vardeparture_day6[count_day6].set("")
        entdeparture_day6[count_day6] = tk.Entry(
            frame, width=120, textvariable=vardeparture_day6[count_day6])
        entdeparture_day6[count_day6].place(x=110, y=100+count_transport *
                                            30, width=120, height=30)

        labdestination = tk.Label(
            frame, text="目的地站名:", justify=tk.RIGHT, width=50)
        labdestination.place(x=210, y=100+count_transport *
                             30, width=100, height=30)
        vardestination_day6[count_day6] = tk.StringVar()
        vardestination_day6[count_day6].set("")
        entdestination_day6[count_day6] = tk.Entry(
            frame, width=120, textvariable=vardestination_day6[count_day6])
        entdestination_day6[count_day6].place(x=310, y=100+count_transport *
                                              30, width=120, height=30)
    sequence_list.append(comtransport_day6.get())
    print(sequence_list)


# day7系列
def hit_me():
    global total_expense
    print(tk.messagebox.askquestion(
        title='結算報告', message='您的交通花費估計是 %d一共是買1280優惠票會比較划算喔！' % total_expense))


def hit_me2():
    global total_expense
    print(tk.messagebox.askquestion(title='結算報告',
                                    message='您的交通花費估計是 %d 不需要買1280優惠票價，省省錢！' % total_expense))


def hit_me3():
    global total_expense
    print(tk.messagebox.askquestion(title='結算報告',
                                    message='您的交通花費估計是 %d 買不買1280優惠票價都可喔！' % total_expense))


def compute():
    """ 最後結算成一個月花費 """
    global mrt_trips
    global total_ticket_fare
    global accumulated_mrt_fare
    global total_expense

    # 計算一個月的mrt trip
    mrt_trips = round(mrt_trips * (30/7))
    if 11 <= mrt_trips <= 20:
        discount = 0.1
    elif 21 <= mrt_trips <= 30:
        discount = 0.15
    elif 31 <= mrt_trips <= 40:
        discount = 0.2
    elif 41 <= mrt_trips <= 50:
        discount = 0.25
    elif 51 <= mrt_trips:
        discount = 0.3
    else:
        discount = 0
    actual_mrt_fare = accumulated_mrt_fare * (30/7)
    discount_money = actual_mrt_fare * discount
    total_expense = round(total_ticket_fare * (30/7) - discount_money)
    if total_expense > 1280:
        hit_me()
    if total_expense < 1280:
        hit_me2()
    else:
        hit_me3()


def end_schedule_2_day7():
    global count_transport
    global comtransport_day7
    global day
    global sequence_list
    sequence_list = []
    day += 1
    labtransport7 = tk.Label(frame, text="Day7", justify=tk.RIGHT, width=50)
    end_sche7 = tk.Button(frame, text="結算費用", bg="pink", command=compute)
    count_transport += 1  # 要算出新增的時候y要加多少
    labtransport7.place(x=10, y=100+count_transport*30, width=100, height=30)
    end_sche7.place(x=110, y=100+count_transport*30, width=60, height=30)
    end_this_sche7 = tk.Button(frame, text="結束行程", bg="pink",
                               command=this_sche7)
    end_this_sche7.place(x=250, y=100+count_transport*30, width=60, height=30)
    count_transport += 1
    labtransport_day7 = tk.Label(
        frame, text="交通工具", justify=tk.RIGHT, width=50)
    labtransport_day7.place(x=10, y=100+count_transport *
                            30, width=100, height=30)
    comtransport_day7 = tt.Combobox(
        frame, width=50, values=stdtransport, state="readonly")
    comtransport_day7.place(x=110, y=100+count_transport *
                            30, width=75, height=30)
    btn_day7 = tt.Button(frame, text="確認", command=checkcmbo_day7)
    btn_day7.place(x=190, y=100+count_transport *
                   30, width=75, height=30)


def checkcmbo_day7():
    global count_transport
    global comtransport_day7
    global count_day7
    global entsection_day7
    global entdeparture_day7
    global entdestination_day7
    count_transport += 1
    count_day7 += 1

    if comtransport_day7.get() == "公車" or comtransport_day7.get() == "幹線":
        labsection = tk.Label(
            frame, text="搭乘段數:", justify=tk.RIGHT, width=50)
        labsection.place(
            x=10, y=100+count_transport*30, width=100, height=30)
        varsection_day7[count_day7] = tk.StringVar()
        varsection_day7[count_day7].set("")
        entsection_day7[count_day7] = tk.Entry(
            frame, width=120, textvariable=varsection_day7[count_day7])
        entsection_day7[count_day7].place(
            x=110, y=100+count_transport*30, width=120, height=30)

    elif comtransport_day7.get() == "捷運":
        labdeparture = tk.Label(frame, text="起始站站名:",
                                justify=tk.RIGHT, width=50)
        labdeparture.place(x=10, y=100+count_transport *
                           30, width=100, height=30)
        vardeparture_day7[count_day7] = tk.StringVar()
        vardeparture_day7[count_day7].set("")
        entdeparture_day7[count_day7] = tk.Entry(
            frame, width=120, textvariable=vardeparture_day7[count_day7])
        entdeparture_day7[count_day7].place(x=110, y=100+count_transport *
                                            30, width=120, height=30)

        labdestination = tk.Label(
            frame, text="目的地站名:", justify=tk.RIGHT, width=50)
        labdestination.place(x=210, y=100+count_transport *
                             30, width=100, height=30)
        vardestination_day7[count_day7] = tk.StringVar()
        vardestination_day7[count_day7].set("")
        entdestination_day7[count_day7] = tk.Entry(
            frame, width=120, textvariable=vardestination_day7[count_day7])
        entdestination_day7[count_day7].place(x=310, y=100+count_transport *
                                              30, width=120, height=30)
    sequence_list.append(comtransport_day7.get())
    print(sequence_list)


class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        # place canvas on self
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        # place a frame on the canvas, this frame will hold the child widgets
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")
        # place a scrollbar on self
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)
        # attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # pack scrollbar to right of self
        self.vsb.pack(side="right", fill="y")
        # pack canvas to left of self and expand to fil
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",  # add view port frame to canvas
                                                       tags="self.viewPort")

        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        # whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


# 創建有滾輪的視窗
window = tk.Tk()
window.title("要不要買定期票小幫手")
window.geometry("780x1200")
canvas = tk.Canvas(window, width=1200, height=2400, scrollregion=(
    0, 0, 600, 2400), bg='white')  # 创建canvas
frame = tk.Frame(canvas, width=1200, height=2400, bg="white")
vbar = tk.Scrollbar(canvas, orient="vertical")
vbar.pack(side="right", fill="y")
vbar.config(command=canvas.yview)
canvas.config(yscrollcommand=vbar.set)
canvas.pack(expand="yes", fill="both")
canvas.create_window(0, 0, anchor=tk.NE, window=frame)

labName = tk.Label(frame, text="票價兌換表位置:", justify=tk.RIGHT, width=50)
labName.place(x=10, y=10, width=100, height=30)

varName = tk.StringVar()
varName.set("")
entName = tk.Entry(frame, width=120, textvariable=varName)
entName.place(x=110, y=10, width=120, height=30)

labticket = tk.Label(frame, text="票種", justify=tk.RIGHT, width=50)
labticket.place(x=10, y=40, width=100, height=30)
stdTicket = ("全票", "學生票")
comTicket = tt.Combobox(frame, width=50, values=stdTicket, state="readonly")
comTicket.place(x=110, y=40, width=75, height=30)
# 票種旁邊的確認
check_ticket = tk.Button(frame, text="確認", bg="pink",
                         command=get_ticket_type)
check_ticket.place(x=200, y=40, width=60, height=30)


labday1 = tk.Label(frame, text="Day1", justify=tk.RIGHT, width=50)
labday1.place(x=10, y=70, width=100, height=30)

# 結束當日行程按鈕
end_sche = tk.Button(frame, text="結束當日行程", bg="pink",
                     command=end_schedule_2_day2)
end_sche.place(x=110, y=70, width=120, height=30)


labtransport = tk.Label(frame, text="交通工具", justify=tk.RIGHT, width=50)
labtransport.place(x=10, y=100, width=100, height=30)
stdtransport = ("公車", "幹線", "捷運")
comtransport = tt.Combobox(
    frame, width=50, values=stdtransport, state="readonly")
comtransport.place(x=110, y=100, width=75, height=30)
canvas.create_window((600, 1200), window=frame)

# 結束行程的鈕，按下後計算這組的票價，並小心紀錄捷運優惠的資訊！
# 需要記下每次的原價，還有紀錄搭了多少趟，最後要算優惠金
end_this_sche = tk.Button(frame, text="結束行程", bg="pink",
                          command=this_sche1)
end_this_sche.place(x=250, y=70, width=60, height=30)


def checkcmbo():
    """ 按下交通工具確認鈕後會發生的事 """
    global count_transport
    global count_day1
    global sequence_list
    global entsection_day1
    global entdestination_day1
    global entdeparture_day1
    count_transport += 1
    count_day1 += 1

    # 顯示不同的輸入
    if comtransport.get() == "公車" or comtransport.get() == "幹線":
        labsection = tk.Label(
            frame, text="搭乘段數:", justify=tk.RIGHT, width=50)
        labsection.place(
            x=10, y=100+count_transport*30, width=100, height=30)
        varsection_day1[count_day1] = tk.StringVar()
        varsection_day1[count_day1].set("")
        entsection_day1[count_day1] = tk.Entry(
            frame, width=120, textvariable=varsection_day1[count_day1])
        entsection_day1[count_day1].place(
            x=110, y=100+count_transport*30, width=120, height=30)

    elif comtransport.get() == "捷運":
        labdeparture = tk.Label(frame, text="起始站站名:",
                                justify=tk.RIGHT, width=50)
        labdeparture.place(x=10, y=100+count_transport *
                           30, width=100, height=30)
        vardeparture_day1[count_day1] = tk.StringVar()
        vardeparture_day1[count_day1].set("")
        entdeparture_day1[count_day1] = tk.Entry(
            frame, width=120, textvariable=vardeparture_day1[count_day1])
        entdeparture_day1[count_day1].place(x=110, y=100+count_transport *
                                            30, width=120, height=30)

        labdestination = tk.Label(
            frame, text="目的地站名:", justify=tk.RIGHT, width=50)
        labdestination.place(x=210, y=100+count_transport *
                             30, width=100, height=30)
        vardestination_day1[count_day1] = tk.StringVar()
        vardestination_day1[count_day1].set("")
        entdestination_day1[count_day1] = tk.Entry(
            frame, width=120, textvariable=vardestination_day1[count_day1])
        entdestination_day1[count_day1].place(x=310, y=100+count_transport *
                                              30, width=120, height=30)
    # 按下確認後就在交通工具list裡面添加(其他天尚未加上)
    sequence_list.append(comtransport.get())
    print(sequence_list)


# 交通工具的確認
btn = tt.Button(frame, text="確認", command=checkcmbo)
btn.place(x=190, y=100, width=75, height=30)
# 站名確認表(防呆)


def addelements(stationlist):
    """ 把listbox中的東西填滿(站名) """
    for item in stationlist:
        stationlistbox.insert(tk.END, item)


def createlistbox():
    """ 創造站名的listbox """
    stationlistbox.delete(0, tk.END)
    if comLines.get() == "文湖線":
        addelements(BRstations)
    elif comLines.get() == "淡水信義線":
        addelements(Rstations)
    elif comLines.get() == "松山新店線":
        addelements(Gstations)
    elif comLines.get() == "中和新蘆線":
        addelements(Ostations)
    elif comLines.get() == "板南線":
        addelements(BLstations)
    elif comLines.get() == "環狀線":
        addelements(Ystations)


# 各個站
lines = ["文湖線", "淡水信義線", "松山新店線", "中和新蘆線", "板南線", "環狀線"]
# 文湖線站
BRstations = ["南港展覽館", "南港軟體園區", "東湖", "葫洲", "大湖公園",
              "內湖", "文德", "港墘", "西湖", "劍南路", "大直",
              "松山機場", "中山國中", "南京復興", "忠孝復興", "大安",
              "科技大樓", "六張犁", "麟光", "辛亥", "萬芳醫院",
              "萬芳社區", "木柵", "動物園"]
# 紅線
Rstations = ["新北投", "淡水", "紅樹林", "竹圍", "關渡", "忠義",
             "復興崗", "北投", "奇岩", "唭哩岸", "石牌", "明德",
             "芝山", "士林", "劍潭", "圓山", "民權西路", "雙連",
             "中山", "臺北車", "台大醫院", "中正紀念堂", "東門",
             "大安森林公園", "大安", "信義安和", "臺北101／世貿", "象山"]
# 綠線
Gstations = ['松山', '南京三民', '臺北小巨蛋', '南京復興', '松江南京', '中山', '北門',
             '西門', '小南門', '中正紀念堂', '古亭', '台電大樓', '公館', '萬隆', '景美', '大坪林',
             '七張', '新店區公所', '新店', '小碧潭']
# 中和新蘆線
Ostations = ['蘆洲', '三民高中', '徐匯中學', '三和國中', '三重國小', '迴龍', '丹鳳',
             '輔大', '新莊', '頭前庄', '先嗇宮', '三重', '菜寮', '臺北橋', '大橋頭',
             '民權西路', '中山國小', '行天宮', '松江南京', '忠孝新生', '東門', '古亭',
             '頂溪', '永安市場', '景安', '南勢角']
# 板南線
BLstations = ['南港展覽館', '南港', '昆陽', '後山埤', '永春', '市政府', '國父紀念館',
              '忠孝敦化', '忠孝復興', '忠孝新生', '善導寺', '臺北車站', '西門',
              '龍山寺', '江子翠', '新埔', '板橋', '府中', '亞東醫院', '海山',
              '土城', '永寧', '頂埔']
# 環狀線
Ystations = ['新北產業園區站', '幸福站', '頭前庄', '新埔民生', '板橋', '板新', '中原',
             '橋和', '中和', '景安', '景平', '秀朗橋', '十四張', '大坪林']
# 標題
lablines = tk.Label(window, text='各線捷運站名查詢表', justify=tk.RIGHT, width=50)
lablines.place(x=450, y=0, width=140, height=30)
# 哪個線的選單
comLines = tt.Combobox(
    window, width=50, values=lines, state="readonly")
comLines.place(x=450, y=30, width=150, height=30)
# 確認鈕
btnline = tt.Button(window, text="確認", command=createlistbox)
btnline.place(x=600, y=30, width=75, height=30)
# 站名選單
sb = tk.Scrollbar(window)
stationlistbox = tk.Listbox(window, yscrollcommand=sb.set)
stationlistbox.place(x=450, y=60, width=225, height=100)
# 票價位置清除鈕


def clean():
    """ 按下清除鈕後清除票價位置 """
    global varName
    global entName
    varName = tk.StringVar()
    varName.set("")
    entName = tk.Entry(frame, width=120, textvariable=varName)
    entName.place(x=110, y=10, width=120, height=30)


# 清除鈕
btnclear = tt.Button(frame, text="清除", command=clean)
btnclear.place(x=240, y=10, width=75, height=30)


# 計算
window.mainloop()
