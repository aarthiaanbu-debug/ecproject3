def use_credits(
    subscription,
    amount
):

    if subscription.credits < amount:

        return {
            "message": "Not enough credits"
        }

    subscription.credits -= amount

    return {
        "message": "Credits used"
    }