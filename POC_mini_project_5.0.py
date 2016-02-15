"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(50)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000
# SIM_TIME = 1000000000
# SIM_TIME = 16

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies = 0.0
        self._total_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        current_state = "Time: " +\
        str(int(self._time)) + " " + "Current Cookies: " +\
        str(self._cookies) + " " + "CPS: " + \
        str(self._cps) + " " + "Total Cookies: " + \
        str(self._total_cookies) + " " + "History: " +\
        str(self._history_list)
        return current_state
    
    def print_history(self):
        """
        Prints the full history of purchases
        """
        history_string = ""
        for dummy_list in self._history_list:
            history_string += ("Purchase: " + str(dummy_list) + "\n")
        return history_string
    
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history_list)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        cookie_difference = cookies - self._cookies
        if cookie_difference > 0:
            return math.ceil(cookie_difference / self._cps)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
        # Increment the time, the current cookie and the
        # total number of cookie
            self._time += time
            self._cookies += (self._cps * time)
            self._total_cookies += (self._cps * time)
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies >= cost:
            
            # Append the item to history list
            self._history_list.append((self._time, item_name, cost, self._total_cookies))
            
            # Decrease the amount of current cookies
            self._cookies -= cost
            
            # Increase the additional CpS
            self._cps += additional_cps
            
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy. Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    # Clones the build info class and make initializations
    build_info_clone = build_info.clone()
    clicker_state = ClickerState()
    
    # Check whether the simulation time has passed
    while clicker_state.get_time() <= duration:
        
        # Update the strategy
        strategies = strategy(clicker_state.get_cookies(), clicker_state.get_cps(),\
                              clicker_state.get_history(), duration - clicker_state.get_time(),\
                              build_info_clone)
        
        # If there is no strategies left, return the remaining duration left
        # and exit out of the loop
        if strategies == None:
            clicker_state.wait(duration - clicker_state.get_time())
            return clicker_state
        
        # Compute the required wait time until the next purchase
        wait_time = clicker_state.time_until(build_info_clone.get_cost(strategies))
        
        # If the wait time is more than the duration left, then change wait time to the time of
        # the remaining duration
        if wait_time > (duration - clicker_state.get_time()):
            clicker_state.wait(duration - clicker_state.get_time())
            return clicker_state
        
        # Update the state of the clicker state
        clicker_state.wait(wait_time)
            
        # Buy item if we have enough money, do nothing if not
        clicker_state.buy_item(strategies, build_info_clone.get_cost(strategies), build_info_clone.get_cps(strategies))
        
        # Update the state of the bought item
        build_info_clone.update_item(strategies)
        
    return clicker_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return 'Cursor'

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    
    # Initialize for minimum possible
    min_cost = float('+inf')
    item_selected = None
    
    # Iterates through the list of buildable items to get
    # the cheapest out of the list
    for dummy_item in build_info.build_items():
        
        # Calculate the wait time needed for the current item
        wait_time = math.ceil((build_info.get_cost(dummy_item) - cookies) / cps)
        
        # Check if the selected item is less than the total cost
        # also check if the item can be bought at the required time
        # also check if we can afford the item (don't have to wait)
        if (build_info.get_cost(dummy_item) <= min_cost) and (wait_time <= time_left):
            item_selected = dummy_item
            min_cost = build_info.get_cost(dummy_item)
            
    return item_selected

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    
    # Initialize some variables
    max_cost = float('-inf')
    item_selected = None
    
    # Iterates through the list of buildable items to get
    # the most expensive that is affordable on the list
    for dummy_item in build_info.build_items():
        
        # Calculate the wait time needed for the current item
        wait_time = math.ceil((build_info.get_cost(dummy_item) - cookies) / cps)
        
        # Check if the selected item is more than the total cost
        # also check if there is time left and check if we can
        # buy the item
        if (build_info.get_cost(dummy_item) >= max_cost) and (wait_time <= time_left):
            item_selected = dummy_item
            max_cost = build_info.get_cost(dummy_item)
    
    return item_selected

