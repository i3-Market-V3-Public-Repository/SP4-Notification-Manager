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
from datetime import datetime, timezone

from loguru import logger
import uuid


class Notification:
    def __init__(self, _id, action, status, origin, receptor, data=None, unread=True, date_created=None):
        self.id = _id
        self.action = action
        self.status = status
        self.origin = origin
        self.receptor = receptor
        self.data = data
        self.unread = unread
        if not date_created:
            self.dateCreated = datetime.utcnow().strftime("%Y/%m/%dT%H:%M:%SZ")
        else:
            self.dateCreated = date_created

    @staticmethod
    def new_offering_notification(receptor_name: str, data: dict = None):
        return Notification(_id=uuid.uuid4().__str__(),
                            action="New Search Hits",
                            status="Ok",
                            origin="i3-market",
                            receptor=receptor_name,
                            data=data)

    @staticmethod
    def update_offering_notification(receptor_name: str, data: dict = None):
        return Notification(_id=uuid.uuid4().__str__(),
                            action="Offering update",
                            status="Ok",
                            origin="i3-market",
                            receptor=receptor_name,
                            data=data)

    @staticmethod
    def agreement_notification(status, data: dict):
        return Notification(_id=uuid.uuid4().__str__(),
                            action="Agreement",
                            status=status,
                            origin=data.pop("OriginMarketId", "i3-market"),
                            receptor=data.pop("marketId", "i3-market"),
                            data=data)

    @staticmethod
    def consent_notification(status, data: dict):
        return Notification(_id=uuid.uuid4().__str__(),
                            action="Consent",
                            status=status,
                            origin=data.pop("OriginMarketId", "i3-market"),
                            receptor=data.pop("marketId", "i3-market"),
                            data=data)

    def to_json(self):
        json_out = {"id": self.id, "action": self.action, "status": self.status, "origin": self.origin,
                    "receptor": self.receptor, "unread": self.unread, "dateCreated": self.dateCreated}
        if hasattr(self, 'data'):
            json_out['data'] = self.data
        return json_out


def notification_to_object(data: dict):
    return Notification(
        data.get('id'),
        data.get('action'),
        data.get('status'),
        data.get('origin'),
        data.get('receptor'),
        data.get('data'),
        data.get('unread', True),
        data.get('dateCreated', None)
    )
