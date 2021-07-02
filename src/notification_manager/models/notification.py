"""
sendNotification(action, status, origin, receptor, data)
* Notification (action, status, origin, receptor, data)
* Notification (action: New Search Hits, status: OK, origin: i3-market, receptor: datamarketplace_consumer, data = search results)
* Notification (action: Data Purchase Request, status: ok, origin: datamarketplace_provider, receptor: i3-Market)
* Notification (action: Data Purchase Request, status: Reject, origin: datamarketplace_provider, receptor: i3-Market)
* Notification (action: Accept Proposal, status: ok, origin: datamarketplace_provider, receptor: i3-Market, data = contractual parameters)
* Notification (action: Accept Proposal, status: Reject, origin: datamarketplace_provider, receptor: i3-Market)
* Notification (action: Activate Agreement, status: pending, origin: i3-Market, receptor: datamarketplace_consumer)
* Notification (action: Activate Agreement, status: ok, origin: i3-market, receptor: datamarketplace_provider, datamarketplace_consumer)
"""


class Notification:
    def __init__(self, action, status, origin, receptor, data=None):
        self.action = action
        self.status = status
        self.origin = origin
        self.receptor = receptor
        self.data = data
