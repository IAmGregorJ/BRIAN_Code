'''imports'''
import logging

logger = logging
logger.basicConfig(filename = 'BRIAN_log.log',
                    format='%(asctime)s: %(levelname)s - %(pathname)s: '
                            '%(message)s', level=logging.INFO)
