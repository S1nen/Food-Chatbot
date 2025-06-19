import re

def get_session_id(session_str:str):
    match=re.search(r"/sessions/(.*?)/contexts/",session_str)
    if match:
        extracted_string=match.group(1)
        return extracted_string
    return ""




def get_values_from_food_dict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])


if __name__=="__main__":
    print(get_values_from_food_dict({"Pizza":3,"mango lassi":2}))
    # print(get_session_id(("projects/chatbot-aqdb/agent/sessions/e6249167-79c6-4c04-95ff-a999b548964e/contexts/ongoing-order")))
