from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from models import db, Cities, Regions, Locations, Users, Trips, Orders, Seats, Cars, Vans, Vehicles, Drivers, Rating

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:13012005@localhost/lab1'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

CORS(app, supports_credentials=True)

db.init_app(app)

with app.app_context():
    db.create_all()

ma = Marshmallow(app)


class RegionsSchema(ma.Schema):
    class Meta:
        fields = ('regions_id', 'name')

    cities = ma.Nested('CitiesSchema', many=True, exclude=('regions_regions_id',))


class CitiesSchema(ma.Schema):
    class Meta:
        fields = ('cities_id', 'name', 'regions_regions_id')

    locations = ma.Nested('LocationsSchema', many=True, exclude=('cities_cities_id',))
    region = ma.Nested('RegionsSchema', exclude=('cities',))


class LocationsSchema(ma.Schema):
    class Meta:
        fields = ('location_id', 'street_name', 'street_number', 'cities_cities_id')


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('users_id', 'number', 'names', 'surname', 'phone_number', 'location_location_id')


class TripsSchema(ma.Schema):
    class Meta:
        fields = ('trip_id', 'start_time', 'end_time', 'route')


class OrdersSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'number', 'price', 'users_users_id', 'trips_trip_id')


class SeatsSchema(ma.Schema):
    class Meta:
        fields = ('seats_id', 'number')


class CarsSchema(ma.Schema):
    class Meta:
        fields = ('cars_id', 'brand', 'model', 'year', 'seats_seat_id')


class VansSchema(ma.Schema):
    class Meta:
        fields = ('vans_id', 'brand', 'model', 'year', 'seats_seats_id')


class VehiclesSchema(ma.Schema):
    class Meta:
        fields = ('vehicles_id', 'type_index', 'colour', 'number_index', 'cars_cars_id', 'vans_vans_id')


class DriversSchema(ma.Schema):
    class Meta:
        fields = ('drivers_id', 'vehicle_numbers', 'name', 'surname', 'order_order_id', 'location_location_id',
                  'vehicles_vehicles_id')


class RatingSchema(ma.Schema):
    class Meta:
        fields = ('orders_order_id', 'drivers_drivers_id', 'stars_number')


@app.route('/all_related_data', methods=['GET'])
def all_related_data():
    all_regions = Regions.query.all()
    regions_cities = {}
    for region in all_regions:
        cities = [city.name for city in region.cities]
        regions_cities[region.name] = cities

    all_cities = Cities.query.all()
    cities_locations = {}
    for city in all_cities:
        locations = [(location.street_name, location.street_number) for location in city.locations]
        cities_locations[city.name] = locations

    all_users = Users.query.all()
    users_orders = {}
    for user in all_users:
        orders = [order.number for order in user.orders]
        users_orders[user.names] = orders

    all_trips = Trips.query.all()
    trips_orders = {}
    for trip in all_trips:
        orders = [order.number for order in trip.orders]
        trips_orders[trip.start_time] = orders

    all_seats = Seats.query.all()
    seats_cars = {}
    for seat in all_seats:
        cars = [(car.brand, car.model) for car in seat.cars]
        seats_cars[seat.number] = cars

    all_cars = Cars.query.all()
    cars_vehicles = {}
    for car in all_cars:
        vehicles = [(vehicle.type_index, vehicle.colour) for vehicle in car.vehicles]
        cars_vehicles[car.brand] = vehicles

    all_vans = Vans.query.all()
    vans_vehicles = {}
    for van in all_vans:
        vehicles = [(vehicle.type_index, vehicle.colour) for vehicle in van.vehicles]
        vans_vehicles[van.brand] = vehicles

    all_drivers = Drivers.query.all()
    drivers_orders = {}
    for driver in all_drivers:
        orders_info = [(order.stars_number, driver.name, order.orders_order_id) for order in driver.rating]
        for rating, name, order_id in orders_info:
            if rating not in drivers_orders:
                drivers_orders[rating] = []
            drivers_orders[rating].append((name, order_id))

    return jsonify({
        "regions_cities": regions_cities,
        "cities_locations": cities_locations,
        "users_orders": users_orders,
        "trips_orders": trips_orders,
        "seats_cars": seats_cars,
        "cars_vehicles": cars_vehicles,
        "vans_vehicles": vans_vehicles,
        "drivers_order": drivers_orders,
    })


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


