

class ChoiceInfo():
    # Condition choices
    PLUS = 'P'
    MINUS = 'M'
    CONDITION_CHOICES = [
        (PLUS, 'Plus'),
        (MINUS, 'Minus'),
    ]
    CONDITIONS = dict(CONDITION_CHOICES)

    # Gender choices
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    GENDERS = dict(GENDER_CHOICES)

    # Order choices
    BUY = 'B'
    SELL = 'S'
    ORDER_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]
    ORDERS = dict(ORDER_CHOICES)

    # Position choices
    LONG = 'L'
    SHORT = 'S'
    POSITION_CHOICES = [
        (LONG, 'Long'),
        (SHORT, 'Short'),
    ]
    POSITIONS = dict(POSITION_CHOICES)
    
    # Status choices
    OPEN = 'O'
    CLOSE = 'C'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSE, 'Close'),
    ]
    STATUSES = dict(STATUS_CHOICES)
