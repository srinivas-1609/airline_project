class Passenger:
    def __init__(self, user_id, username, name, email, phone, role):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role # 'admin' or 'passenger'

    def __str__(self):
        return f"{self.name} ({self.username}) - {self.role.upper()}"