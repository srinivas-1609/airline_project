class Flight:
    def __init__(self, flight_number, airline, source, destination, flight_date, dep_time, arr_time, total_seats, available_seats, price):
        self.flight_number = flight_number
        self.airline = airline
        self.source = source
        self.destination = destination
        self.flight_date = flight_date
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.price = price

    def __str__(self):
        return f"{self.flight_number} | {self.airline} | {self.source} -> {self.destination} | Seats: {self.available_seats}/{self.total_seats}"