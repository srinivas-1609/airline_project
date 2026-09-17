class Booking:
    def __init__(self, booking_id, user_id, flight_number, status, booking_date):
        self.booking_id = booking_id
        self.user_id = user_id
        self.flight_number = flight_number
        self.status = status # 'CONFIRMED' or 'CANCELLED'
        self.booking_date = booking_date

    def __str__(self):
        return f"Booking [{self.booking_id}] - User: {self.user_id} - Flight: {self.flight_number} - {self.status}"