Khalti Payment Integration

This project demonstrates the integration of Khalti payment gateway using Python for the backend and a JavaScript-based frontend.

Project Structure

Frontend: Contains the React-based frontend code.

mypay (Backend): Django-based backend for handling payments.

Prerequisites

Ensure you have the following installed:

Node.js & npm

Python & pip

Django

Installation & Setup

Clone the Repository

git clone https://github.com/Rajdonge/Khalti-Payment-Integration
cd Khalti-Payment-Integration

Frontend Setup

cd frontend
npm install
npm run dev

The frontend exposes the following endpoints:

/checkout - To initiate the payment process

/confirm-payment - To confirm and verify payments

Backend Setup

cd mypay
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

The backend runs on Django and provides necessary API endpoints for payment verification.

Features

Khalti payment gateway integration

Secure backend handling of payments

Frontend UI for processing payments

License

This project is open-source. Feel free to use and modify it as needed.

Author

Developed by Bibek Dhimal.

