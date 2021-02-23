if (user == "AnonymousUser"){
    userFormData.name = form.name.value
    userFormData.email = form.email.value
}

var url = "/process_order/"

fetch(url, {
    method: "POST",
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
        'form': userFormData,
        'shipping': shippingInfo,
    })
})

.then((response) => {response.json()})

.then((data) => {
    console.log('transaction:', data);  
    alert('transaction complete');
    window.location.href = "{% url 'store' %}";
})
