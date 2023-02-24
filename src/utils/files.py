file_schema = ('id', 'card_id', 'merchant', 'mcc', 'currency', 'amount', 'sgd_amount',
               'transaction_id', 'transaction_date', 'card_pan', 'card_type')


def is_valid_file_schema(file):
    file_data = file.readline().decode("utf-8")
    fields = file_data.rstrip("\n").replace('\"', '').split(",")
    for field in fields:
        if field not in file_schema:
            return False
    return True
