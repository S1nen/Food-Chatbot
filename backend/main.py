from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import general_helper

app=FastAPI()


in_progress_orders={}

@app.post("/")
async def handle_request(request: Request):
        payload = await request.json()
        intent = payload["queryResult"]["intent"]["displayName"]
        parameters = payload["queryResult"]["parameters"]
        output_contexts = payload["queryResult"]["outputContexts"]

        session_id = general_helper.get_session_id(output_contexts[0]["name"])



        intent_handler_dict = {
            "Add Order-context:ongoing-order": add_to_order,
            "remove order-context:ongoing-order": remove_from_order,
            "Order complete-context:ongoing-order": complete_order,
            "Track Order-context:ongoing-order": track_order,
            "Cancel order":cancel_order,
            "New Order":new_order
        }

        return intent_handler_dict[intent](parameters, session_id)




def new_order(parameters:dict,session_id:str):
    if session_id in in_progress_orders:
        del in_progress_orders[session_id]
    return JSONResponse(content={"fulfillmentText":"Ok, starting a new order. You can say things like 'I want two pizzas and one Chocolate Milkshake'."
                                 " Make sure to specify a quantity for every food item!" 
                                 " Also, we have only the following items on our menu: Burger, Fried Rice, Pizza, Mango Lassi, Chicken Sandwich, Veg Sandwich, Chocolate Milkshake, Caramel Cake, Strawberry Pancake and Loaded Fries."
                                 })




def add_to_order(parameters:dict,session_id:str):
    food_items = parameters.get("Food-Item")
    quantities = parameters.get("number")

    if len(food_items) != len(quantities):
        fulfillment_text="Sorry I didn't understand. Can you please specify food items and quantities clearly!"
    else:
        new_food_dict=dict(zip(food_items,quantities))

        if session_id in in_progress_orders:
            current_food_dict=in_progress_orders[session_id]
            current_food_dict.update(new_food_dict)
            in_progress_orders[session_id]=current_food_dict
        else:
            in_progress_orders[session_id]=new_food_dict

        order_str=general_helper.get_values_from_food_dict(in_progress_orders[session_id])
        fulfillment_text=f"So far you have:{order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })





def remove_from_order(parameters: dict, session_id: str):
    if session_id not in in_progress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters["food-item"]
    current_order = in_progress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = general_helper.get_values_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}, You need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })





def complete_order(parameters:dict,session_id:str):
    if session_id not in in_progress_orders:
        fulfillment_text="Sorry, I am having trouble finding your order. Can you place a new order please?"
    else:
        order=in_progress_orders[session_id]
        order_id=save_to_db(order)

        if order_id==-1:
            fulfillment_text="Sorry, I couldn't process your order due to a backend error."\
            "Please place a new order again"

        else:
            order_total=db_helper.get_total_price(order_id)
            fulfillment_text=f"We have successfully placed your order."\
            f" Here is your order id: #{order_id}. "\
            f"Your order total is {order_total}, which you can pay at the time of delivery. Thank You."

        del in_progress_orders[session_id]
    return JSONResponse(content={
        "fulfillmentText":fulfillment_text
    })





def save_to_db(order:dict):
    next_order_id=db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        record=db_helper.insert_order_item(
            food_item,quantity,next_order_id
        )

        if record==-1:
            return -1
    db_helper.insert_order_tracking_state(next_order_id,"In progress")


    return next_order_id





def track_order(parameters: dict,session_id:str):
    order_id=int(parameters.get("number"))
    order_status=db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text=f"The order status for order id {order_id} is: {order_status}"
    else:
        fulfillment_text=f"No order found with order id : {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })





def cancel_order(parameters:dict,order_id:int):
    order_id=int(parameters.get("number"))
    id_order=db_helper.get_id_from_db(order_id)
    if not id_order:
        fulfillment_text=f"Order not found with the given id {order_id}, Place a new order"
    else:
        db_helper.delete_from_db(order_id)
        fulfillment_text=f"Your Order with id #{order_id} is Successfully Cancelled "
    return JSONResponse(content={
        "fulfillmentText":fulfillment_text
    })
