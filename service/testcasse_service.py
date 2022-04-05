
'''
    服务层
'''
from Test_pingtai.case_table.log_util import logger
from Test_pingtai.dao.testcase_model import TestCase


class Testcase:


    def get(self,case_id):
        # 具体业务逻辑层
        if case_id:
            logger.info(f"case_id：{case_id}")
            result = TestCase.query.filter_by(case_id=case_id).first()
            logger.info(f"结果为：{result}")
            if result:
                datas = [{"case_id": result.case_id,
                          "case_title": result.case_title,
                          "remark": result.remark}]
            else:
                datas = []

        else:
            case_datas = TestCase.query.all()

            datas = [{'Access-Control-Allow-Origin': "*",
                      "case_id": case_data.case_id,
                      "case_title": case_data.case_title,
                      "remark": case_data.remark} for case_data in case_datas]


        return datas