import csv
# 讀取捷運價目表
file_input = input("Please enter the location of ticket fare table: ")

file = open(file_input, "r", encoding='utf-8')
csvFile = csv.DictReader(file)


# 全票，學生票兩種
ticket_type = input("Please enter the ticket type: 全票/學生票")
if ticket_type == "全票":
    bus_fare = 15
    discount_bus = 7
    difference = bus_fare - discount_bus
else:
    bus_fare = 12
    discount_bus = 6
    difference = bus_fare - discount_bus


def count_mrt_fare(begin, final):
    for row in csvFile:
        if row["Departure_Station"] == begin and row["Destination_Station"] == final:
            fare = int(row["Adult/Full Fare Tickets"])
            return fare
        else:
            continue


weekday = 1  # 以第一天為起始
mrt_trips = 0  # 7天搭了幾趟捷運
accumulated_mrt_fare = 0  # 7天常客優惠的計算金額
total_ticket_fare = 0  # 7天現金花費
day1_day2_fare = 0  # 第一、二天的總金額
day1_day2_mrt_trips = 0  # 第一、二天捷運趟數
day1_day2_mrt_fare = 0  # 第一、二天常客優惠的錢

while weekday <= 7:  # 一週七天

    print("現在是第" + str(weekday) + "天")
    one_day_mrt_fare = 0  # 一天計算常客優惠的錢
    one_day_ticket_fare = 0  # 一天實際現金花費
    one_day_mrt_trips = 0  # 一天搭了幾次捷運

    while True:  # 一天有無限組

        add_or_not = input("請問是否要加組，y/n")

        if add_or_not == "y":  # 要加的話

            sequence_list = list()  # 放該組搭乘工具種類、順序

            while True:  # 無限組行程

                trans_type = input("請輸入交通工具，公車/幹線/捷運：")

                if trans_type == "公車":

                    sections = int(input("請輸入公車「段數」"))

                    if (len(sequence_list) > 0) and (sequence_list[-1] == "捷運" or sequence_list[-1] == "幹線"):
                        # 如果已經搭過別的交通工具，且是可以有折扣的

                        if sections > 1:  # 若段數超過一段
                            price = discount_bus + bus_fare * (sections - 1)
                            one_day_ticket_fare += price

                        else:  # 只有一段
                            price = discount_bus
                            one_day_ticket_fare += price

                    else:  # 如果沒搭過別的交通工具或前一個無法有折扣
                        one_day_ticket_fare += bus_fare * sections

                    sequence_list.append(trans_type)

                elif trans_type == "幹線":

                    sections = int(input("請輸入公車「段數」"))

                    if len(sequence_list) != 0:  # 如果前面搭過任何交通工具，都能享有優惠

                        if sections > 1:  # 搭超過一段
                            price = discount_bus + bus_fare * (sections - 1)
                            one_day_ticket_fare += price

                        else:  # 搭一段而已
                            one_day_ticket_fare += discount_bus

                    else:  # 若沒搭過別的交通工具
                        one_day_ticket_fare += bus_fare * sections

                    sequence_list.append(trans_type)

                elif trans_type == "捷運":
                    begin_station = input("請輸入上車站名")
                    final_station = input("請輸入下車站名")
                    mrt_fare = count_mrt_fare(begin_station, final_station)
                    one_day_mrt_trips += 1
                    print(mrt_fare)

                    if (len(sequence_list) > 0) and (sequence_list[-1] == "公車" or sequence_list[-1] == "幹線"):
                        new_fare = mrt_fare - difference
                        one_day_ticket_fare += new_fare
                        one_day_mrt_fare += mrt_fare
                    else:
                        one_day_ticket_fare += mrt_fare
                        one_day_mrt_fare += mrt_fare
                    sequence_list.append(trans_type)
                else:
                    break

        else:
            if weekday == 1 or weekday == 2:
                day1_day2_fare += one_day_ticket_fare
                day1_day2_mrt_trips += one_day_mrt_trips
                day1_day2_mrt_fare += one_day_mrt_fare

            total_ticket_fare += one_day_ticket_fare
            accumulated_mrt_fare += one_day_mrt_fare
            mrt_trips += one_day_mrt_trips
            break

    weekday += 1

mrt_trips = mrt_trips * 4 + day1_day2_mrt_trips
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

# 比較一個月花費跟1280
actual_mrt_fare = accumulated_mrt_fare * 4 + day1_day2_mrt_fare
discount_money = actual_mrt_fare * discount
total_expense = total_ticket_fare * 4 + day1_day2_fare - discount_money

if total_expense < 1280:
    print("Your monthly expense is: " + str(total_expense) + ". Don't buy $1280!")
elif total_expense == 1280:
    print("Your monthly expense is: " + str(total_expense) + ". Whatever is fine!")
elif total_expense > 1280:
    print("Your monthly expense is: " + str(total_expense) + ". Buy 1280! Save money!")
