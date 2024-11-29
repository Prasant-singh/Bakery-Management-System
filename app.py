import streamlit as st
import pandas as pd
import datetime
import io
import openpyxl
class Bakery:
    def __init__(self):
        self.cid = 100
        self.orders = pd.DataFrame(columns=["id", "Name", "Item", "Quantity", "Date"])
        self.date = datetime.datetime.now().replace(second=0, microsecond=0)
    
    def add_order(self, name, item, quantity):
        """Add a new order to the DataFrame."""
        order_id = self.cid  
        self.cid += 1
        new_order = {
            "id": order_id,
            "Name": name,
            "Item": item,
            "Quantity": quantity,
            "Date": self.date
        }
        self.orders = pd.concat([self.orders, pd.DataFrame([new_order])], ignore_index=True)
        return new_order

    def update_order(self, customer_name, new_item, new_quantity):
        """Update an order for a given customer name."""
        if customer_name in self.orders["Name"].values:
            idx = self.orders[self.orders["Name"] == customer_name].index[0]
            self.orders.loc[idx, "Item"] = new_item
            self.orders.loc[idx, "Quantity"] = new_quantity
            return True
        return False

    def save_to_excel(self):
        """Save the current orders to an Excel file and return it as binary data."""
        output = io.BytesIO()  # In-memory binary stream
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            self.orders.to_excel(writer, index=False)  # Write DataFrame to Excel
        output.seek(0)  # Reset the stream position
        return output.read()


# Ensure Bakery instance is maintained in session state
if "bakery" not in st.session_state:
    st.session_state.bakery = Bakery()

bakery = st.session_state.bakery  # Access the session state Bakery instance

# Streamlit Interface
st.set_page_config(page_title="Apna Bakery Store", layout="centered")

st.title("Apna Bakery Store")
st.write("Welcome to the bakery management app. Use the options below to manage orders.")

# Navigation
menu = st.sidebar.radio("Navigate", ["Add Order", "View Orders", "Update Order", "Save Orders"])

# Add Order Section
if menu == "Add Order":
    st.header("Add a New Order")
    name = st.text_input("Enter Customer Name")
    item = st.selectbox(
        "Select Item", 
        ["Samosa", "Patties", "Pastry", "Burger"]
    )
    quantity = st.number_input("Enter Quantity", min_value=1, step=1)
    if st.button("Add Order"):
        if name and item and quantity:
            new_order = bakery.add_order(name, item, quantity)
            st.success(f"Order added successfully! Order ID: {new_order['id']}")
        else:
            st.error("Please fill in all the fields.")

# View Orders Section
elif menu == "View Orders":
    st.header("All Orders")
    if bakery.orders.empty:
        st.write("No orders available.")
    else:
        st.dataframe(bakery.orders)

# Update Order Section
elif menu == "Update Order":
    st.header("Update an Existing Order")
    if bakery.orders.empty:
        st.write("No orders available to update.")
    else:
        customer_name = st.text_input("Enter Customer Name to Update")
        new_item = st.selectbox(
            "Select New Item", 
            ["Samosa", "Patties", "Pastry", "Burger"]
        )
        new_quantity = st.number_input("Enter New Quantity", min_value=1, step=1)
        if st.button("Update Order"):
            if bakery.update_order(customer_name, new_item, new_quantity):
                st.success(f"Order for {customer_name} updated successfully!")
            else:
                st.error("Customer not found. Please try again.")

# Save Orders Section
elif menu == "Save Orders":
    st.header("Save Orders to Excel")
    if st.button("Save to Excel"):
        excel_data = bakery.save_to_excel()  # Fetch binary content of the Excel file
        st.success("Orders saved successfully! Click below to download.")
        st.download_button(
            label="Download Excel File",
            data=excel_data,
            file_name="bakery_orders.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )