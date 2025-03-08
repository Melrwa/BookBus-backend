from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.bus import Bus
from app.models.bookings import Booking
from app.models.transactions import Transaction
from datetime import datetime, timedelta

def seed_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Seed Admin
        admin = User(
            name="Melki Orwa",
            email="orwamelki@gmail.com",
            role="admin"
        )
        admin.set_password("adminpassword")
        db.session.add(admin)

        # Seed Drivers
        driver1 = User(name="Driver One", email="driver1@example.com", role="driver")
        driver1.set_password("driverpassword")
        db.session.add(driver1)

        driver2 = User(name="Driver Two", email="driver2@example.com", role="driver")
        driver2.set_password("driverpassword")
        db.session.add(driver2)

        driver3 = User(name="Driver Three", email="driver3@example.com", role="driver")
        driver3.set_password("driverpassword")
        db.session.add(driver3)

        # Seed Customers
        customer1 = User(name="Customer One", email="customer1@example.com", role="customer")
        customer1.set_password("customerpassword")
        db.session.add(customer1)

        customer2 = User(name="Customer Two", email="customer2@example.com", role="customer")
        customer2.set_password("customerpassword")
        db.session.add(customer2)

        customer3 = User(name="Customer Three", email="customer3@example.com", role="customer")
        customer3.set_password("customerpassword")
        db.session.add(customer3)

        customer4 = User(name="Customer Four", email="customer4@example.com", role="customer")
        customer4.set_password("customerpassword")
        db.session.add(customer4)

        customer5 = User(name="Customer Five", email="customer5@example.com", role="customer")
        customer5.set_password("customerpassword")
        db.session.add(customer5)

        # Commit users to ensure they have IDs
        db.session.commit()

        # Seed Buses
        bus1 = Bus(
            driver_id=driver1.id,
            number_of_seats=30,
            cost_per_seat=500,
            route="Nairobi to Mombasa",
            departure_time=datetime.utcnow() + timedelta(hours=2),
            arrival_time=datetime.utcnow() + timedelta(hours=10)  # 8-hour trip
        )
        db.session.add(bus1)

        bus2 = Bus(
            driver_id=driver2.id,
            number_of_seats=40,
            cost_per_seat=600,
            route="Nairobi to Kisumu",
            departure_time=datetime.utcnow() + timedelta(hours=3),
            arrival_time=datetime.utcnow() + timedelta(hours=8)  # 5-hour trip
        )
        db.session.add(bus2)

        bus3 = Bus(
            driver_id=driver3.id,
            number_of_seats=35,
            cost_per_seat=550,
            route="Nairobi to Nakuru",
            departure_time=datetime.utcnow() + timedelta(hours=4),
            arrival_time=datetime.utcnow() + timedelta(hours=6)  # 2-hour trip
        )
        db.session.add(bus3)

        bus4 = Bus(
            driver_id=None,  # Unassigned bus
            number_of_seats=25,
            cost_per_seat=450,
            route="Nairobi to Eldoret",
            departure_time=datetime.utcnow() + timedelta(hours=5),
            arrival_time=datetime.utcnow() + timedelta(hours=9)  # 4-hour trip
        )
        db.session.add(bus4)

        bus5 = Bus(
            driver_id=None,  # Unassigned bus
            number_of_seats=20,
            cost_per_seat=400,
            route="Nairobi to Thika",
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=7)  # 1-hour trip
        )
        db.session.add(bus5)

        # Commit buses to ensure they have IDs
        db.session.commit()

        # Seed Bookings
        booking1 = Booking(
            customer_id=customer1.id,  # Assign customer_id
            bus_id=bus1.id,  # Assign bus_id
            seat_number=1,
            booking_date=datetime.utcnow(),
            status="confirmed"  # Confirmed booking
        )
        db.session.add(booking1)

        booking2 = Booking(
            customer_id=customer2.id,  # Assign customer_id
            bus_id=bus2.id,  # Assign bus_id
            seat_number=2,
            booking_date=datetime.utcnow(),
            status="confirmed"  # Confirmed booking
        )
        db.session.add(booking2)

        booking3 = Booking(
            customer_id=customer3.id,  # Assign customer_id
            bus_id=bus3.id,  # Assign bus_id
            seat_number=3,
            booking_date=datetime.utcnow(),
            status="canceled"  # Canceled booking
        )
        db.session.add(booking3)

        booking4 = Booking(
            customer_id=customer4.id,  # Assign customer_id
            bus_id=bus1.id,  # Assign bus_id
            seat_number=4,
            booking_date=datetime.utcnow(),
            status="pending"  # Pending booking
        )
        db.session.add(booking4)

        booking5 = Booking(
            customer_id=customer5.id,  # Assign customer_id
            bus_id=bus2.id,  # Assign bus_id
            seat_number=5,
            booking_date=datetime.utcnow(),
            status="confirmed"  # Confirmed booking
        )
        db.session.add(booking5)

        booking6 = Booking(
            customer_id=customer1.id,  # Assign customer_id
            bus_id=bus3.id,  # Assign bus_id
            seat_number=6,
            booking_date=datetime.utcnow(),
            status="pending"  # Pending booking
        )
        db.session.add(booking6)

        # Commit bookings
        db.session.commit()

        # Seed Transactions (only for confirmed bookings)
        transaction1 = Transaction(
            booking_id=booking1.id,  # Confirmed booking
            amount_paid=500,
            payment_date=datetime.utcnow(),
            payment_method="M-Pesa"
        )
        db.session.add(transaction1)

        transaction2 = Transaction(
            booking_id=booking2.id,  # Confirmed booking
            amount_paid=600,
            payment_date=datetime.utcnow(),
            payment_method="Credit Card"
        )
        db.session.add(transaction2)

        transaction3 = Transaction(
            booking_id=booking5.id,  # Confirmed booking
            amount_paid=550,
            payment_date=datetime.utcnow(),
            payment_method="M-Pesa"
        )
        db.session.add(transaction3)

        # Commit all changes
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()