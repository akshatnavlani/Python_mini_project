import random
def trans_id():
    random_number = random.randint(10000,99999)
    cursor.execute(SELECT transaction_id FROM expenses)
    if random_number not in transaction_id:
        return random_number
    else:
        trans_id()