region_schema = RegionsSchema()
regions_schema = RegionsSchema(many=True)


@app.route('/regions', methods=['GET'])
def list_regions():
    all_regions = Regions.query.all()
    results = regions_schema.dump(all_regions)
    return jsonify(results)


@app.route('/regiondetails/<id>', methods=['GET'])
def region_details(id):
    region = Regions.query.get(id)
    return region_schema.jsonify(region)


@app.route('/regionupdate/<id>', methods=['PUT'])
def region_update(id):
    region = Regions.query.get(id)
    name = request.json['name']
    region.name = name
    db.session.commit()
    return region_schema.jsonify(region)


@app.route('/regiondelete/<id>', methods=['DELETE'])
def region_delete(id):
    region = Regions.query.get(id)
    db.session.delete(region)
    db.session.commit()
    return region_schema.jsonify(region)


@app.route('/newregion', methods=['POST'])
def new_region():
    name = request.json['name']
    regions_id = request.json['regions_id']
    new_region = Regions(name=name, regions_id=regions_id)

    db.session.add(new_region)
    db.session.commit()

    return jsonify({'message': 'New region created successfully'})


city_schema = CitiesSchema()
cities_schema = CitiesSchema(many=True)


@app.route('/cities', methods=['GET'])
def list_cities():
    all_cities = Cities.query.all()
    results = cities_schema.dump(all_cities)
    return jsonify(results)


@app.route('/citydetails/<id>', methods=['GET'])
def city_details(id):
    city = Cities.query.get(id)
    return city_schema.jsonify(city)


@app.route('/cityupdate/<id>', methods=['PUT'])
def city_update(id):
    city = Cities.query.get(id)

    name = request.json['name']
    regions_id = request.json['regions_regions_id']

    city.name = name
    city.regions_regions_id = regions_id

    db.session.commit()
    return city_schema.jsonify(city)


@app.route('/citydelete/<id>', methods=['DELETE'])
def city_delete(id):
    city = Cities.query.get(id)

    if city:
        locations = Locations.query.filter_by(cities_cities_id=id).all()
        for location in locations:
            location.cities_cities_id = None

        db.session.delete(city)
        db.session.commit()
        return jsonify({'message': f'City with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'City not found'}), 404


@app.route('/newcity', methods=['POST'])
def new_city():
    name = request.json['name']
    regions_id = request.json['regions_regions_id']

    new_city = Cities(name=name, regions_regions_id=regions_id)
    db.session.add(new_city)
    db.session.commit()

    return city_schema.jsonify(new_city)


location_schema = LocationsSchema()
locations_schema = LocationsSchema(many=True)


@app.route('/locations', methods=['GET'])
def list_locations():
    all_locations = Locations.query.all()
    results = locations_schema.dump(all_locations)
    return jsonify(results)


@app.route('/locationdetails/<id>', methods=['GET'])
def location_details(id):
    location = Locations.query.get(id)
    return location_schema.jsonify(location)


@app.route('/locationupdate/<id>', methods=['PUT'])
def location_update(id):
    location = Locations.query.get(id)

    street_name = request.json['street_name']
    street_number = request.json['street_number']
    city_id = request.json['city_id']

    location.street_name = street_name
    location.street_number = street_number
    location.cities_cities_id = city_id

    db.session.commit()
    return location_schema.jsonify(location)


@app.route('/locationdelete/<id>', methods=['DELETE'])
def location_delete(id):
    location = Locations.query.get(id)

    if location:
        users_with_location = Users.query.filter_by(location_location_id=id).all()
        for user in users_with_location:
            user.location_location_id = None

        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': f'Location with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Location not found'}), 404


@app.route('/newlocation', methods=['POST'])
def new_location():
    street_name = request.json['street_name']
    street_number = request.json['street_number']
    city_id = request.json['city_id']

    location = Locations(street_name=street_name, street_number=street_number, cities_cities_id=city_id)

    db.session.add(location)
    db.session.commit()
    return location_schema.jsonify(location)


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


@app.route('/users', methods=['GET'])
def list_users():
    all_users = Users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)


@app.route('/userdetails/<id>', methods=['GET'])
def user_details(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)


@app.route('/userupdate/<id>', methods=['PUT'])
def user_update(id):
    user = Users.query.get(id)

    number = request.json['number']
    names = request.json['names']
    surname = request.json['surname']
    phone_number = request.json['phone_number']
    location_id = request.json['location_id']

    user.number = number
    user.names = names
    user.surname = surname
    user.phone_number = phone_number
    user.location_location_id = location_id

    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/userdelete/<id>', methods=['DELETE'])
def user_delete(id):
    user = Users.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/newuser', methods=['POST'])
def new_user():
    number = request.json['number']
    names = request.json['names']
    surname = request.json['surname']
    phone_number = request.json['phone_number']
    location_id = request.json['location_id']

    user = Users(number=number, names=names, surname=surname, phone_number=phone_number,
                 location_location_id=location_id)

    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)


