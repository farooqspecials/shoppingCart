# Flask Shopping Cart Application

This is a simple Flask application demonstrating a shopping cart system with functionalities such as listing products, adding them to a cart, checking out, and saving customer details.

## Features

- **List Products:** Display a list of products with their prices and categories.
- **Add to Cart:** Add products to a shopping cart.
- **View Cart:** Display items in the cart with quantities and total prices.
- **Checkout:** Collect customer name and address information and display a thank you message upon order placement.

## Prerequisites

Before running this application, ensure you have the following software installed:

- [Docker](https://www.docker.com/products/docker-desktop) (Docker Desktop for Windows/macOS or Docker Engine for Linux)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Application with Docker Compose

Follow these steps to set up and run the application using Docker Compose:

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/farooqspecials/flask-shopping-cart.git
cd flask-shopping-cart

### Step 2: Running the application
docker-compose up --build

### Step 3: Access the application
http://localhost:5000


