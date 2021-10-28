import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as Ticker
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation, FFMpegWriter
import yfinance as yf

def get_ticker_data(ticker='TSLA', period='ytd'):
    try:
        stock = yf.Ticker(ticker)
        if period in ['5y','10y','max']:
            df =stock.history(interval='1wk', period=period)
        else:
            df = stock.history(interval='1d', period=period)
        return df, stock
    except:
        return print('Stock ticker not working, please double check and try again')

def animate_ticker(ticker='TSLA', period='ytd'):
    plt.switch_backend('Agg')
    plt.rcParams['animation.html'] = 'jshtml'
    df, stock = get_ticker_data(ticker, period)
    dates = pd.to_datetime(df.index.values, format='%d/%b/%y')
    dates = dates.to_pydatetime()
    x = df.index.values
    y = df.Close.values
    fig, ax = plt.subplots(figsize=(12,6))

    ax.tick_params(axis='x', labelrotation=45)
    ax.set_xticks(dates)
    ax.xaxis.set_major_locator(Ticker.MaxNLocator(20))
    ax.yaxis.set_major_formatter('${x:,.0f}')
    xmft = mdates.DateFormatter('%d/%b/%y')
    ax.xaxis.set_major_formatter(xmft)
    fig.autofmt_xdate()

    xlim = (dates.min(), dates.max())
    ylim = (y.min()-100, y.max()+100)
    ax.set(xlim=xlim, ylim=ylim)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    l, = ax.plot([],[])

    plt.figure(facecolor='white')
    fig.suptitle(f"{stock.info['shortName']} Close data\nfrom {dates.min().strftime('%d/%b/%Y')} - {dates.max().strftime('%d/%b/%Y')}")

    def animate(i,x,y,l):
        l.set_data(x[:i], y[:i])
        return l,

    animation = FuncAnimation(fig, func=animate, frames=x.shape[0], interval=100,
                                fargs=[x,y,l], blit=True, save_count=0)

    writer = FFMpegWriter(fps=15)
    html = animation.to_html5_video()
    print(html[:50])
    html = html.replace('width="1200" height="600"','width="900" height="450"')
    return html
