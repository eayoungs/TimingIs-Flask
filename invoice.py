from geepal import get_events as ge
from geepal import dfsort as dfs
import invdef


calendar = invdef.calendar
eventType = invdef.eventType
project = invdef.project

"""
# TODO (eayoungs@gmail.com): Move the invoice creation to a separate file
doc = SimpleInvoice('invoice.pdf')

# Paid stamp, optional
doc.is_paid = True

doc.invoice_info = InvoiceInfo(1023, datetime.now(), datetime.now())  #     Invoice info, optional

# Service Provider Info, optional
doc.service_provider_info = ServiceProviderInfo(
    name=invdef.provider_name,
    street=invdef.provider_street,
    city=invdef.provider_city,
    state=invdef.provider_state,
    country=invdef.provider_country,
    post_code=invdef.provider_post_code,
    #vat_tax_number=invdef.vat_tax_number
)

# Client info, optional
doc.client_info = ClientInfo(
    email=invdef.client_email
    #name=invdef.client_name,
    #street=invdef.client_street,
    #city=invdef.client_city,
    #state=invdef.client_state,
    #country=invdef.client_country,
    #post_code=invdef.client_post_code,
)
"""

# Add Item
evStartEvEnd_calEvDfsDct = dfs.add_durations(ge.main())
eventTypesDct = dfs.get_unique_events(evStartEvEnd_calEvDfsDct, calendar) 

for name, value in eventTypesDct.items():
    #    if eventType in name:
    invoiceDf = dfs.get_project(value, project) 
    for index, row in invoiceDf.iterrows():
        print(row['joined'])
        #doc.add_item(Item('Item', row['joined'], 1, '1.1'))

"""
# Tax rate, optional
doc.set_item_tax_rate(20)  # 20%

# Transactions detail, optional
doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
doc.add_transaction(Transaction('Stripe', 222, date.today(), 2))

# Optional  
doc.set_bottom_tip("Email: " + invdef.provider_email + "<br />Don't hesitate to contact   us for any questions.")

doc.finish()
"""
