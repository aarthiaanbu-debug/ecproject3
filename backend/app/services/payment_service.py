import razorpay

client = razorpay.Client(
    auth=(
        "YOUR_KEY",
        "YOUR_SECRET"
    )
)

def create_payment(amount):

    payment = client.order.create({

        "amount": amount * 100,

        "currency": "INR",

        "payment_capture": 1
    })

    return payment