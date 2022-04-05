import yaml
from flask import Flask, request
from flask_restx import Resource, Api, Namespace
from flask_sqlalchemy import SQLAlchemy
# 实例化app 对象
from sqlalchemy import *
from flask_cors import CORS, cross_origin
from Test_pingtai.case_table.log_util import logger

app = Flask(__name__)
CORS(app, resources=r'/*')
api = Api(app)

#创建命名空间，对flask接口进行管理
case_ns = Namespace("case",description="用例管理")

with open("./db.yaml") as f :
    result = yaml.safe_load(f)
    username = result.get("database").get('username')
    password = result.get("database").get('password')
    server = result.get("database").get('server')
    db = result.get("database").get('db')

#
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql+pymysql://{username}:{password}@{server}/{db}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# SQLAlchemy 绑定app
db = SQLAlchemy(app)

# 定义数据库的表 需要继承 db.Model，db 为 app 启动的时的 SQLAlchemy 绑定的实例
class User(db.Model):
    #固定表明
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80))

    def __repr__(self):
        return f"<User {self.username}>"

class TestCase(db.Model):
    #固定表明
    __tablename__ = "testcase"
    #创建用例ID字段
    case_id = Column(Integer, primary_key=True)
    #创建用例case_tile
    case_title = Column(String(100),nullable=False)
    remark = Column(String(100))


'''
    创建
'''
@case_ns.route("/")
@cross_origin()
class TestCaseServer(Resource):
    get_parser = api.parser()
    get_parser.add_argument("case_id", type=int, location="args")
    '''
        查找,
    '''
    @case_ns.expect(get_parser)
    def get(self):
        logger.info(f"request args:{request.args}")
        case_id = request.args.get("case_id")
        if case_id:
            logger.info(f"case_id：{case_id}")
            result = TestCase.query.filter_by(case_id=case_id).first()
            logger.info(f"结果为：{result}")
            if result:
                datas = [{"case_id":result.case_id,
                          "case_title":result.case_title,
                              "remark":result.remark}]
            else:
                datas = []

        else:
            case_datas = TestCase.query.all()
            datas = [ {"case_id":case_data.case_id,
                          "case_title":case_data.case_title,
                              "remark":case_data.remark} for case_data in case_datas]
        #
        return  datas



    """
        这是在定义界面上输入的内容
    """
    api_parser = api.parser()
    api_parser.add_argument("case_id", type=int, required=True, location="json")
    api_parser.add_argument("case_title", type=str, required=True, location="json")
    api_parser.add_argument("remark", type=str, location="json")

    '''
        新增方法-post
    '''
    @case_ns.expect(api_parser)
    def post(self):
        # 输出日志信息
        logger.info(f"reuqest params:{request.json}")

        #获取请求头中的json数据
        case_data = request.json
        #获取json中id值
        case_id = case_data.get("case_id")

        #查询
        result = TestCase.query.filter_by(case_id=case_id).first()
        if result:
            return {"code": 401, "message": "ID已存在"}
        else:
            case = TestCase(**case_data)
            db.session.add(case)
            #提交数据库中
            db.session.commit()

            db.session.close()
            return {"code": 200, "message": "添加成功"}


    update_parser = api.parser()
    update_parser.add_argument("case_id", type=int,required=True,location="json")
    update_parser.add_argument("case_title", type=str, required=True, location="json")
    update_parser.add_argument("remark", type=str, location="json")
    """
        修改方法
    """
    @case_ns.expect(update_parser)
    def put(self):
        logger.info("put method")
        # 获取请求头中的json数据
        case_data = request.json
        # 获取json中id值
        case_id = case_data.get("case_id")
        if case_id:
            logger.info(f"case_id：{case_id}")
            result = TestCase.query.filter_by(case_id=case_id).first()

            if result:

                case_data['case_title'] = case_data.get("case_title")
                case_data['remark'] = case_data.get("remark")
                TestCase.query.filter_by(case_id=case_id).update(case_data)
                db.session.commit()
                return {"code": 200, "message": f"{case_id} success change"}
            else:
                return {"code":4002,"message":"id not found"}



    delete_parser = api.parser()
    delete_parser.add_argument("case_id",type=int,required=True,location="json")
    '''
        删除方法    
    '''
    @case_ns.expect(delete_parser)
    def delete(self):
        logger.info("delete method")
        logger.info(f"reuqest params:{request.json}")

        # 获取请求头中的json数据
        case_data = request.json
        # 获取json中id值
        case_id = case_data.get("case_id")
        if result:
            TestCase.query.filter_by(case_id=case_id).delete()

            #提交数据库中
            db.session.commit()
            db.session.close()
            return {"code": 200, "message": "delete success"}
        else:

            return {"code": 402, "message": "case 不存在"}



api.add_namespace(case_ns,"/testcase")


if __name__ == '__main__' :

    app.run(debug=True,host='127.0.0.1')

    #db.create_all()

    # #实例化一个新的对象
    # user1 = User(username="Lisi")
    # user2 = User(username="王五")
    # #将实例添加到session
    # #db.session.add(user1)
    #
    # #批量添加
    # db.session.add_all([user1,user2])
    #
    # #提交更新
    # db.session.commit()
    # #关闭连接
    # db.session.close()
    # # #查询全部数据
    #
    # print(User.query.all())
    #
    # #条件查询
    # User.query.order_by()


