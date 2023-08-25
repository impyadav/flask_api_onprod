"""
# -*- coding: utf-8 -*-

Created on Aug 2023
@author: Prateek Yadav

"""
from src.app import app as flaskApplication

if __name__ == '__main__':
    flaskApplication.run(host='0.0.0.0', port=8989)