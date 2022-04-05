'''
    dao层: 负责与数据库进行交互

'''

# 实例化app 对象
from sqlalchemy import *

from Test_pingtai.server import db


class TestCase(db.Model):
    #固定表明
    __tablename__ = "testcase"
    #创建用例ID字段
    case_id = Column(Integer, primary_key=True)
    #创建用例case_tile
    case_title = Column(String(100),nullable=False)
    remark = Column(String(100))

