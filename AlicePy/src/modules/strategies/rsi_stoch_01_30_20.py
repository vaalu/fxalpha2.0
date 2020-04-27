import ta

def RSI(close,timePeriod):    
    rsi = ta.RSI(close,timePeriod)
    rsiSell = (rsi>70) & (rsi.shift(1)<=70)
    rsiBuy = (rsi<30) & (rsi.shift(1)>=30)
    return rsiSell,rsiBuy, rsi

def Stoch(close,high,low):    
    slowk, slowd = ta.STOCH(high, low, close)
    stochSell = ((slowk < slowd) & (slowk.shift(1) > slowd.shift(1))) & (slowd > 80)
    stochBuy = ((slowk > slowd) & (slowk.shift(1) < slowd.shift(1))) & (slowd < 20)
    return stochSell,stochBuy, slowk,slowd