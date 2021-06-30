# [i3-market] Notification Manager

_en construcción..._
## Notifications API examples
Gived information about examples of Notifications (Not currently used)

sendNotification(action, status, origin, receptor, data)

* Notification (action, status, origin, receptor, data)

* Notification (action: New Search Hits, status: OK, origin: i3-market, receptor: datamarketplace_consumer, data = search results)

* Notification (action: Data Purchase Request, status: ok, origin: datamarketplace_provider, receptor: i3-Market)

* Notification (action: Data Purchase Request, status: Reject, origin: datamarketplace_provider, receptor: i3-Market)
 
* Notification (action: Accept Proposal, status: ok, origin: datamarketplace_provider, receptor: i3-Market, data = contractual parameters)

* Notification (action: Accept Proposal, status: Reject, origin: datamarketplace_provider, receptor: i3-Market)

* Notification (action: Activate Agreement, status: pending, origin: i3-Market, receptor: datamarketplace_consumer)

* Notification (action: Activate Agreement, status: ok, origin: i3-market, receptor: datamarketplace_provider, datamarketplace_consumer)

## Notification API Examples 2
Define in swagger the next methods:
GETTER METHODS:

* /v1/subscriptions retrieve al subscriptions

* /v1/subscriptions/<subscription_id> retrieve subscriptions by id

* /v1/subscriptions/user/<user_id> retrieve al user subscriptions    

New offering notification

method: POST

url: /v1/offering/notify

body:

```{
  "active": "yes",
  "dataOffering": "i3market",
  "category": "iot",
  "description": "test offering for i3market",
  "hasDataset": [
    {
      "accrualPeriodicity": " accuralPriodicity-13market",
      "creator": "qaiser",
      "dataset": "13market-dataset",
      "description": "dataset about 13market",
      "distribution": [
        {
          "accessService": [
            {
              "conformsTo": "confomrsTo-13market",
              "endpointDescription": "13market endpoint description",
              "endpointURL": "http://13market.org",
              "servesDataset": "servesdataset-13market",
              "serviceSpecs": "servicespace-13market"
            }
          ],
          "conformsTo": "conformsto-distribution-13market",
          "description": "distribution-description-13market",
          "distribution": "13market distribution",
          "license": "apache",
          "mediaType": "13market media type",
          "packageFormat": "13market package",
          "title": "distribution title 13market"
        }
      ],
      "issued": "2021-05-10T13:58:26.671Z",
      "language": "rdf",
      "modified": "2021-05-10T13:58:26.671Z",
      "spatial": "spatial-13market",
      "temporal": "temporal-13market",
      "temporalResolution": "temporlaResolution-13market",
      "theme": [
        "13market them"
      ],
      "title": "dataset title for 13market"
    }
  ],
  "hasPricingModel": [
    {
      "basicPrice": "20",
      "currency": "euro",
      "hasPaymentType": [
        {
          "fromValue": "2021-05-10T13:58:26.671Z",
          "hasSubscriptionPrice": "2",
          "paymentType": "cash",
          "repeat": "weekly",
          "timeDuration": "one year",
          "toValue": "2021-05-10T13:58:26.671Z"
        }
      ]
    }
  ],
  "isProvidedBy": "888888id",
  "label": "dataoffering label",
  "license": "dataoffering license",
  "title": "dataoffering title"
}
```

**Not Defined currently**

* /v1/offering/purchase()

* /v1/offering/proposal/reject()

* /v1/offering/proposal/accept()

* /v1/offering/proposal/agreement()

* /v1/offering/agreement/accept()


## UML

![UML1](docs/uml_1.png)
![UML2](docs/uml_2.png)
![UML3](docs/uml_3.png)

## Maintainers

- [diego.s](mailto:diego.s@hopu.org) - Software engineer and Data scientist
- [eleazar](mailto:eleazar@hopu.eu) - Software engineer