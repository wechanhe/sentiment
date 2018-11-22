#!/usr/bin/python 
# -*- coding: UTF-8 -*-

import MySQLdb
import codecs
import sys
import datetime
default_encoding = "utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)

conn = None  # db connection

def getCursor():
    global conn
    conn = MySQLdb.connect(host="10.92.33.136", user="root", passwd="tcl@123",
                           db="scrapy_data", charset="utf8")
    cursor = conn.cursor()
    return cursor

def getDataset():
    comment = []
    rating = []
    sql = "select advantage, disadvantage, summary, content, total from evaluate_item"
    try:
        cursor = getCursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            text = ''
            if row[4] != None:
                if row[0] != None:
                    text += codecs.encode(row[0], 'utf-8')
                if row[1] != None:
                    text += codecs.encode(row[1], 'utf-8')
                if row[2] != None:
                    text += codecs.encode(row[2], 'utf-8')
                # if row[3] != None:
                #     text += codecs.encode(row[3], 'utf-8')
                if text != '':
                    comment.append(text)
                    rating.append(row[4])
        print len(comment), len(rating)
        return comment, rating
    except():
        pass
    finally:
        if conn != None:
            conn.close()

def read_db():
    advantage = []
    disadvantage = []
    sql = "select distinct advantage, disadvantage from evaluate_item"
    try:
        start = datetime.datetime.now()
        cursor = getCursor()
        print 'loading data...'
        cursor.execute(sql)
        end = datetime.datetime.now()
        print 'load data finished, it takes', (end - start).seconds, 'seconds'
        for row in cursor.fetchall():
            if row[0] is not None:
                advantage.append(codecs.encode(str(row[0]), 'utf-8'))
            if row[1] is not None:
                disadvantage.append(codecs.encode(row[1], 'utf-8'))
        return advantage, disadvantage
    except():
        pass
    finally:
        if conn != None:
            conn.close()

# 数据写入到本地
def saveData():
    advantage, disadvantage = read_db()
    adv_path = '/local/TextClassification/advantage.txt'
    dis_path = '/local/TextClassification/disadvantage.txt'
    try:
        with open(adv_path, 'w') as adv_file:
            for i in range(len(advantage)):
                adv_file.write(advantage[i]+"\n")
        with open(dis_path, 'w') as dis_file:
            for i in range(len(disadvantage)):
                dis_file.write(disadvantage[i]+"\n")
    except:
        print 'write error'

# 从本地文件读取数据集
def readData():
    advantage = []
    disadvantage = []
    adv_path = '/local/TextClassification/advantage.txt'
    dis_path = '/local/TextClassification/disadvantage.txt'
    try:
        with open(adv_path, 'r') as adv_file:
            lines = adv_file.readlines()
            for line in lines:
                advantage.append(line)
        with open(dis_path, 'r') as dis_file:
            lines = dis_file.readlines()
            for line in lines:
                disadvantage.append(line)
        print 'file:', len(advantage), len(disadvantage)
        return advantage, disadvantage
    except:
        print 'read error'

def read_rawdata():
    sql = """select distinct m.name, m.brand, e.advantage, e.disadvantage
            from mobile m, evaluate_item e
            where m.id = e.mobile_id"""
    rawdata = []
    try:
        start = datetime.datetime.now()
        cursor = getCursor()
        print 'loading data...'
        cursor.execute(sql)
        end = datetime.datetime.now()
        print 'load data finished, it takes', (end - start).seconds, 'seconds'
        for row in cursor.fetchall():
            if row[2] != None or row[3] != None:
                name = ''
                brand = ''
                advantage = ''
                disadvantage = ''
                if row[0] != None:
                    name = codecs.encode(row[0], 'utf-8')
                if row[1] != None:
                    brand = codecs.encode(row[1], 'utf-8')
                if row[2] != None:
                    advantage = codecs.encode(row[2], 'utf-8')
                if row[3] != None:
                    disadvantage = codecs.encode(row[3], 'utf-8')
                rawdata.append((name, brand, advantage, disadvantage))
        print len(rawdata)
        return rawdata
    except():
        pass
    finally:
        if conn != None:
            conn.close()
