from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")  # Replace with your connection string
db = client['car_booking_app']
cars_col = db['cars']
bookings_col = db['bookings']

# View available cars
def view_cars():
    print("\nAvailable Cars:")
    cars = cars_col.find({"booked": False})
    found = False
    for car in cars:
        print(f"ID: {car['_id']} | {car['brand']} {car['model']} - ₹{car['price']}/day")
        found = True
    if not found:
        print("No cars available.")

# Book a car
def book_car():
    view_cars()
    car_id = input("Enter Car ID to book: ")
    user_name = input("Enter your name: ")
    
    car = cars_col.find_one({"_id": ObjectId(car_id), "booked": False})
    
    if car:
        cars_col.update_one({"_id": ObjectId(car_id)}, {"$set": {"booked": True}})
        bookings_col.insert_one({
            "user": user_name,
            "car_id": car["_id"],
            "brand": car["brand"],
            "model": car["model"]
        })
        print(f"Car {car['brand']} {car['model']} booked successfully!")
    else:
        print("Invalid Car ID or car already booked.")

# Cancel a booking
def cancel_booking():
    user_name = input("Enter your name to cancel booking: ")
    booking = bookings_col.find_one({"user": user_name})
    
    if booking:
        cars_col.update_one({"_id": booking["car_id"]}, {"$set": {"booked": False}})
        bookings_col.delete_one({"_id": booking["_id"]})
        print(f"Booking for {booking['brand']} {booking['model']} cancelled.")
    else:
        print("No booking found for this user.")

# View user's booking
def view_booking():
    user_name = input("Enter your name to view booking: ")
    booking = bookings_col.find_one({"user": user_name})
    
    if booking:
        print(f"You booked: {booking['brand']} {booking['model']}")
    else:
        print("No booking found.")

# Admin: Add a new car
def add_car():
    brand = input("Enter Car Brand: ")
    model = input("Enter Car Model: ")
    price = input("Enter Price per Day: ")

    car = {
        "brand": brand,
        "model": model,
        "price": price,
        "booked": False
    }
    cars_col.insert_one(car)
    print("Car added successfully.")

# Admin: Remove a car
def remove_car():
    view_cars()
    car_id = input("Enter Car ID to remove: ")
    result = cars_col.delete_one({"_id": ObjectId(car_id)})
    if result.deleted_count > 0:
        print("Car removed successfully.")
    else:
        print("Car ID not found.")

# Menu
def menu():
    while True:
        print("\n--- Car Booking App (MongoDB) ---")
        print("1. View Available Cars")
        print("2. Book a Car")
        print("3. Cancel Booking")
        print("4. View My Booking")
        print("5. Admin - Add Car")
        print("6. Admin - Remove Car")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_cars()
        elif choice == '2':
            book_car()
        elif choice == '3':
            cancel_booking()
        elif choice == '4':
            view_booking()
        elif choice == '5':
            add_car()
        elif choice == '6':
            remove_car()
        elif choice == '7':
            print("Thank you for using the Car Booking App!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
