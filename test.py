from pathlib import Path
from uuid import uuid4
import webbrowser

number_of_seats = 150
correct_password = "secure123"


def escape_pdf_text(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_ticket_pdf(customer_name, seats_booked, ticket_id=None, output_dir=None):
    ticket_id = ticket_id or f"TKT-{uuid4().hex[:8].upper()}"
    safe_name = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in (customer_name or "guest").strip())
    output_dir = Path(output_dir or Path(__file__).resolve().parent / "tickets")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{safe_name}_{ticket_id}.pdf"

    lines = [
        "THEATER BOOKING TICKET",
        f"Ticket ID: {ticket_id}",
        f"Customer: {customer_name.strip() or 'Guest'}",
        f"Seats Booked: {seats_booked}",
        "Status: Confirmed",
    ]

    content_stream = "BT\n"
    y_position = 760
    for line in lines:
        safe_line = line.encode("latin-1", "replace").decode("latin-1")
        content_stream += f"/F1 12 Tf 50 {y_position} Td ({escape_pdf_text(safe_line)}) Tj T* \n"
        y_position -= 16
    content_stream += "ET"

    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(content_stream.encode('latin-1'))} >>\nstream\n{content_stream}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    pdf_data = bytearray(b"%PDF-1.4\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf_data))
        pdf_data.extend(f"{index} 0 obj\n".encode("latin-1"))
        pdf_data.extend(obj.encode("latin-1"))
        pdf_data.extend(b"\nendobj\n")

    xref_offset = len(pdf_data)
    pdf_data.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    pdf_data.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf_data.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

    pdf_data.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin-1")
    )

    output_path.write_bytes(pdf_data)
    return output_path


def generate_and_download_ticket(customer_name, seats_booked, ticket_id=None, output_dir=None):
    output_path = generate_ticket_pdf(customer_name, seats_booked, ticket_id=ticket_id, output_dir=output_dir)
    webbrowser.open(output_path.resolve().as_uri())
    return output_path


def main():
    password = input("Enter the password: ")
    if password != correct_password:
        print("Incorrect password. Access denied.")
        return

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
                customer_name = input("Enter your name for the ticket: ").strip() or "Guest"
                ticket_path = generate_and_download_ticket(customer_name, number)
                print("Congrats! You have successfully booked", number, "seats.")
                print("Ticket PDF created at:", ticket_path)

        elif choice == 2:
            print("Available seats =", number_of_seats)

        elif choice == 3:
            print("Thank you for using our service. Goodbye!!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
