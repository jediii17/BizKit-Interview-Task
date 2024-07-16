from flask import Blueprint, request

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args), 200


def search_users(args):
    results = []

    # Extract query parameters
    search_id = args.get("id")
    search_name = args.get("name")  # case insensitive
    search_age = args.get("age")
    search_occupation = args.get("occupation")  # case insensitive

    # Convert search_age to int if it exists
    if search_age:
        try:
            search_age = int(search_age)
        except ValueError:
            search_age = None

    # Iterate over USERS and apply filters
    for user in USERS:
        user_id = user["id"]
        user_name = user["name"].lower()
        user_age = user["age"]
        user_occupation = user["occupation"].lower()

        parArr = [search_id, search_name, search_age, search_occupation]
        valueArr = [user_id, user_name, user_age, user_occupation]
        # Check if user should be included based on search criteria
        include_user = False

        ctr = 0
        for argsG in parArr:
            # check only the args that has a value from the link
            if argsG is not None:
                # if index is for user_Age
                if ctr == 2 and user_age:
                    if user_age >= search_age - 1 and user_age <= search_age + 1:
                        include_user = True
                        break
                elif argsG.lower() in valueArr[ctr].lower():
                    include_user = True
                    break

            ctr = ctr + 1

        # Add user to results if all criteria match
        if include_user:
            results.append(user)

    return results


