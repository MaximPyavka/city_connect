import logging
import logging.config

from flask import render_template

from city_connect.config import LOGGING
from city_connect.views.base_view import BaseMethodView

logging.config.dictConfig(LOGGING)


class Index(BaseMethodView):

    def get(self):
        logging.debug('Get.Index template.')
        return render_template('index.html')
