number_of_seats = 150
correct_password = "secure123"

password = input("Enter the password: ")
if password != correct_password:
    print("Incorrect password. Access denied.")
    raise SystemExit

print("\nPassword accepted. Welcome to the Theater Booking System!")

while True:
    print("\n\t---MAIN MENU---")
    print("1. Book a seat")
    print("2. Check available seats")
    print("3. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        number = int(input("Enter the number of seats to book: "))
        if number > number_of_seats:
            print("Invalid choice! Not enough seats available.")
        else:
            number_of_seats -= number
            print("Congrats! You have successfully booked", number, "seats.")

    elif choice == 2:
        print("Available seats =", number_of_seats)

    elif choice == 3:
        print("Thank you for using our service. Goodbye!!")
        break

    else:
        print("Invalid option. Please try again.")
