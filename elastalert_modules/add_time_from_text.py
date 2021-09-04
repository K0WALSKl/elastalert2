import datetime

from elastalert.enhancements import BaseEnhancement


class addTimeFromText(BaseEnhancement):
    def process(self, match):
        current_date = datetime.datetime.now()
        changed_time = current_date

        if '{1}' in self.rule['alert_text']:
            changed_hours = datetime.timedelta(hours=1)
            changed_time = current_date - changed_hours
            match['@version'] = "'" + changed_time.strftime("%Y-%m-%dT%H:%M:%S.000Z") + "'"
            self.rule['alert_text'].replace('{1}', "'" + changed_time.strftime("%Y-%m-%dT%H:%M:%S.000Z") + "'")

        if '{2}' in self.rule['alert_text']:
            self.rule['alert_text'].replace('{2}', "'" + current_date.strftime("%Y-%m-%dT%H:%M:%S.000Z") + "'")
