import csv
# 讀取捷運價目表
file_input = input()

file = open(file_input, "r", encoding='utf-8')
csvFile = csv.DictReader(file)


# 全票，學生票兩種
ticket_type = input()
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
            fare = row["Adult/Full Fare Tickets"]
    return fare


mrt_trips = 0
accumulated_mrt_fare = 0
total_ticket_fare = 0
weekday = 1
record_day1_fare = 0
record_day2_fare = 0
mrt_trips_day1 = 0
mrt_trips_day2 = 0
while weekday <= 7:  # 一週七天
    payment_record_list = list()
    one_day_mrt_fare = 0
    one_day_ticket_fare = 0
    while True:  # 一天有無限組

        add_or_not = input()  # 是否要加組

        if add_or_not == "add":  # 要加的話

            while True:  # 無限組行程
                sequence_list = list()  # 放該組搭乘工具種類、順序
                trans_type = input()  # 公車、幹線、捷運
                if trans_type == "公車":

                    sections = int(input())  # 段數

                    if sequence_list[-1] == "捷運" or sequence_list[-1] == "幹線":
                        if sections > 1:
                            first_section_price = bus_fare - difference
                            price = first_section_price + bus_fare * (sections - 1)
                            if weekday == 1:
                                record_day1_fare += price
                            elif weekday == 2:
                                record_day2_fare += price
                            else:
                                one_day_ticket_fare += price
                        else:
                            price = discount_bus
                            if weekday == 1:
                                record_day1_fare += price
                            elif weekday == 2:
                                record_day2_fare += price
                            else:
                                one_day_ticket_fare += price
                    else:
                        price = bus_fare
                        if weekday == 1:
                                record_day1_fare += price
                        elif weekday == 2:
                            record_day2_fare += price
                        else:
                            one_day_ticket_fare += price
                    sequence_list.append(trans_type)

                elif trans_type == "幹線":
                    sections = int(input())
                    if len(sequence_list) != 0:
                        if sections > 1:
                            first_section_price = bus_fare - difference
                            price = first_section_price + bus_fare * (sections - 1)
                            if weekday == 1:
                                record_day1_fare += price
                            elif weekday == 2:
                                record_day2_fare += price
                            else:
                                one_day_ticket_fare += price
                        else:
                            price = discount_bus
                            if weekday == 1:
                                record_day1_fare += price
                            elif weekday == 2:
                                record_day2_fare += price
                            else:
                                one_day_ticket_fare += price
                    else:
                        if weekday == 1:
                                record_day1_fare += price
                        elif weekday == 2:
                            record_day2_fare += price
                        else:
                            one_day_ticket_fare += price
                    sequence_list.append(trans_type)

                elif trans_type == "捷運":
                    begin = input()
                    final = input()
                    mrt_fare = count_mrt_fare(begin, final)
                    if weekday == 1:
                        mrt_trips_day1 += 1
                    elif weekday == 2:
                        mrt_trips_day2 += 1
                    else:
                        mrt_trips += 1

                    if sequence_list[-1] == "公車" or sequence_list[-1] == "幹線":
                        new_fare = mrt_fare - difference
                        if weekday == 1:
                            record_day1_fare += new_fare
                            record_day1_fare += mrt_fare
                        elif weekday == 2:
                            record_day2_fare += new_fare
                            record_day2_fare += mrt_fare
                        else:   
                            total_ticket_fare += new_fare
                            one_day_mrt_fare += mrt_fare
                    else:
                        if weekday == 1:
                            record_day1_fare += new_fare
                            record_day1_fare += mrt_fare
                        elif weekday == 2:
                            record_day2_fare += new_fare
                            record_day2_fare += mrt_fare
                        else:   
                            total_ticket_fare += new_fare
                            one_day_mrt_fare += mrt_fare
                    sequence_list.append(trans_type)
                else:
                    break
            accumulated_mrt_fare += one_day_mrt_fare
            total_ticket_fare += one_day_ticket_fare
        else:
            break


    weekday += 1

mrt_trips = mrt_trips * (4) + mrt_trips_day1 + mrt_trips_day2 
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
total_expense = (accumulated_mrt_fare + total_ticket_fare)*(4) + record_day1_fare + record_day2_fare
discount_money = total_expense*discount
total_expense = total_expense - discount_money

if total_expense < 1280:
    print("your monthly expense is" + str(total_expense) + "don't buy $1280 !")
elif total_expense == 1280:
    print("your monthly expense is" + str(total_expense) + "whatever is fine !")
elif total_expense > 1280:
    print("your monthly expense is" + str(total_expense) + "buy 1280 ! save money !")


