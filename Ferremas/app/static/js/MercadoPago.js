function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const totalConIva = parseFloat(document.querySelector('.total').dataset.total);

const carritoItems = [];
document.querySelectorAll('.item').forEach(item => {
    carritoItems.push({
        sku: item.dataset.sku,
        nombre: item.dataset.nombre,
        cantidad: parseInt(item.dataset.cantidad),
        precio: parseFloat(item.dataset.precio),
        imagen: item.dataset.imagen
    });
});

const mp = new MercadoPago('TEST-021dcf1f-ec2f-4f9f-aa82-1f57c175d50c', {
    locale: 'es'
});
const bricksBuilder = mp.bricks();
const renderPaymentBrick = async (bricksBuilder) => {
    fetch('/crear_preferencia/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            transaction_amount: totalConIva,
            items: carritoItems
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al crear la preferencia de pago');
            }
            return response.json();
        })
        .then(data => {
            console.log('Respuesta de crear_preferencia:', data);
            const preferenceId = data.preference_id;

            const settings = {
                initialization: {
                    preferenceId: preferenceId,
                    amount: totalConIva,
                    payer: {
                        name: "",
                        surname: "",
                        email: "",
                    },
                },
                customization: {
                    visual: {
                        style: {
                            theme: "default",
                        },
                    },
                    paymentMethods: {
                        ticket: "all",
                        atm: "all",
                        onboarding_credits: "all",
                        debitCard: "all",
                        creditCard: "all",
                        maxInstallments: 12
                    },
                },
                callbacks: {
                    onReady: () => {
                    },
                    onSubmit: ({ selectedPaymentMethod, formData }) => {
                        return new Promise((resolve, reject) => {
                            fetch("/process_payment/", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                    "X-CSRFToken": csrftoken
                                },
                                body: JSON.stringify({
                                    transaction_amount: totalConIva,
                                    items: carritoItems,
                                    formData: formData
                                }),
                            })
                                .then((response) => {
                                    if (!response.ok) {
                                        throw new Error('Error al procesar el pago');
                                    }
                                    return response.json();
                                })
                                .then((response) => {
                                    window.location.href = response.redirect_url;
                                })
                                .catch((error) => {
                                    console.error('Error:', error);
                                    reject(error);
                                });
                        });
                    },
                    onError: (error) => {
                        console.error(error);
                    },
                },
            };

            window.paymentBrickController = bricksBuilder.create(
                "payment",
                "paymentBrick_container",
                settings
            );
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

renderPaymentBrick(bricksBuilder);