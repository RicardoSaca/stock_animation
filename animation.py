import streamlit as st
from animate import animate_ticker

st.title('Demo of Animation with Matplotlib')

st.header('Animation of Stock Close Data')

col1, col2 = st.columns([10,5])
with col1:
    ticker = st.text_input("Input ticker symbol", 'TSLA', max_chars=7)
with col2:
    period = st.view = st.selectbox("Period",
            ('ytd','1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','max'))

plot = st.button('Animate')

if plot:
    with st.spinner(text='Animating in progress...'):
        st.markdown( animate_ticker(ticker, period), unsafe_allow_html=True)

st.markdown(""" \n\n\n""")

with st.expander("See explanation"):
    st.header('How does this applicatio work?')
    st.markdown("""
                This streamlit app is using two main components [`yfinance`](https://pypi.org/project/yfinance/) and [`matplotlib`](https://matplotlib.org/).\n
                It uses `yfinance` to gather the stock data, and `matplotlib` to chart the animation.\n
                ### Getting the Financial Data\n
                To get the financial data using yfinance we first initialize the stock using:\n
                `stock = yf.Ticker(ticker)`.\n
                Then we download the data into a pandas DataFrame using:\n
                `df = stock.history(interval='1d', period=period)`\n

                ### Doing the animation\n
                To create the anmation we use matplotlib's animation module, specifically the function [`FuncAnimation`](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html). 
                We first create are x and y variables, using the dataframe created earlier, along with initializing the plot:\n
                    x = df.index.values
                    y = df.Close.values
                    fig, ax = plt.subplots(figsize=(12,6))
                \n
                After this, we format the plot so it looks better:\n
                    #Format Dates for X axis ticks
                    dates = pd.to_datetime(df.index.values, format='%d/%b/%y')
                    dates = dates.to_pydatetime()
                    ax.tick_params(axis='x', labelrotation=45)
                    ax.set_xticks(dates)
                    ax.xaxis.set_major_locator(Ticker.MaxNLocator(20))
                    xmft = mdates.DateFormatter('%d/%b/%y')
                    ax.xaxis.set_major_formatter(xmft)
                    fig.autofmt_xdate()

                    #Format Y axis ticks
                    ax.yaxis.set_major_formatter('${x:,.0f}')

                    #Set chart xlim and ylim
                    xlim = (dates.min(), dates.max())
                    ylim = (y.min()-100, y.max()+100)
                    ax.set(xlim=xlim, ylim=ylim)

                    #Remove the right and top spines
                    ax.spines['right'].set_visible(False)
                    ax.spines['top'].set_visible(False)

                    #Set background color to white
                    plt.figure(facecolor='white')

                    #Set dynamic title
                    title = "{stock.info['shortName']} Close data from"
                    subtitle = f" {dates.min().strftime('%d/%b/%Y')} - {dates.max().strftime('%d/%b/%Y')}"
                    fig.suptitle(f"{title} {subtitle}" )
                \n
                The funcanimation takes the following `FuncAnimation(fig, animation_function, frames, interval, fargs, blit, save_count)`. [More info here](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html).\n
                Where:
                * fig is the figure we initialized
                * animation_function is a funtion that updates the graph with our frames of data
                * frames is the amount of frames
                * interval is the delay between frames in milliseconds
                * fargs are other arguments to pass our function animation
                * blit is to optimize the animation drawing
                * save_count is the fallback for the number of values from frames to cache.
                \n
                To plot the chart we then use the following code:\n
                    l, = ax.plot([],[])

                    def animate(i,x,y,l):
                        l.set_data(x[:i], y[:i])
                        return l,

                    animation = FuncAnimation(fig, func=animate, frames=x.shape[0], interval=100,
                                                fargs=[x,y,l], blit=True, save_count=0)
                \n

                We finally have to save the plot to be able to display it. [More info here](https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/).
                We use ffmpeg and html to save our animation which is then passed to our streamlit app.\n
                    writer = FFMpegWriter(fps=15)
                    html = animation.to_html5_video()
                    print(html[:50])
                    html = html.replace('width="1200" height="600"','width="900" height="450"')
                \n
                So this is the process I used to create an animation of stock closing prices.
                If you have any questions don't hesitate to reach out [here](https://ricardosaca.herokuapp.com/contactme)
                """)