trip_schema = TripsSchema()
trips_schema = TripsSchema(many=True)


@app.route('/trips', methods=['GET'])
def list_trips():
    all_trips = Trips.query.all()
    results = trips_schema.dump(all_trips)
    return jsonify(results)


@app.route('/tripdetails/<id>', methods=['GET'])
def trip_details(id):
    trip = Trips.query.get(id)
    return trip_schema.jsonify(trip)


@app.route('/tripupdate/<id>', methods=['PUT'])
def trip_update(id):
    trip = Trips.query.get(id)

    start_time = request.json['start_time']
    end_time = request.json['end_time']
    route = request.json['route']

    trip.start_time = start_time
    trip.end_time = end_time
    trip.route = route

    db.session.commit()
    return trip_schema.jsonify(trip)


@app.route('/tripdelete/<id>', methods=['DELETE'])
def trip_delete(id):
    trip = Trips.query.get(id)

    if trip:
        for order in trip.orders:
            order.trip = None

        db.session.delete(trip)
        db.session.commit()
        return jsonify({'message': f'Trip with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Trip not found'}), 404


@app.route('/newtrip', methods=['POST'])
def new_trip():
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    route = request.json['route']

    trip = Trips(start_time=start_time, end_time=end_time, route=route)

    db.session.add(trip)
    db.session.commit()
    return trip_schema.jsonify(trip)


order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)


@app.route('/orders', methods=['GET'])
def list_orders():
    all_orders = Orders.query.all()
    results = orders_schema.dump(all_orders)
    return jsonify(results)


@app.route('/orderdetails/<id>', methods=['GET'])
def order_details(id):
    order = Orders.query.get(id)
    return order_schema.jsonify(order)


@app.route('/orderupdate/<id>', methods=['PUT'])
def order_update(id):
    order = Orders.query.get(id)

    number = request.json['number']
    price = request.json['price']

    order.number = number
    order.price = price

    db.session.commit()
    return order_schema.jsonify(order)


@app.route('/orderdelete/<id>', methods=['DELETE'])
def order_delete(id):
    order = Orders.query.get(id)

    if order:
        order.trip = None

        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': f'Order with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Order not found'}), 404


@app.route('/neworder', methods=['POST'])
def new_order():
    number = request.json['number']
    price = request.json['price']
    user_id = request.json['user_id']
    trip_id = request.json['trip_id']

    order = Orders(number=number, price=price, users_users_id=user_id, trips_trip_id=trip_id)

    db.session.add(order)
    db.session.commit()
    return order_schema.jsonify(order)


seat_schema = SeatsSchema()
seats_schema = SeatsSchema(many=True)


@app.route('/seats', methods=['GET'])
def list_seats():
    all_seats = Seats.query.all()
    results = seats_schema.dump(all_seats)
    return jsonify(results)


@app.route('/seatdetails/<id>', methods=['GET'])
def seat_details(id):
    seat = Seats.query.get(id)
    return seat_schema.jsonify(seat)


@app.route('/seatupdate/<id>', methods=['PUT'])
def seat_update(id):
    seat = Seats.query.get(id)

    number = request.json['number']

    seat.number = number

    db.session.commit()
    return seat_schema.jsonify(seat)


@app.route('/seatdelete/<id>', methods=['DELETE'])
def seat_delete(id):
    seat = Seats.query.get(id)

    if seat:
        db.session.delete(seat)
        db.session.commit()
        return jsonify({'message': f'Seat with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Seat not found'}), 404


