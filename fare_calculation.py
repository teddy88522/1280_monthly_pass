import csv
file_input = input()

file = open(file_input, "r", encoding='utf-8')
csvFile = csv.DictReader(file)

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
while weekday <= 7:  # 一週七天
    payment_record_list = list()
    one_day_mrt_fare = 0
    one_day_ticket_fare = 0
    while True:  # 一天有無限組

        add_or_not = input()  # 是否要加組

        if add_or_not == "add":  # 要加的話

            while True:  # 無限組行程
                sequence_list = list()  # 放搭乘工具種類、順序
                trans_type = input()  # 公車、幹線、捷運
                if trans_type == "公車":

                    sections = int(input())  # 段數

                    if trans_type[-1] == "捷運" or trans_type[-1] == "幹線":
                        if sections > 1:
                            first_section_price = bus_fare - difference
                            price = first_section_price + bus_fare * (sections - 1)
                            one_day_ticket_fare += price
                        else:
                            price = discount_bus
                            one_day_ticket_fare += price
                            print(one_day_ticket_fare)
                    else:
                        price = bus_fare
                        one_day_ticket_fare += price
                    sequence_list.append(trans_type)

                elif trans_type == "幹線":
                    sections = int(input())
                    if len(sequence_list) != 0:
                        if sections > 1:
                            first_section_price = bus_fare - difference
                            price = first_section_price + bus_fare * (sections - 1)
                            one_day_ticket_fare += price
                        else:
                            price = discount_bus
                            one_day_ticket_fare += price
                    else:
                        one_day_ticket_fare += bus_fare * sections
                    sequence_list.append(trans_type)

                elif trans_type == "捷運":
                    begin = input()
                    final = input()
                    mrt_fare = count_mrt_fare(begin, final)
                    if sequence_list[-1] == "公車" or sequence_list[-1] == "幹線":
                        new_fare = mrt_fare - difference
                        total_ticket_fare += new_fare
                        one_day_mrt_fare += mrt_fare
                    else:
                        one_day_ticket_fare += mrt_fare
                        one_day_mrt_fare += mrt_fare
                    sequence_list.append(trans_type)
                else:
                    print(one_day_ticket_fare)
                    print(one_day_mrt_fare)
                    break
        else:
            break


    weekday += 1
