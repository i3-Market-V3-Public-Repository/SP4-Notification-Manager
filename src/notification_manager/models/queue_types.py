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
            "rejectPenalty",
            'terminationproposal',
            'terminationrejection'
        },
        "consent": {
            'given',
            'revoked'
        }
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
    AGREEMENTPROPOSEPENALTY= 'agreement.proposepenalty'
    AGREEMENTAGREEONPENALTY = 'agreement.agreeonpenalty'
    AGREEMENTREJECTPENALTY = 'agreement.rejectpenalty'
    AGREEMENTTERMINATIONPROPOSAL = 'agreement.terminationproposal'
    AGREEMENTTERMINATIONREJECTION = 'agreement.terminationrejection'

    CONSENTGIVEN = 'consent.given'
    CONSENTREVOKED = 'consent.revoked'
    @classmethod
    def is_valid(cls, name):
        return name in cls._value2member_map_



