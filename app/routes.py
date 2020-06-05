# -*- coding: utf-8 -*-
from datetime import datetime
from flask import request, render_template, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import appF, db
from app.forms import LoginForm, RegistrationForm, EditStationForm, EditGoodsForm, EditServicesForm  # IndexForm
from app.models import User, Stations, Services, Goods
from werkzeug.urls import url_parse
from math import ceil


@appF.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@appF.route('/', methods=['GET', 'POST'])
@appF.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    stations = Stations.query.order_by(Stations.id).paginate(page, 30, False)
    next_url = url_for('index', page=stations.next_num) if stations.has_next else None
    prev_url = url_for('index', page=stations.prev_num) if stations.has_prev else None
    #form = IndexForm()
    #if form.validate_on_submit():
    #    flash('A table is updated!')
    #    return redirect(url_for('index'))
    return render_template("index.html", title='Data Page', stations=stations.items, next_url=next_url,
                           prev_url=prev_url)


@appF.route('/station/<int:st_id>', methods=['GET', 'POST'])
@login_required
def station_edit(st_id):
    page = ceil(float(st_id) / 30.0)
    form = EditStationForm()
    station = Stations.query.filter_by(id=st_id).first()
    if form.validate_on_submit():
        station.coordinates = form.coordinates.data
        station.number = form.number.data
        station.address = form.address.data
        db.session.commit()
        flash('Data is updated!')
        return redirect(url_for('index', page=page))
    elif request.method == 'GET':
        form.coordinates.data = station.coordinates
        form.number.data = station.number
        form.address.data = station.address
        form.lnk = url_for('index', page=page)
        form.st_id = st_id
        form.photos = station.photos
        form.goods = station.goods
        form.services = station.services
    return render_template("station_edit.html", form=form)


@appF.route('/services/<int:s_id>', methods=['GET', 'POST'])
@login_required
def service_edit(s_id):
    form = EditServicesForm()
    service = Services.query.filter_by(id=s_id).first()
    st_id = request.args.get('st_id', 1, type=int)
    if form.validate_on_submit():
        service.title = form.title.data
        service.image_url = form.image_url.data
        db.session.commit()
        flash('Data is updated!')
        return redirect(url_for('station_edit', st_id=st_id))
    elif request.method == 'GET':
        form.title.data = service.title
        form.image_url.data = service.image_url
        form.lnk = url_for('station_edit', st_id=st_id)
        form.s_id = s_id
    return render_template("service_edit.html", form=form)


@appF.route('/goods/<int:g_id>', methods=['GET', 'POST'])
@login_required
def product_edit(g_id):
    form = EditGoodsForm()
    product = Goods.query.filter_by(id=g_id).first()
    st_id = product.station_id
    if form.validate_on_submit():
        product.title = form.title.data
        product.amount = form.amount.data
        product.currency = form.currency.data
        product.image_url = form.image_url.data
        db.session.commit()
        flash('Data is updated!')
        return redirect(url_for('station_edit', st_id=st_id))
    elif request.method == 'GET':
        form.title.data = product.title
        form.amount.data = product.amount
        form.currency.data = product.currency
        form.image_url.data = product.image_url
        form.lnk = url_for('station_edit', st_id=st_id)
        form.g_id = g_id
    return render_template("product_edit.html", form=form)


@appF.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@appF.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@appF.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@appF.route('/api/data', methods=['GET'])
@appF.route('/api/data/<int:page>', methods=['GET'])
def get_data(page=0):
    if page == 0:
        stations = Stations.query.all()
    else:
        stations = Stations.query.order_by(Stations.id).paginate(page, 100, False).items
    data_dict = {}
    for station in stations:
        photos = []
        for photo in station.photos:
            photos.append(photo.url)
        services = []
        for service in station.services:
            services.append([service.title, service.image_url])
        goods = {}
        for product in station.goods:
            goods[product.title] = [product.amount, product.currency, product.image_url]
        data_dict[station.id] = {'coordinates': station.coordinates,
                                 'number': station.number,
                                 'address': station.address,
                                 'photos': photos,
                                 'services': services,
                                 'goods': goods
                                 }

    return jsonify(data_dict)


# @appF.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('user.html', user=user)


if __name__ == "__main__":
    stations = Stations.query.order_by(Stations.id).paginate(1, 100, False).items
    print(len(stations))
