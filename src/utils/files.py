spend_file_schema = ('id', 'card_id', 'merchant', 'mcc', 'currency', 'amount',
                     'transaction_id', 'transaction_date', 'card_pan', 'card_type')

user_file_schema = ('id', 'first_name', 'last_name', 'phone', 'email', 'created_at', 'updated_at',
                    'card_id', 'card_pan', 'card_type')

file_schema = {
    "spend": spend_file_schema,
    "user": user_file_schema
}


def is_valid_file_schema(file, file_type):
    last_pos = file.tell()
    file_data = file.readline().decode("utf-8")
    file.seek(last_pos) # return pointer to header row
    fields = file_data.rstrip("\r\n").replace('\"', '').split(",")
    for field in fields:
        if field not in file_schema[file_type]:
            return False
    return True
