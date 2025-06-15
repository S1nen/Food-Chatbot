from statistics import quantiles

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
app=FastAPI()

"""
@app.post("/")
async def handle_request(request: Request):
    try:
        payload = await request.json()
        intent = payload["queryResult"]["intent"]["displayName"]
        parameters = payload["queryResult"]["parameters"]

        if intent == "Track Order-context:ongoing-order":
            return track_order(parameters)

        return JSONResponse(content={
            "fulfillmentText": f"Sorry, I don't handle the intent: {intent}"
        })

    except Exception as e:
        return JSONResponse(content={
            "fulfillmentText": f"Error occurred: {str(e)}"
        })


def track_order(parameters: dict):
    try:
        order_id = int(parameters.get("order_id"))
        order_status = db_helper.get_order_status(order_id)

        if order_status:
            fulfillment_text = f"The order status for order id {order_id} is: {order_status}"
        else:
            fulfillment_text = f"No order found with order id {order_id}"

        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    except Exception as e:
        return JSONResponse(content={"fulfillmentText": f"Error: {str(e)}"})
"""



@app.post("/")
async def handle_request(request: Request):
    payload=await request.json()
    intent=payload["queryResult"]["intent"]["displayName"]
    parameters=payload["queryResult"]["parameters"]
    output_contexts=payload["queryResult"]["outputContexts"]

    intent_handler_dict={
        "Add Order-context:ongoing-order":add_to_order,
        # "remove order-context:ongoing-order":remove_from_order,
        # "Order complete-context:ongoing-order":complete_order,
        "Track Order-context:ongoing-order":track_order
    }

    return intent_handler_dict[intent](parameters)


def add_to_order(parameters:dict):
    food_items=parameters.get("Food-Item")
    quantities=parameters.get("number")

    if len(food_items) != len(quantities):
        fulfillment_text="Sorry I didn't understand. Can you please specify food items and quantities clearly!"
    else:
        fulfillment_text=f"Order received for {food_items} - {quantities}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def track_order(parameters: dict):
    order_id=int(parameters.get("number"))
    order_status=db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text=f"The order status for order id {order_id} is:{order_status}"
    else:
        fulfillment_text=f"No order found with order id : {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper

app = FastAPI()


@app.post("/")
async def handle_request(request: Request):
    try:
        payload = await request.json()
        print("Payload received:", payload)  # 🧪 Log input

        intent = payload["queryResult"]["intent"]["displayName"]
        parameters = payload["queryResult"]["parameters"]
        print("Intent:", intent)
        print("Parameters:", parameters)

        if intent == "Track Order-context:ongoing-order":
            return track_order(parameters)
        else:
            return JSONResponse(content={"fulfillmentText": "Intent not handled."})

    except Exception as e:
        import traceback
        traceback.print_exc()  # 🧪 Log full error in the terminal
        return JSONResponse(status_code=500, content={"error": str(e)})




def track_order(parameters: dict):
    # Fix: Dialogflow sends 'number' not 'order_id'
    order_id = parameters.get("number")

    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id {order_id}"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

"""