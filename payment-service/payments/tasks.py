import time
import random
from celery import shared_task
from .models import Payment

@shared_task
def async_process_payment(payment_id):
    """
    Simulates an asynchronous payment processing and updates the payment status.
    """
    try:
        payment = Payment.objects.get(id=payment_id)
        payment.status = 'Processing'
        payment.save()
        print(f"Payment {payment_id} is now Processing.")

        # Simulate a delay for payment processing (e.g., 5-10 seconds)
        time.sleep(random.randint(5, 10))

        # Simulate success or failure
        if random.random() > 0.1:
            payment.status = 'Completed'
            payment.transaction_id = f"TXN-{payment_id}-{int(time.time())}"
            print(f"Payment {payment_id} Completed with Transaction ID: {payment.transaction_id}")
        else:
            payment.status = 'Failed'
            print(f"Payment {payment_id} Failed.")

        payment.save()

    except Payment.DoesNotExist:
        print(f"Payment with ID {payment_id} not found.")
    except Exception as e:
        print(f"Error processing payment {payment_id}: {e}")