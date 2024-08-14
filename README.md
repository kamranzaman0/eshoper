# Eshoper

Eshoper is a comprehensive e-commerce platform built using Django. It offers a full-fledged online shopping experience with features
like product browsing, filtering, shopping cart, checkout, and payment integration.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Features
- User registration and authentication
- Product browsing with categories and filters
- Shopping cart management
- Order management
- Payment integration with Stripe and PayPal


## Installation

To get the project up and running locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kamranzaman0/eshoper.git
   cd eshoper
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`


## Usage

After setting up the project, you can:

- Register as a new user or log in with an existing account.
- Browse products by categories and apply filters.
- Add products to the shopping cart.
- Proceed to checkout and complete the purchase using Stripe or PayPal.
- View order history in your account.


## Contributing

Contributions are welcome! Please fork this repository and submit a pull request if you would like to improve the codebase.

## Contact

For any inquiries or issues, please contact me at kamranzaman0502@gmail.com or on linkedin https://www.linkedin.com/in/kamran-zaman-4520a1300/


