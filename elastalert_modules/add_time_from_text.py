import datetime
import re

from elastalert.enhancements import BaseEnhancement


class MyEnhancement(BaseEnhancement):
    def process(self, match):
        current_date = datetime.datetime.now()
        changed_time = current_date

        # Replace firstly the @@time@@ substring by the current time
        match = match.replace("@@time@@", "'" + current_date.strftime(
            "%Y-%m-%dT%H:%M:%S.000Z") + "'")

        # Extract the number of hours we want to add or substract to the current date
        time_changer_value = re.search('(?<=\@\@time(?:\+|\-))(.*?)(?=\@\@)', match)
        if time_changer_value is None:
            return match
        time_changer_value = time_changer_value.group(1)
        print(time_changer_value)

        # Extract the type of operation (+ or -)
        operation_type = re.search('(?<=\@\@time)(.)(?=[0-9])', match)
        if operation_type is None:
            return match
        operation_type = operation_type.group(1)

        print(operation_type)
        if operation_type == '+':
            changed_hours = datetime.timedelta(hours=int(time_changer_value))
            changed_time = current_date + changed_hours
        elif operation_type == '-':
            changed_hours = datetime.timedelta(hours=int(time_changer_value))
            changed_time = current_date - changed_hours
        else:
            return match
        match.replace(
            '@@time' + str(operation_type) + str(time_changer_value) + '@@', "'" + changed_time.strftime("%Y-%m-%dT%H:%M:%S.000Z") + "'")
