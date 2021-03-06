"""
This file houses the customer board interface.
It is used to interact with the customer profile database for boards.
"""
from bson.objectid import ObjectId
from modules.database import QueryFailureException, UpdateFailureException
from modules.owner.restaurant_profile_manager import RestaurantProfileManager


def check_bingo(board, completed_indices, size):
    """
	Helper function to update a board with the customer's bingos.
	"""
    a_diag = size - 1
    d_diag = size + 1
    ranges = [[]]
    for i in range(1, size + 1):
        ranges[0].append(a_diag * i)
    for i in range(0, size * size, size):
        ranges.append([x for x in range(i, i + size)])
    for i in range(size):
        ranges.append([x for x in range(size * size) if x % size == i])
    ranges.append([])
    for i in range(0, size):
        ranges[-1].append(d_diag * i)

    if len(completed_indices) == size * size:
        board["board"][0]["board_complete"] = True
    count = 0
    for rang in ranges:
        is_bingo = True
        for i in rang:
            if i not in completed_indices:
                is_bingo = False
        if is_bingo:
            for i in rang:
                board["board"][i]["is_bingo"] = True
                board["board_reward"][count]["is_earned"] = True
        count += 1


def set_board_progress(cpm, board, rest_id):
    """
	Given a board and restaurant id, update a board with the customer's progress.
	"""
    try:
        rest_id = ObjectId(rest_id)

        # assign incomplete for all goals initially
        for i in range(len(board["board"])):
            board["board"][i]["is_complete"] = False

        # assign "not bingo" for all goals initially
        for i in range(len(board["board"])):
            board["board"][i]["is_bingo"] = False

        # assign "not earned" for all rewards initially
        for i in range(len(board["board_reward"])):
            board["board_reward"][i]["is_earned"] = False

        # assign complete for all goals the customer completed
        # assign bingo for all goals that make up a bingo that the customer completed
        # assign earned for all rewards that are earned
        customer = cpm.db.query("customers", {"username": cpm.id})[0]
        if "progress" in customer:
            for restaurant in customer["progress"]:
                if restaurant["restaurant_id"] == rest_id:
                    for goal in restaurant["completed_goals"]:
                        completed_index = [
                            int(x["position"])
                            for x in restaurant["completed_goals"]
                        ]
                        index = int(goal["position"])
                        if board["board"][index]["_id"] == goal["_id"]:
                            board["board"][index]["is_complete"] = True
                            check_bingo(board, completed_index,
                                        board["size"])

    except QueryFailureException:
        print("Something's wrong with the query.")
    except IndexError:
        print("Could not find the customer")


def reset_complete_board(cpm, rest_id):
    """
	Clears the bingo board once the entire board has been filled.
	"""
    try:
        cpm.db.update('customers', {
            "username": cpm.id,
            "progress.restaurant_id": rest_id
        }, {"$set": {
            "progress.$.completed_goals": []
        }})
    except UpdateFailureException:
        print("There was an issue updating")


def get_reward_progress(cpm):
    """
	Return the current user's reward history as a tuple of two lists:
	([active rewards], [redeemed rewards]).
	Returns ([], []) on failure.
	"""
    try:
        customer = cpm.db.query("customers", {"username": cpm.id})[0]

        # no game progress
        if "progress" not in customer:
            return ([], [])

        active_rewards = []
        redeemed_rewards = []
        for resaurant in customer["progress"]:

            # no rewards completed at this restaurant
            if "completed_rewards" not in resaurant:
                continue

            restaurant_name = RestaurantProfileManager(
                "").get_restaurant_name_by_id(resaurant["restaurant_id"])

            # add rewards to appropriate collection
            for reward in resaurant["completed_rewards"]:
                reward["restaurant_name"] = restaurant_name
                if reward["is_redeemed"]:
                    redeemed_rewards.append(reward)
                else:
                    active_rewards.append(reward)

        # sort redeemed rewards by date
        redeemed_rewards = sorted(redeemed_rewards,
                                  key=lambda x: x["redemption_date"],
                                  reverse=True)

        # format all dates
        for index, reward in enumerate(redeemed_rewards):
            redeemed_rewards[index]["redemption_date"] = reward[
                "redemption_date"].strftime("%B X%d, %Y").replace("X0", "X").replace("X", "")

        return (active_rewards, redeemed_rewards)

    except QueryFailureException:
        print("Something's wrong with the query.")
        return ([], [])
    except IndexError:
        print("Could not find the customer")
        return ([], [])
