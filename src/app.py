"""Flask web application for warehouse management."""

from flask import Flask, render_template, request, redirect, url_for, flash
from ohtuvarasto import Ohtuvarasto

app = Flask(__name__)
app.secret_key = "ohtuvarasto-secret-key"

# Global warehouse manager instance
warehouse_manager = Ohtuvarasto()


@app.route("/")
def index():
    """Display list of all warehouses."""
    warehouses = warehouse_manager.get_all_warehouses()
    return render_template("index.html", warehouses=warehouses)


@app.route("/warehouse/new", methods=["GET", "POST"])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            warehouse_manager.create_warehouse(name)
            flash(f"Warehouse '{name}' created successfully!", "success")
            return redirect(url_for("index"))
        flash("Warehouse name cannot be empty.", "error")
    return render_template("create_warehouse.html")


@app.route("/warehouse/<int:warehouse_id>")
def view_warehouse(warehouse_id):
    """View a specific warehouse and its products."""
    warehouse = warehouse_manager.get_warehouse(warehouse_id)
    if warehouse is None:
        flash("Warehouse not found.", "error")
        return redirect(url_for("index"))
    products = warehouse_manager.get_products(warehouse_id)
    return render_template(
        "view_warehouse.html",
        warehouse_id=warehouse_id,
        warehouse=warehouse,
        products=products,
    )


@app.route("/warehouse/<int:warehouse_id>/edit", methods=["GET", "POST"])
def edit_warehouse(warehouse_id):
    """Edit a warehouse name."""
    warehouse = warehouse_manager.get_warehouse(warehouse_id)
    if warehouse is None:
        flash("Warehouse not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        if new_name:
            warehouse_manager.update_warehouse_name(warehouse_id, new_name)
            flash(f"Warehouse renamed to '{new_name}'!", "success")
            return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))
        flash("Warehouse name cannot be empty.", "error")

    return render_template(
        "edit_warehouse.html", warehouse_id=warehouse_id, warehouse=warehouse
    )


@app.route("/warehouse/<int:warehouse_id>/delete", methods=["POST"])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    warehouse = warehouse_manager.get_warehouse(warehouse_id)
    if warehouse:
        name = warehouse["name"]
        warehouse_manager.delete_warehouse(warehouse_id)
        flash(f"Warehouse '{name}' deleted.", "success")
    else:
        flash("Warehouse not found.", "error")
    return redirect(url_for("index"))


@app.route("/warehouse/<int:warehouse_id>/product/add", methods=["POST"])
def add_product(warehouse_id):
    """Add a product to a warehouse."""
    name = request.form.get("product_name", "").strip()
    try:
        quantity = float(request.form.get("quantity", 0))
    except ValueError:
        quantity = 0

    if name and quantity >= 0:
        if warehouse_manager.add_product(warehouse_id, name, quantity):
            flash(f"Product '{name}' added with quantity {quantity}.", "success")
        else:
            flash("Failed to add product.", "error")
    else:
        flash("Invalid product name or quantity.", "error")

    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


@app.route("/warehouse/<int:warehouse_id>/product/<product_name>/remove", methods=["POST"])
def remove_product(warehouse_id, product_name):
    """Remove a product from a warehouse."""
    if warehouse_manager.remove_product(warehouse_id, product_name):
        flash(f"Product '{product_name}' removed.", "success")
    else:
        flash("Failed to remove product.", "error")
    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


@app.route("/warehouse/<int:warehouse_id>/product/<product_name>/update", methods=["POST"])
def update_product(warehouse_id, product_name):
    """Update product quantity."""
    try:
        new_quantity = float(request.form.get("quantity", 0))
    except ValueError:
        new_quantity = -1

    if new_quantity >= 0:
        if warehouse_manager.update_product_quantity(
            warehouse_id, product_name, new_quantity
        ):
            flash(f"Product '{product_name}' quantity updated to {new_quantity}.", "success")
        else:
            flash("Failed to update product quantity.", "error")
    else:
        flash("Invalid quantity.", "error")

    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


@app.route("/warehouse/<int:warehouse_id>/clear", methods=["POST"])
def clear_warehouse(warehouse_id):
    """Clear all products from a warehouse."""
    if warehouse_manager.clear_warehouse(warehouse_id):
        flash("All products cleared from warehouse.", "success")
    else:
        flash("Failed to clear warehouse.", "error")
    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


if __name__ == "__main__":
    app.run(debug=True)
