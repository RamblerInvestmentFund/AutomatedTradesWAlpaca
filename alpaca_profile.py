#connections with alpaca profile
import alpaca_trade_api as tradeapi
import time
import threading
import config

API_KEY = config.ALPACA_API_KEY
API_SECRET = config.ALPACA_SECRET_KEY
APCA_API_BASE_URL = config.ALPACA_ENDPOINT


class Profile():

    def __init__(self):
        self.api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

        self.r_positions = {}

    def clear_orders(self):
        try:
            self.api.cancel_all_orders()
            print("All open orders cancelled.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def add_items(self, data):
        ''' Expects a list of lists containing two items: symbol and position qty/pct
        '''
        for row in data:
            self.r_positions[row[0]] = [row[1], 0]

    def send_basic_order(self, sym, qty, side, order_type, time_in_force):
        qty = int(qty)
        if(qty == 0):
            return
        q2 = 0
        try:
            position = self.api.get_position(sym)
            curr_pos = int(position.qty)
            if((curr_pos + qty > 0) != (curr_pos > 0)):
                q2 = curr_pos
                qty = curr_pos + qty
        except BaseException:
            pass
        try:
            if q2 != 0:
                self.api.submit_order(symbol=sym, qty=abs(q2), side=side, type=order_type, time_in_force=time_in_force)
                try:
                    self.api.submit_order(symbol=sym, qty=abs(qty), side=side, type=order_type, time_in_force=time_in_force)
                except Exception as e:
                    print(
                        f"Error line 52: {str(e)}. Order of | {abs(qty) + abs(q2)} {sym} {side} | partially sent ({abs(q2)} shares sent).")
                    return False
            else:
                self.api.submit_order(symbol=sym, qty=abs(qty), side=side, type=order_type, time_in_force=time_in_force)
            print(f"Order of | {abs(qty) + abs(q2)} {sym} {side} | submitted.")
            return True
        except Exception as e:
            print(
                f"Error line 60: {str(e)}. Order of | {abs(qty) + abs(q2)} {sym} {side} | not sent.")
            return False

    def confirm_full_execution(self, sym, qty, side, expected_qty, order_type, time_in_force):
        sent = self.send_basic_order(sym, qty, side, order_type, time_in_force)
        if(not sent):
            return

        executed = False
        while(not executed):
            try:
                position = self.api.get_position(sym)
                if int(position.qty) == int(expected_qty):
                    executed = True
                else:
                    print(f"Waiting on execution for {sym}...")
                    time.sleep(20)
            except BaseException:
                print(f"Waiting on execution for {sym}...")
                time.sleep(20)
        print(
            f"Order of | {abs(qty)} {sym} {side} | completed.  Position is now {expected_qty} {sym}.")

    def timeout_execution(self, sym, qty, side, expected_qty, timeout, order_type, time_in_force):
        sent = self.send_basic_order(sym, qty, side, order_type, time_in_force)
        if(not sent):
            return
        output = []
        executed = False
        timer = threading.Thread(
            target=self.set_timeout, args=(
                timeout, output))
        timer.start()
        while(not executed):
            if(len(output) == 0):
                try:
                    position = self.api.get_position(sym)
                    if int(position.qty) == int(expected_qty):
                        executed = True
                    else:
                        print(f"Waiting on execution for {sym}...")
                        time.sleep(20)
                except BaseException:
                    print(f"Waiting on execution for {sym}...")
                    time.sleep(20)
            else:
                timer.join()
                try:
                    position = self.api.get_position(sym)
                    curr_qty = position.qty
                except BaseException:
                    curr_qty = 0
                print(
                    f"Process timeout at {timeout} seconds: order of | {abs(qty)} {sym} {side} | not completed. Position is currently {curr_qty} {sym}.")
                return
        print(
            f"Order of | {abs(qty)} {sym} {side} | completed.  Position is now {expected_qty} {sym}.")

    def set_timeout(self, timeout, output):
        time.sleep(timeout)
        output.append(True)


