# Zee Mart

An intuitive and user-friendly e-commerce platform designed to provide a seamless shopping experience. From browsing a diverse range of products to secure online payments, our website ensures a hassle-free process for both sellers and buyers. With features like detailed product descriptions, Cart and integrated payment gateways, shopping has never been more convenient. Whether you're a vendor looking to reach a broader audience or a shopper seeking the latest in fashion, tech, or home goods, ZeeMart caters to all your e-commerce needs.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Payment Integration](#payment-integration)
7. [Contributing](#contributing)

## Getting Started

Our project is a comprehensive RESTful API built using Django, designed to power a modern e-commerce platform. At its core, the API aims to provide all the necessary backend functionalities required to create a seamless online shopping experience. Here's a brief overview of its capabilities:

- User Authentication: Users can register and log in using their standard credentials or opt for a swift Google-based authentication.

- Product Management: The API handles a wide array of products, categorized effectively to ensure easy browsing and product discovery.

- Cart Functionality: Users can add products to their cart, modify item quantities, or remove them as they continue their shopping journey. This dynamic cart system ensures flexibility and user convenience.

- Secure Payment: Leveraging the power of Stripe, one of the most reliable online payment solutions, the API ensures that transactions are not only swift but also secure, offering peace of mind to both buyers and sellers.

- This API is the backbone of our e-commerce platform, ready to be integrated with frontend solutions, ensuring scalability, security, and efficiency in managing online commerce operations.


### Prerequisites

- Python
- Postgres
- Django
- Postman

### Installation

1. Clone the repo:
```
   git clone https://github.com/abbasifaizan70/Ecommerce_django_rest_apis
```

2. Install the required packages:
```
   pip install -r requirements.txt
```

## Usage

### **Starting the Server:**

To get started, run the Django development server:

```bash
python manage.py runserver
```

This will start the server on [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### **Step dependencies:**

create ``.env`` file in root directory with following key and values

```
GOOGLE_CLIENT_ID=your google client id
GOOGLE_CLIENT_SECRET=your google client secret key
CLOUDNARY_CLOUD_NAME=your cloudnary cloud anme 
CLOUDNARY_API_KEYS=your cloudnary api key
CLOUDNARY_API_SECRET=your cloudnary secret key
CLOUDNARY_SECURE=TRUE
```

## API Endpoints

For a comprehensive list and description of all available API endpoints, navigate to the Swagger documentation:

[http://localhost:8000/swagger/](http://127.0.0.1:8000/swagger/)

Swagger provides a user-friendly interface where you can view all the API functionalities, try them out, and see their responses in real-time. Whether you're looking to authenticate a user, manage products, or handle payments, everything you need can be found there.

Remember, as you make changes or updates to the API, ensure the documentation reflects these modifications to assist future developers or users.


## Contributing

For Contribution you can reach me at ``abbasi.faizan1997@gmail.com``
