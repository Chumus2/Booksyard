// Adding_Quantity_To_Cart
function add_Quantity(amount) {

    const input = document.getElementById("quantity");
    let value = parseInt(input.value) + amount;

    if (value < 1) value = 1;
    input.value = value
 
};