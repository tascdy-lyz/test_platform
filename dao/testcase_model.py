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



    @classmethod
    def get_by_filter(cls,**kwargs):
        return  cls.query.filter_by(**kwargs).first()


    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls,case_id,case_title,remark):
        case = cls(case_id=case_id,case_title=case_title,remark=remark)
        db.session.add(case)
        # 提交数据库中
        db.session.commit()
        db.session.close()

    @classmethod
    def update(cls,case_id,case_data):
        cls.query.filter_by(case_id=case_id).update(case_data)

