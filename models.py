from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "tblusers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, unique=True)
    email = db.Column(db.String(150), index=True, unique=True)
    password = db.Column(db.String(255), index=True, unique=True)


class Regions(db.Model):
    __tablename__ = 'regions'
    regions_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Cities(db.Model):
    __tablename__ = 'cities'
    cities_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    regions_regions_id = db.Column(db.Integer, db.ForeignKey('regions.regions_id'), nullable=False)
    region = db.relationship('Regions', backref='cities')


class Locations(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(45), nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    cities_cities_id = db.Column(db.Integer, db.ForeignKey('cities.cities_id'), nullable=False)
    city = db.relationship('Cities', backref='locations')


class Users(db.Model):
    __tablename__ = 'users'
    users_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    names = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    phone_number = db.Column(db.String(45), nullable=False)
    location_location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    location = db.relationship('Locations', backref='users')


class Trips(db.Model):
    __tablename__ = 'trips'
    trip_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(45), nullable=True)
    end_time = db.Column(db.String(45), nullable=True)
    route = db.Column(db.String(45), nullable=True)


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=True)
    users_users_id = db.Column(db.Integer, db.ForeignKey('users.users_id'), nullable=False)
    trips_trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'), nullable=False)
    user = db.relationship('Users', backref='orders')
    trip = db.relationship('Trips', backref='orders')


class Seats(db.Model):
    __tablename__ = 'seats'
    seats_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)


class Cars(db.Model):
    __tablename__ = 'cars'
    cars_id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(45), nullable=False)
    model = db.Column(db.String(45), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    seats_seat_id = db.Column(db.Integer, db.ForeignKey('seats.seats_id'), nullable=False)
    seat = db.relationship('Seats', backref='cars')


class Vans(db.Model):
    __tablename__ = 'vans'
    vans_id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(45), nullable=False)
    model = db.Column(db.String(45), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    seats_seats_id = db.Column(db.Integer, db.ForeignKey('seats.seats_id'), nullable=False)
    seat = db.relationship('Seats', backref='vans')


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    vehicles_id = db.Column(db.Integer, primary_key=True)
    type_index = db.Column(db.String(45), nullable=False)
    colour = db.Column(db.String(45), nullable=False)
    number_index = db.Column(db.String(45), nullable=False)
    cars_cars_id = db.Column(db.Integer, db.ForeignKey('cars.cars_id'), nullable=False)
    vans_vans_id = db.Column(db.Integer, db.ForeignKey('vans.vans_id'), nullable=False)
    car = db.relationship('Cars', backref='vehicles')
    van = db.relationship('Vans', backref='vehicles')


class Drivers(db.Model):
    __tablename__ = 'drivers'
    drivers_id = db.Column(db.Integer, primary_key=True)
    vehicle_numbers = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    order_order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    location_location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    vehicles_vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.vehicles_id'), nullable=False)
    location = db.relationship('Locations', backref='drivers')
    vehicle = db.relationship('Vehicles', backref='drivers')
    orders = db.relationship('Orders', backref='driver')

class Rating(db.Model):
    __tablename__ = 'rating'
    orders_order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    drivers_drivers_id = db.Column(db.Integer, db.ForeignKey('drivers.drivers_id'), primary_key=True)
    stars_number = db.Column(db.String(5), nullable=True)
    order = db.relationship('Orders', backref='rating')
    driver = db.relationship('Drivers', backref='rating')
