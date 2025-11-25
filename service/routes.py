"""
Product Service

Paths:
------
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database
"""

from flask import jsonify, request, url_for, abort
from service.models import Product
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Product REST API Service",
            version="1.0",
            paths=url_for("list_products", _external=True),
        ),
        200,
    )


######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its id
    """
    app.logger.info("Request for product with id: %s", product_id)
    
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product with id '{product_id}' was not found.")
    
    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), 200


######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product
    This endpoint will update a Product based on the body that is posted
    """
    app.logger.info("Request to update product with id: %s", product_id)
    
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product with id '{product_id}' was not found.")
    
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    
    app.logger.info("Product with ID [%s] updated.", product.id)
    return jsonify(product.serialize()), 200


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product
    This endpoint will delete a Product based on the id specified in the path
    """
    app.logger.info("Request to delete product with id: %s", product_id)
    
    product = Product.find(product_id)
    if product:
        product.delete()
        app.logger.info("Product with ID [%s] delete complete.", product_id)
    
    return "", 204


######################################################################
# LIST ALL PRODUCTS / QUERY PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """
    Returns all of the Products or query by name, category, or availability
    """
    app.logger.info("Request for product list")
    
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    
    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Find by category: %s", category)
        products = Product.find_by_category(category)
    elif available:
        app.logger.info("Find by availability: %s", available)
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        app.logger.info("Find all")
        products = Product.all()
    
    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    
    return jsonify(results), 200


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based on the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)
    
    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(message), 201, {"Location": location_url}