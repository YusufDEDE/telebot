import requests
from logging import Handler, Formatter
import logging
import datetime

def sendAuto_message(tchatID, message):
    TELEGRAM_TOKEN = '970406731:AAGRJVcUeDSnWZP39x70jRdcfvlmECVLHNQ'
    TELEGRAM_CHAT_ID = tchatID

    class RequestsHandler(Handler):
        def emit(self, record):
            log_entry = self.format(record)
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': log_entry,
                'parse_mode': 'HTML'
            }
            return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
                                data=payload).content

    class LogstashFormatter(Formatter):
        def __init__(self):
            super(LogstashFormatter, self).__init__()

        def format(self, record):
            t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)



    logger = logging.getLogger('trymeApp')
    logger.setLevel(logging.WARNING)

    handler = RequestsHandler()
    formatter = LogstashFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(logging.WARNING)

    logger.error(message)

    print(TELEGRAM_CHAT_ID)
