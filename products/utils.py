from django.conf import settings
from django.core.mail import send_mail

from .models import User, Brand, Product

def send_email_notification(user, old_instance, instance, update=True):
    """ Sends an email notification to all users except the one performing the change
    
        Parameters:
        + user: User changing the instance
        + old_instance: Old instance (updated or removed)
        + instance: Instance with updated information
        + update: whether the instance was updated or not (deleted)
    """
    if update and not instance.changed(old_instance): # Instance didn't change, notification is not necessary
        return
    # Subject construction
    subject = ""
    instance_type = "instance"
    if isinstance(old_instance, Brand):
        subject = "Brand"
        instance_type = "brand"
    elif isinstance(old_instance, Product):
        subject = "Product"
        instance_type = "product"
    subject += f" {old_instance.name}" # Product/brand old name (if the name changed,
                                       # admins can still identify it)
    if update:
        subject += f" with ID {old_instance.id}"
    subject += " updated" if update else " deleted" # Action performed
    # Message construction
    message = f"{user.first_name} {user.last_name} ({user.username}) has "
    if update:
        message += f"updated the {instance_type} {old_instance.name} (ID: {old_instance.id}).\nFields updated:{instance.get_updated_info_str(old_instance)}"
    else:
        message += f"removed the {instance_type} {old_instance.name}.\n{old_instance.get_info_str()}"

    recipient_list = User.objects.exclude(id=user.id).values_list('email', flat=True)
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list
    )