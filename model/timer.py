class timer:
    # 开关
    on_off = False
    # 次数
    count = 0

    def on(self):
        self.on_off = True
    
    def off(self):
        self.on_off = False
    
    def increment(self):
        self.count += 1
    
    def reset(self):
        self.count = 0
    
    def getCount(self):
        return self.count