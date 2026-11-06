import random
import logging

class TradingEngine:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.is_running = False
        self.positions = {}
        self.cash = 100000.0

    def start(self):
        self.is_running = True
        logging.info("量化交易核心引擎已启动")

    def stop(self):
        self.is_running = False
        logging.info("量化交易核心引擎已停止")

    def evaluate_and_trade(self):
        if not self.is_running:
            return None
        candidates = [
            ("600519", "贵州茅台", 1520.0),
            ("300750", "宁德时代", 210.3),
            ("002594", "比亚迪", 265.8),
            ("000858", "五粮液", 138.5)
        ]
        if random.random() > 0.5:
            code, name, price = random.choice(candidates)
            volume = 100
            total_amount = price * volume
            if self.cash >= total_amount:
                self.cash -= total_amount
                if code in self.positions:
                    old_vol = self.positions[code]["vol"]
                    old_cost = self.positions[code]["cost"]
                    new_vol = old_vol + volume
                    new_cost = (old_vol * old_cost + total_amount) / new_vol
                    self.positions[code] = {"name": name, "vol": new_vol, "cost": new_cost, "price": price}
                else:
                    self.positions[code] = {"name": name, "vol": volume, "cost": price, "price": price}
                msg = f"【买入成交】{name}({code}) {volume}股 @ ¥{price:.2f}，成交额: ¥{total_amount:,.2f}"
                logging.info(msg)
                if self.db_manager:
                    self.db_manager.log_trade(msg, "TRADE")
                return {"action": "BUY", "code": code, "name": name, "vol": volume, "price": price, "cash": self.cash}
        return None

