ticket_type = input()
if ticket_type == "全票":
    bus_fare = 15
    discount_bus = 7
    difference = bus_fare - discount_bus
else:
    bus_fare = 12
    discount_bus = 6
    difference = bus_fare - discount_bus

mrt_trips = 0
accumulated_mrt_fare = 0
total_ticket_fare = 0
weekday = 1
while weekday <= 7:  # 一週七天
    while True:  # 無限組行程
        sequence_list = list()
        trans_type = input()  # 公車、幹線、捷運
        if trans_type == "公車":
            sections = int(input())
            sequence_list.append(trans_type)
            if trans_type[-1] == "捷運" or trans_type[-1] == "幹線":
                if sections >= 1:
                    price = bus_fare - difference




    weekday += 1