@app.route('/newseat', methods=['POST'])
def new_seat():
    number = request.json['number']

    seat = Seats(number=number)

    db.session.add(seat)
    db.session.commit()
    return seat_schema.jsonify(seat)


car_schema = CarsSchema()
cars_schema = CarsSchema(many=True)


@app.route('/cars', methods=['GET'])
def list_cars():
    all_cars = Cars.query.all()
    results = cars_schema.dump(all_cars)
    return jsonify(results)


@app.route('/cardetails/<id>', methods=['GET'])
def car_details(id):
    car = Cars.query.get(id)
    return car_schema.jsonify(car)


@app.route('/carupdate/<id>', methods=['PUT'])
def car_update(id):
    car = Cars.query.get(id)

    brand = request.json['brand']
    model = request.json['model']
    year = request.json['year']

    car.brand = brand
    car.model = model
    car.year = year

    db.session.commit()
    return car_schema.jsonify(car)


@app.route('/cardelete/<id>', methods=['DELETE'])
def car_delete(id):
    car = Cars.query.get(id)

    if car:
        vehicles_with_car = Vehicles.query.filter_by(cars_cars_id=id).all()

        for vehicle in vehicles_with_car:
            vehicle.car = None

        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': f'Car with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Car not found'}), 404


@app.route('/newcar', methods=['POST'])
def new_car():
    brand = request.json['brand']
    model = request.json['model']
    year = request.json['year']
    seats_seat_id = request.json['seats_seat_id']

    car = Cars(brand=brand, model=model, year=year, seats_seat_id=seats_seat_id)

    db.session.add(car)
    db.session.commit()
    return car_schema.jsonify(car)


van_schema = VansSchema()
vans_schema = VansSchema(many=True)


@app.route('/vans', methods=['GET'])
def list_vans():
    all_vans = Vans.query.all()
    results = vans_schema.dump(all_vans)
    return jsonify(results)


@app.route('/vandetails/<id>', methods=['GET'])
def van_details(id):
    van = Vans.query.get(id)
    return van_schema.jsonify(van)


@app.route('/vanupdate/<id>', methods=['PUT'])
def van_update(id):
    van = Vans.query.get(id)

    brand = request.json['brand']
    model = request.json['model']
    year = request.json['year']

    van.brand = brand
    van.model = model
    van.year = year

    db.session.commit()
    return van_schema.jsonify(van)


@app.route('/vandelete/<id>', methods=['DELETE'])
def van_delete(id):
    van = Vans.query.get(id)

    if van:
        van.seat = None

        db.session.delete(van)
        db.session.commit()
        return jsonify({'message': f'Van with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Van not found'}), 404


@app.route('/newvan', methods=['POST'])
def new_van():
    brand = request.json['brand']
    model = request.json['model']
    year = request.json['year']
    seats_seats_id = request.json['seats_seats_id']

    van = Vans(brand=brand, model=model, year=year, seats_seats_id=seats_seats_id)

    db.session.add(van)
    db.session.commit()
    return van_schema.jsonify(van)


vehicle_schema = VehiclesSchema()
vehicles_schema = VehiclesSchema(many=True)


@app.route('/vehicles', methods=['GET'])
def list_vehicles():
    all_vehicles = Vehicles.query.all()
    results = vehicles_schema.dump(all_vehicles)
    return jsonify(results)


@app.route('/vehicledetails/<id>', methods=['GET'])
def vehicle_details(id):
    vehicle = Vehicles.query.get(id)
    return vehicle_schema.jsonify(vehicle)


@app.route('/vehicleupdate/<id>', methods=['PUT'])
def vehicle_update(id):
    vehicle = Vehicles.query.get(id)

    type_index = request.json['type_index']
    colour = request.json['colour']
    number_index = request.json['number_index']

    vehicle.type_index = type_index
    vehicle.colour = colour
    vehicle.number_index = number_index

    db.session.commit()
    return vehicle_schema.jsonify(vehicle)


