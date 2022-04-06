import yaml
from flask import Flask
from flask_restx import  Api

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
api = Api(app)

# with open("case_table/db.yaml") as f :
#     result = yaml.safe_load(f)
#     username = result.get("database").get('username')
#     password = result.get("database").get('password')
#     server = result.get("database").get('server')
#     db = result.get("database").get('db')
username = 'root'
password = '123456'
server = '127.0.0.1:3306'
db = 'test'
#
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql+pymysql://{username}:{password}@{server}/{db}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# SQLAlchemy 绑定app
db = SQLAlchemy(app)

#由于有循环导入，
def get_router():
    from Test_pingtai.router.testcase import case_ns
    api.add_namespace(case_ns, "/testcase")

if __name__ == '__main__' :
    get_router()
    app.run(debug=True)
