import os
import json
from random import randint
from faker import Faker
from simplejob.models import db, User, Company, Job

faker = Faker('zh-CN')  # 创建 faker 工厂对象，生成一个用于测试数据的库

user = User(
    username='Shiyanlou',
    password='shiyanlou',
    phone='12012134999',
    email='shiyanlou@qq.com',
    role=30,
)

with open(os.path.join(os.getcwd(), 'datas', 'job.json')) as f:
    jobs = json.load(f)

def iter_companys():
    for i in jobs:
        yield Company(
            #logo = company['logo'],
            #company_name = company['company_name'],
            #offical_websit = company['offical_websit'],
            #industry = company['industry'],
            #stage = company['stage'],
            #city = company['city']
            name = i['company'],
            email = faker.email(),
            website = faker.uri(),
            user = user,
            address = faker.address()
        )

companys = list(iter_companys())

def iter_jobs():
    for i, job in enumerate(jobs):
        yield Job(
            #job_name = job['jobname'],
            #wage_area = job['wage_area'],
            #working_address = job['working_address'],
            #experience_required = job['experience'],
            #edu_required = job['education'],
            #release_date = job['release_date']
            name = job['name'],
            #salary = job['salary'],
            #address = job['address'],
            company = user
            )

def run():
    db.session.add(user)
    for company in companys:
        db.session.add(company)
    for job in iter_jobs():
        db.session.add(job)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
