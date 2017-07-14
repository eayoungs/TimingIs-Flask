from datetime import datetime, date
import pandas as pd
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, \
                             Item, Transaction
from pyinvoice.templates import SimpleInvoice


invoiceItems = pd.DataFrame()
invoiceItemsDct = {'Project1' : {0: {'duration': 2, 'description': 'Work'},
                                 1: {'duration': 1.5, 'description': 'Some other work'}},
                   'Project2' : {2: {'duration': 2, 'description': 'Work'},
                                 3: {'duration': 1.5, 'description': 'Some other work'}}
                  }

calendar = 'Billing'
eventType = 'work'
project = 'Project'
billing_rate = '101'

client_email='client@email.com'
client_name='Client',
client_street='Easy St.',
client_city='Big City',
client_state='Blue State',
client_country='USA',
client_post_code='55555',

provider_email='provider@email.com'
provider_name='Provider Inc.'
provider_street='Easy St.'
provider_city='Big City'
provider_state='Blue State'
provider_country='USA'
provider_post_code='55555'
provider_tax_number='Vat/Tax number'

def main(invoiceItemsDct=invoiceItemsDct, calendar=calendar, eventType=eventType, project=project, 
         client_email=client_email,
         client_name=client_name,
         client_street=client_street,
         client_city=client_city,
         client_state=client_state,
         client_country=client_country,
         client_post_code=client_post_code,
         provider_email=provider_email,
         provider_name=provider_name,
         provider_street=provider_street,
         provider_city=provider_city,
         provider_state=provider_state,
         provider_country=provider_country,
         provider_post_code=provider_post_code,
         provider_tax_number=provider_tax_number,
         billing_rate=billing_rate,
         paid_status=False):
    """  """

    doc = SimpleInvoice('invoice.pdf')

    # Paid stamp, optional
    doc.is_paid = paid_status

    doc.invoice_info = InvoiceInfo(1023, datetime.now(), datetime.now())  #     Invoice info, optional

    # Service Provider Info, optional
    doc.service_provider_info = ServiceProviderInfo(
        name=provider_name,
        street=provider_street,
        city=provider_city,
        state=provider_state,
        country=provider_country,
        post_code=provider_post_code,
        #vat_tax_number=vat_tax_number
    )

    # Client info, optional
    doc.client_info = ClientInfo(
        email=client_email
        #name=client_name,
        #street=client_street,
        #city=client_city,
        #state=client_state,
        #country=client_country,
        #post_code=client_post_code,
    )

    # Add Item
    for key1, value1 in invoiceItemsDct.items():
        for key2, value2 in value1.items():
            doc.add_item(Item(key1, value2['description'], value2['duration'], billing_rate))

    # Tax rate, optional
    doc.set_item_tax_rate(20)  # 20%

    # Transactions detail, optional
    doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
    doc.add_transaction(Transaction('Stripe', 222, date.today(), 2))

    # Optional  
    doc.set_bottom_tip("Email: " + provider_email + "<br />Don't hesitate to contact   us for any questions.")

    doc.finish()

if __name__ == '__main__':
    main()
