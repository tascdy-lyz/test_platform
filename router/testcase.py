'''
    路由层

'''
from flask import request
from flask_restx import Namespace, Resource
from Test_pingtai.case_table.log_util import logger
from Test_pingtai.server import api, db
from Test_pingtai.service.testcasse_service import Testcase

case_ns = Namespace("case", description="用例管理")


@case_ns.route("/")
class TestCaseServer(Resource):

    get_parser = api.parser()
    get_parser.add_argument("case_id", type=int, location="args")
    '''
        查找,
    '''
    @case_ns.expect(get_parser)
    def get(self):
        logger.info(f"request header {request.headers}")
        logger.info("get method")
        logger.info(f"request args:{request.args}")
        case_id = request.args.get("case_id")

        #调用service层的具体业务逻辑
        testcase = Testcase()
        datas = testcase.get(case_id)
        #响应内容
        return datas



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
        logger.info("post method")
        logger.info(f"request params:{request.json}")

        # 获取请求头中的json数据
        case_data = request.json
        case_id = case_data.get("case_id")
        case_title = case_data.get("case_title")
        remark = case_data.get("remark")
        testcase = Testcase()
        datas = testcase.post(case_id=case_id,case_title=case_title,remark=remark)
        if datas:
            return {"code": 200, "message": "添加成功"}
        else:
            return {"code": 401, "message": "ID已存在"}



    update_parser = api.parser()
    update_parser.add_argument("case_id", type=int, required=True, location="json")
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
        logger.info(f"request params:{request.json}")
        testcase = Testcase()
        exits = testcase.put(case_data)
        if exits:
            return {"code": 200, "message": f"{case_data.get('case_id')} success change"}
        else:
            return {"code": 4002, "message": "id not found"}




    delete_parser = api.parser()
    delete_parser.add_argument("case_id", type=int, required=True, location="json")
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

        if case_id:
            TestCase.query.filter_by(case_id=case_id).delete()

            # 提交数据库中
            db.session.commit()
            db.session.close()
            return {"code": 200, "message": "delete success"}
        else:

            return {"code": 402, "message": "case 不存在"}
