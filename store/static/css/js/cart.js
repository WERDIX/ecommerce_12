var updateBtns = document.getElementsByClassName("update-cart");

console.log("Update Buttons Found:", updateBtns.length); // Added logging

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("Product ID:", productId, "Action:", action);

        console.log("USER", user); // Confirm user variable
        if (user === 'AnonymousUser') {
            console.log('Not logged in');
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log("User is logged in, sending data...");

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Ensure this token is set correctly
        },
        body: JSON.stringify({ "productId": productId, "action": action })
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('Data', data);
        location.reload();
    })
    .catch((error) => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}