@app.route('/vehicledelete/<id>', methods=['DELETE'])
def vehicle_delete(id):
    vehicle = Vehicles.query.get(id)

    if vehicle:
        if vehicle.car:
            vehicle.car = None
        elif vehicle.van:
            vehicle.van = None

        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'message': f'Vehicle with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Vehicle not found'}), 404


@app.route('/newvehicle', methods=['POST'])
def new_vehicle():
    type_index = request.json['type_index']
    colour = request.json['colour']
    number_index = request.json['number_index']
    cars_cars_id = request.json['cars_cars_id']
    vans_vans_id = request.json['vans_vans_id']

    vehicle = Vehicles(type_index=type_index, colour=colour, number_index=number_index, cars_cars_id=cars_cars_id,
                       vans_vans_id=vans_vans_id)

    db.session.add(vehicle)
    db.session.commit()
    return vehicle_schema.jsonify(vehicle)


driver_schema = DriversSchema()
drivers_schema = DriversSchema(many=True)


@app.route('/drivers', methods=['GET'])
def list_drivers():
    all_drivers = Drivers.query.all()
    results = drivers_schema.dump(all_drivers)
    return jsonify(results)


@app.route('/driverdetails/<id>', methods=['GET'])
def driver_details(id):
    driver = Drivers.query.get(id)
    return driver_schema.jsonify(driver)


@app.route('/driverupdate/<id>', methods=['PUT'])
def driver_update(id):
    driver = Drivers.query.get(id)

    vehicle_numbers = request.json['vehicle_numbers']
    name = request.json['name']
    surname = request.json['surname']

    driver.vehicle_numbers = vehicle_numbers
    driver.name = name
    driver.surname = surname

    db.session.commit()
    return driver_schema.jsonify(driver)


@app.route('/driverdelete/<id>', methods=['DELETE'])
def driver_delete(id):
    driver = Drivers.query.get(id)

    if driver:
        db.session.delete(driver)
        db.session.commit()
        return jsonify({'message': f'Driver with ID {id} deleted successfully'})
    else:
        return jsonify({'message': 'Driver not found'}), 404


@app.route('/newdriver', methods=['POST'])
def new_driver():
    vehicle_numbers = request.json['vehicle_numbers']
    name = request.json['name']
    surname = request.json['surname']
    order_order_id = request.json['order_order_id']
    location_location_id = request.json['location_location_id']
    vehicles_vehicles_id = request.json['vehicles_vehicles_id']

    driver = Drivers(vehicle_numbers=vehicle_numbers, name=name, surname=surname, order_order_id=order_order_id,
                     location_location_id=location_location_id, vehicles_vehicles_id=vehicles_vehicles_id)

    db.session.add(driver)
    db.session.commit()
    return driver_schema.jsonify(driver)


rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)


@app.route('/ratings', methods=['GET'])
def list_ratings():
    all_ratings = Rating.query.all()
    results = ratings_schema.dump(all_ratings)
    return jsonify(results)


@app.route('/ratingdetails/<order_id>/<driver_id>', methods=['GET'])
def rating_details(order_id, driver_id):
    rating = Rating.query.filter_by(orders_order_id=order_id, drivers_drivers_id=driver_id).first()
    return rating_schema.jsonify(rating)


@app.route('/ratingupdate/<order_id>/<driver_id>', methods=['PUT'])
def rating_update(order_id, driver_id):
    rating = Rating.query.filter_by(orders_order_id=order_id, drivers_drivers_id=driver_id).first()

    stars_number = request.json['stars_number']

    rating.stars_number = stars_number

    db.session.commit()
    return rating_schema.jsonify(rating)


@app.route('/ratingdelete/<order_id>/<driver_id>', methods=['DELETE'])
def rating_delete(order_id, driver_id):
    rating = Rating.query.filter_by(orders_order_id=order_id, drivers_drivers_id=driver_id).first()
    db.session.delete(rating)
    db.session.commit()
    return rating_schema.jsonify(rating)


@app.route('/newrating', methods=['POST'])
def new_rating():
    order_id = request.json['orders_order_id']
    driver_id = request.json['drivers_drivers_id']
    stars_number = request.json['stars_number']

    rating = Rating(orders_order_id=order_id, drivers_drivers_id=driver_id, stars_number=stars_number)

    db.session.add(rating)
    db.session.commit()
    return rating_schema.jsonify(rating)
