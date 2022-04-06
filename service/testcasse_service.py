
'''
    服务层
'''
from Test_pingtai.case_table.log_util import logger
from Test_pingtai.dao.testcase_model import TestCase
from Test_pingtai.server import db


class Testcase:


    def get(self,case_id):
        # 具体业务逻辑层
        if case_id:
            logger.info(f"case_id：{case_id}")
            #result = TestCase.query.filter_by(case_id=case_id).first()

            result = TestCase.get_by_filter(case_id=case_id)
            logger.info(f"结果为：{result}")
            if result:
                datas = [{"case_id": result.case_id,
                          "case_title": result.case_title,
                          "remark": result.remark}]
            else:
                datas = []

        else:
            case_datas = TestCase.get_all()

            datas = [{'Access-Control-Allow-Origin': "*",
                      "case_id": case_data.case_id,
                      "case_title": case_data.case_title,
                      "remark": case_data.remark} for case_data in case_datas]


        return datas


    def post(self,case_id,case_title,remark):
        # 获取json中id值
        case_id = case_id
        # 查询
        exists = TestCase.get_by_filter(case_id=case_id)
        logger.info(f"case_id为{case_id}是否存在,{exists}")
        if not exists:
            TestCase.create(case_id=case_id,case_title=case_title,remark=remark)
            return True
        else:
            return False

    '''
        更新方法
    '''
    def put(self,case_data):

        # 获取json中id值
        case_id = case_data.get("case_id")
        case_data['case_title'] = case_data.get("case_title")
        case_data['remark'] = case_data.get("remark")

        if case_id:
            logger.info(f"case_id：{case_id}")

            exits = TestCase.get_by_filter(case_id=case_id)
            if exits:

                TestCase.query.filter_by(case_id=case_id).update(case_data)
                db.session.commit()
                return True
            else:
                return False