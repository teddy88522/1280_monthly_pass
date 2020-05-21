ticket_type = input()
if ticket_type == "全票":
    bus_fare = 15
    discount_bus = 7
else:
    bus_fare = 12
    discount_bus = 6

mrt_trips = 0
accumulated_mrt_fare = 0
total_ticket_fare = 0
weekday = 1
while weekday <= 7:  # 一週七天
    while True:  #

        trans_type = input()
        if trans_type == "公車":
            sections = int(input())



    weekday += 1