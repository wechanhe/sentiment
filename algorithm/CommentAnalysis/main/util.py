#!/usr/bin/python 
# -*- coding: UTF-8 -*-

import MySQLdb
import codecs
import sys
import datetime
default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)

conn = None  # db connection

def getCursor():
    global conn
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456',
                           db='test', charset='utf8')
    cursor = conn.cursor()
    return cursor

def read(brand, name, aspect):
    sql = "select * from app1_sentiment " \
          "where name = '%s' and brand = '%s' and aspect = '%s' " % (brand, name, aspect)
    res = []
    try:
        cursor = getCursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            res.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return res
    except:
        if conn != None:
            conn.rowback()
    finally:
        if conn != None:
            conn.close()

def add(record):
    sql = '''insert into app1_result
            (name, brand, aspect, comments, positive, negative, pos_list, neg_list)
            values('%s', '%s', '%s', '%d', '%d', '%d', '%s', '%s')''' \
          % (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])
    try:
        cursor = getCursor()
        cursor.execute(sql)
        conn.commit()
        return True
    except:
        print 'fail to add'
        if conn != None:
            conn.rollback()
        return False
    finally:
        if conn != None:
            conn.close()

def modify(record = ()):
    sql = '''update app1_sentiment 
            set comments = '%d', positive = '%d', negative = '%d' 
            where name = '%s' and brand = '%s' and aspect = '%s' ''' \
          % (record[3], record[4], record[5], record[0], record[1], record[2])
    try:
        cursor = getCursor()
        cursor.execute(sql)
        conn.commit()
        print 'succeed to modify'
    except:
        print 'fail to modify'
        if conn != None:
            conn.rowback()
    finally:
        if conn != None:
            conn.close()

def delete(brand, name, aspect):
    sql = "delete from app1_sentiment " \
          "where name = '%s' and brand = '%s' and aspect = '%s' " % (brand, name, aspect)
    try:
        cursor = getCursor()
        cursor.execute(sql)
        conn.commit()
        print 'succeed to delete'
    except:
        print 'fail to delete'
        if conn != None:
            conn.rowback()
    finally:
        if conn != None:
            conn.close()

# record = ('1','1','1',1, 100, 1, '123', '123')
# add(record)
# delete(record[0], record[1], record[2])
# modify(record)
# res = read(record[0], record[1], record[2])
# for r in res:
#     for i in range(len(r)):
#         print r[i] ,
