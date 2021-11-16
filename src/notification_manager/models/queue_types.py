import json
from enum import Enum
from apiflask import Schema
from apiflask.fields import String, Integer, List
from apiflask.validators import Length, OneOf

channels = {
    "offering": {
        "new",
        "update",
    },
    "smartcontract": {
        "agreement":
        {
            "accepted",
            "update",
            "pending",
            "termination",
            "claim",
        },
    }
}


class QueueType(Enum):
    NEWOFFERING = 'offering.new'
    UPDATEOFFERING = 'offering.update'

    AGREEMENTACCEPTED = 'agreement.accepted'
    AGREEMENTREJECTED = 'agreement.rejected'
    AGREEMENTUPDATE = 'agreement.update'
    AGREEMENTPENDING = 'agreement.pending'
    AGREEMENTTERMINATION = 'agreement.termination'
    AGREEMENTCLAIM = 'agreement.claim'

    @classmethod
    def is_valid(cls, name):
        return name in cls._value2member_map_



