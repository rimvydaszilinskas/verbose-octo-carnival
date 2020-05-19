# Ticketing

`./bin/kafka-topics.sh --create --zookeeper ticketing_zookeeper:2181 --replication-factor 1 --partitions 1 --topic tickets`

## Topics & env

|Variable|Default|
|-|-|
|TICKET_CREATION_TOPIC|tickets|
|TICKET_CREATION_MESSAGE_TYPE|tickets|
|NEW_SALE_TOPIC|sales|
|NEW_SALE_MESSAGE_TYPE|sales|
|ACCOUNTING_SALE_TOPIC|acc_sales|
|ACCOUNTING_SALE_MESSAGE_TYPE|acc_sales|

### Create tickets message

```json
{
    "rows":50,
    "columns":12,
    "flight":"id"
}
```

### New sale message

```json
{
	"customer_reference": "?????",
	"tickets": [
		{
			"uuid": "valid_uuid",
			"name": "name",
			"ref": "?????",

		}
	]
}
```

### Sale update message

```json
{
	"uuid": "valid_uuid",
	"status": "paid"
}
```

### Sale creation alert

```json
json:{
    "type":"acc_sales",
    "version":1,
    "message":
        {
            "uuid":"5c86c2bf48bb4f128c0c0eff3e2d3651",
            "paid":false,
            "customer":"iadsbjudasniudasmniadsnuasdfbnusgbnjafnsjndas",
            "tickets":{
                "passsenger":1,
                "business":1,
                "first":1
            }
        }
    }
```

### Create new tickets

```json
{
    "rows": 3,
    "columns": 2,
    "flight": "1234",
    "classes": [
        {
            "class_type": "1",
            "rows": [
                1
            ]
        },
           {
            "class_type": "2",
            "rows": [
                2
            ]
        },
    ]
}
```

This will create:

```
1A 1B - Business class
2A 2B - First class
3A 3B - Passenger class
```