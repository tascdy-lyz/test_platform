'''
    一对多的关系
    Project 为 1 ，plan 为多

    一个项目有很多测试计划
'''
from sqlalchemy import *

from Test_pingtai.server import db


class ProjectModel(db.Model):
    # 固定表明
    __tablename__ = "project"
    # 创建用例ID字段
    id = Column(Integer, primary_key=True)
    # 创建用例case_tile
    name = Column(String(100), nullable=False)



class PlanModel(db.Model):

    # 固定表明
    __tablename__ = "plan"
    # 创建用例ID字段
    id = Column(Integer, primary_key=True)
    # 不允许重复
    name = Column(String(100), nullable=False,unique=True)
    # 通过外键设置一对多表的关联关系
    project_id = Column(Integer,ForeignKey("project.id"))

    projects = db.relationship("ProjectModel",backref="plans")


if __name__ == '__main__':

    #db.create_all()

    # project1 = ProjectModel(id = 1, name= '微信项目')
    # project2 = ProjectModel(id = 2,name = '飞书项目')
    #
    # db.session.add_all([project1,project2])
    # db.session.commit()
    # db.session.close()

    # plan1 = PlanModel(id= 1,name="成员管理",project_id= 1)
    # plan2 = PlanModel(id= 2,name="部门管理",project_id= 1)
    # db.session.add_all([plan1,plan2])
    # db.session.commit()
    # db.session.close()

    #由多插一 ，查询成员管理所对应的什么项目
    plan1 = PlanModel.query.filter_by(id=1).first()
    print(plan1.projects.name)

    #由一查多， 查找出 微信项目所把包含的测试计划
    project1 = ProjectModel.query.filter_by(id=1).first()
    print(project1.plans)
    print(project1.plans[0].name)


    #由一 改多， 通过微信项目将计划表中  id=1的数据name给改掉
    project1 = ProjectModel.query.filter_by(id=1).first()
    project1.plans[0].name = "成员管理2"
    db.session.commit()
    db.session.close()


    #多对多增删查改






