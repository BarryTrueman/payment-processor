# payment-processor.py

"""
Payment Processor

A Python module for processing payments.

Usage
--------

    python payment_processor.py [options]

Options
--------

    -h, --help           Display help message
    -t, --test           Test mode
    -p, --process        Process payment
    -v, --version        Display version

"""

import argparse
import logging
import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'payment_processor': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
})

def main():
    parser = argparse.ArgumentParser(description='Payment Processor')
    parser.add_argument('-t', '--test', action='store_true', help='Test mode')
    parser.add_argument('-p', '--process', action='store_true', help='Process payment')
    parser.add_argument('-v', '--version', action='version', version='payment-processor 1.0')

    args = parser.parse_args()

    if args.test:
        logging.info('Running in test mode')
    elif args.process:
        logging.info('Processing payment')
    else:
        parser.print_help()
        return

if __name__ == '__main__':
    main()