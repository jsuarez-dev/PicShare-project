"""Utils functional test"""
# files
import csv


def get_username_and_password(num):
    if 0 < num < 6:
        with open('functional_test/fixtures/user_info.csv', 'r') as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if count == num:
                    username = row[0]
                    password = row[1]
                    return username, password
                else:
                    count += 1
    else:
        return None, None