def strategy_best_mod3(cookies, cps, history, time_left, build_info):
    """
    This strategy will make a purchase that will double the cps
    using the cheapest amount possible
    """
    
    selected_item = None
    max_cps = float('-inf')
    min_cost = float('+inf')
    max_expected_earnings = float('-inf')
    
    for dummy_item in build_info.build_items():
        
        # Calculate the cost
        cost = build_info.get_cost(dummy_item)
        wait_time = math.ceil((cost - cookies) / cps)
        if wait_time < 0:
            wait_time = 0
        cps_expected = cps + (build_info.get_cps(dummy_item))
        expected_earnings = cps_expected * (time_left - wait_time)
        
        if (cps_expected >= max_cps) and (wait_time <= time_left) and (cost <= min_cost) and (max_expected_earnings <= expected_earnings):
            max_cps = cps_expected
            selected_item = dummy_item
            min_cost = cost
            max_expected_earnings = expected_earnings
    
    return selected_item

def strategy_best_mod(cookies, cps, history, time_left, build_info):
    """
    This strategy will make a purchase that will double the cps
    using the cheapest amount possible
    """
    
    selected_item = None
    max_cps = float('-inf')
    min_cost = float('+inf')
    max_expected_earnings = float('-inf')
    
    for dummy_item in build_info.build_items():
        
        # Calculate the cost
        cost = build_info.get_cost(dummy_item)
        wait_time = math.ceil((cost - cookies) / cps)
        cps_expected = cps + (build_info.get_cps(dummy_item))
        expected_earnings = cps_expected * (time_left - wait_time)
        
        if (cps_expected >= max_cps) and (wait_time <= time_left) and (cost <= min_cost) and (max_expected_earnings <= expected_earnings):
            max_cps = cps_expected
            selected_item = dummy_item
            min_cost = cost
            max_expected_earnings = expected_earnings
        elif (wait_time <= 0):
            selected_item = dummy_item
    
    return selected_item

def strategy_best_mod2(cookies, cps, history, time_left, build_info):
    """
    This strategy will make a purchase that will double the cps
    using the cheapest amount possible
    """
    
    selected_item = None
    max_cps = float('-inf')
    min_cost = float('+inf')
    max_expected_earnings = float('-inf')
    
    for dummy_item in build_info.build_items():
        
        # Calculate the cost
        cost = build_info.get_cost(dummy_item)
        wait_time = math.ceil((cost - cookies) / cps)
        cps_expected = cps + (build_info.get_cps(dummy_item))
        expected_earnings = cps_expected * (time_left - wait_time)
        
        if (wait_time <= 0) and (max_expected_earnings <= expected_earnings):
            max_expected_earnings = expected_earnings
            selected_item = dummy_item
        elif (cps_expected >= max_cps) and (wait_time <= time_left) and (cost <= min_cost) and (max_expected_earnings <= expected_earnings):
            max_cps = cps_expected
            selected_item = dummy_item
            min_cost = cost
            max_expected_earnings = expected_earnings
            
    return selected_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    This strategy will make a purchase that will double the cps
    using the cheapest amount possible
    """
    
    selected_item = None
    max_fom = float('-inf')
    
    build_items_list = list([])
    
    for dummy_build_items in build_info.build_items():
        
        wait_time = math.ceil((build_info.get_cost(dummy_build_items) - cookies) / cps)
        if wait_time <= 0:
            wait_time = 0
        
        if wait_time <= time_left:
            build_items_list.append((dummy_build_items, wait_time))

    for dummy_build_items in build_items_list:
        
        # This is the new figure of merit strategy
        # Less wait time, more cps
        if dummy_build_items[1] == 0:
            fom = float('+inf')
        else:
            fom = build_info.get_cps(dummy_build_items[0]) / dummy_build_items[1]
        
        # Checks for maximum fom
        if (fom >= max_fom):
            max_fom = fom
            selected_item = dummy_build_items[0]
            
    return selected_item

def strategy_double(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    This strategy looks at the expected earnings over a long
    period of time and compares which has the most earnings.
    Also checks whether the earnings are affordable
    """
    
    # Initializations of variables
    max_earnings = float('-inf')
    item_selected = None
    
    # Test over the number of possible purchases with the alloted time
    for dummy_item in build_info.build_items():
        
        # Calculate the wait time and the expected earnings and cost
        cost = build_info.get_cost(dummy_item)
        wait_time = math.ceil((cost - cookies)/ cps)
        expected_earnings = (time_left - wait_time) * (cps + build_info.get_cps(dummy_item))
        
        # Check whether the expected earnings can be selected
        # Also checks whether there is enough time left
        if (expected_earnings >= max_earnings) and (wait_time < time_left):
            max_earnings = expected_earnings
            item_selected = dummy_item
    
    return item_selected

