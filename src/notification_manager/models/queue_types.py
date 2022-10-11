from enum import Enum
from apiflask import Schema
from apiflask.fields import String, Integer, List
from apiflask.validators import Length, OneOf

# This is just for clarification
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
            "penaltyChoices",
            "agreeOnPenalty",
            "rejectPenalty"
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
    AGREEMENTPENALTYCHOICES= 'agreement.penaltychoices'
    AGREEMENTAGREEONPENALTY = 'agreement.agreeonpenalty'
    AGREEMENTREJECTPENALTY = 'agreement.rejectpenalty'

    @classmethod
    def is_valid(cls, name):
        return name in cls._value2member_map_



