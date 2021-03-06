# -*- coding: utf-8 -*-

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import (generate_password_hash, check_password_hash)

from flask import url_for

from flask_login import (current_user, UserMixin)


db = SQLAlchemy()

jobhunter_job = db.Table(
    'jobhunter_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
)


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_JOBHUNTER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(128), nullable=False)
    phone = db.Column(db.String(18), unique=True, index=True, nullable=True)
    is_enable = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_JOBHUNTER)
    job_intention = db.relationship('Job',
                                secondary=jobhunter_job,
                                backref='users')
    detail = db.relationship("Company", uselist=False)
    #detail = db.relationship("Company")
    # 该处是否可以使用外键
    #company_id = db.Column(db.Integer)
    # 暂时先用简历地址代替简历存储
    #resume_url = db.Column(db.String(64))

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_jobhunter(self):
        return self.role == self.ROLE_JOBHUNTER
    
    @property
    def is_enable_jobs(self):
        if not self.is_company:
            raise AttributeError("User类缺少is_enable_jobs属性")
        return self.jobs.filter(Job.is_enable.is_(True))
    

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))
    user = db.relationship("User", uselist=False, backref=db.backref("company_detail", uselist=False))
    #user = db.relationship("User", backref=db.backref("company_detail", uselist=False))
    website = db.Column(db.String(64), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    logo = db.Column(db.String(256))
    # 融资进度
    finance_stage = db.Column(db.String(128))
    # 公司领域
    field = db.Column(db.String(128))
    # 公司标签
    tags = db.Column(db.String(128))
    # 简介
    description = db.Column(db.String(1024))
    # 详情
    company_info = db.Column(db.Text)

    def __repr__(self):
        return '<Company: {}>'.format(self.name)
    '''
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)
    '''
    @property
    def tag_list(self):
        return self.tags.split(",")


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    salary_low = db.Column(db.Integer)
    salary_high = db.Column(db.Integer)
    # 工作详情页对工作需求的描述 
    #salary_high = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    # 工作待遇 
    treatment = db.Column(db.Text)
    # 经验要求
    exp = db.Column(db.String(64), default="经验不限")
    # 学历要求
    #exp = db.Column(db.String(64), default="经验不限", nullable=False)
    degree = db.Column(db.String(64))
    # 技术栈
    #degree = db.Column(db.String(64), nullable=False)
    stacks = db.Column(db.String(128))
    # 工作地点
    location = db.Column(db.String(24))
    # 全职/兼职
    is_fulltime = db.Column(db.Boolean, default=False)
    # 工作标签
    tags = db.Column(db.String(128))
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company = db.relationship('User', uselist=False, backref=db.backref('jobs', lazy='dynamic'))
    #company = db.relationship('User', backref=db.backref('jobs', lazy='dynamic'))
    # 职位上线
    is_enable = db.Column(db.Boolean, default=True)


    def __repr__(self):
        return '<Job: {}>'.format(self.name)

    @property
    def url(self):
        return url_for('job.detail', course_id = self.id)

    @property
    def stack_list(self):
        return self.stacks.split(",")

    @property
    def tag_list(self):
        return self.tags.split(",")

    @property
    def current_user_is_applied(self):
        delivery = Delivery.query.filter_by(job_id=self.id,
                user_id=current_user.id).first()
        return (delivery is not None)


class Delivery(Base):
    __tablename__ = 'delivery'

    STATUS_WAITTING = 1
    STATUS_REJECT = 2
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    company_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=STATUS_WAITTING)
    company_response = db.Column(db.String(256))

    @property
    def user(self):
        return User.query.get(self.user_id)

    @property
    def job(self):
        return Job.query.get(self.job_id)