def strategy_grandma_broken(cookies, cps, history, time_left, build_info):
    """
    This strategy will always return grandma.
    """
    
    return "Grandma"

def strategy_farm_broken(cookies, cps, history, time_left, build_info):
    """
    This Strategy will always return farm.
    """
    
    return "Farm"

def strategy_factory_broken(cookies, cps, history, time_left, build_info):
    """
    This Strategy will always return factory.
    """
    
    return "Factory"

def strategy_mine_broken(cookies, cps, history, time_left, build_info):
    """
    This strategy will always return mine.
    """
    
    return "Mine"

def strategy_shipment_broken(cookies, cps, history, time_left, build_info):
    """
    This strategy will always return shipment.
    """
    
    return "Shipment"

def strategy_alchemy_broken(cookies, cps, history, time_left, build_info):
    """
    This strategy will always return alchemy.
    """
    
    return "Alchemy Lab"

def strategy_portal_broken(cookies, cps, history, time_left, build_info):
    """
    This strategy will always return portal.
    """
    
    return "Portal"

def strategy_time_machine_broken(cookies, cps, history, time_left, build_info):
    """
    This strategy will always return time machine.
    """
    
    return "Time Machine"

def strategy_condenser_broken(cookies, cps, history, time_left, build_info):
    """
    This strategy will always return anti matter condenser.
    """
    
    return "Antimatter Condenser"

def strategy_fom(cookies, cps, history, time_left, build_info):
    """
    This strategy computes the best strategy by the following
    process.
    
    To make the first purchase, we will take the time remaining and
    the wait time and subtract them to make the remainder time,
    we then get the extra cps of the purchase and multiply
    the cps * time_remainder to get the figure of merit.
    
    Select the ones with the highest figure of merit.
    """
    
    # Initialize variables
    figure_of_merit = float('-inf')
    item_selected = None
    
    # Reiterates over the items inside the list
    for dummy_items in build_info.build_items():
        
        wait_time = math.ceil((build_info.get_cost(dummy_items) - cookies) / cps)
        if wait_time < 0:
            wait_time = 0.0
        time_remaining = time_left - wait_time
        cps_expected = build_info.get_cps(dummy_items)
        fom = cps_expected * time_remaining
        
        if (fom >= figure_of_merit) and (wait_time <= time_left):
            figure_of_merit = fom
            item_selected = dummy_items
            
    return item_selected

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time
    
    # print state.print_history()

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)
    
def run():
    """
    Run the simulator.
    """
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # run_strategy("None", SIM_TIME, strategy_none)
    # run_strategy("Cheapest", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    # run_strategy("Best Mod", SIM_TIME, strategy_best_mod)
    # run_strategy("Best Mod2", SIM_TIME, strategy_best_mod2)
    # run_strategy("Best Mod3", SIM_TIME, strategy_best_mod3)
    # run_strategy("Double", SIM_TIME, strategy_double)
    # run_strategy("Grandma", SIM_TIME, strategy_grandma_broken)
    # run_strategy("Farm", SIM_TIME, strategy_farm_broken)
    # run_strategy("Factory", SIM_TIME, strategy_factory_broken)
    # run_strategy("Mine", SIM_TIME, strategy_mine_broken)
    # run_strategy("Shipment", SIM_TIME, strategy_shipment_broken)
    # run_strategy("Alchemy Lab", SIM_TIME, strategy_alchemy_broken)
    # run_strategy("Portal", SIM_TIME, strategy_portal_broken)
    # run_strategy("Time Machine", SIM_TIME, strategy_time_machine_broken)
    # run_strategy("Antimatter Condenser", SIM_TIME, strategy_condenser_broken)
    # run_strategy("FOM", SIM_TIME, strategy_fom)
    
run()
