import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

st.set_page_config(layout="wide")
st.title("Tank Optimisation Visualiser")
graph_type = st.selectbox("Select Pumping Pattern", ["Once a Day", "Twice a Day", "Optimised Model"])

st.sidebar.title("Cost v/s Time")


currCost = []
for i in range(24):
    input_val = st.sidebar.number_input(f"{i} Hours", value=0.0, step=0.1)
    currCost.append(input_val)


def refillTank():
    return 100

def predictWaterLevel(currLevel, currTime):
    nextFiveHours = []

    df = pd.read_csv('level_differences.csv')
    for i in range(currTime+1, currTime+6):
        column_name = f'Hour_'+str(i%24)
        average = df[column_name][-30:].mean()
        nextFiveHours.append(currLevel+average)
        currLevel+=average

    return nextFiveHours

threeDayUsage = pd.read_csv('level_differences.csv').iloc[0, 1:].tolist()
level = 100
if st.sidebar.button("Calculate"):
    if graph_type == "Once a Day":
        levelList = []

        sumCost = 0

        for i in range(0, 720):
            if(i%24 == 12):
                level = refillTank()
                sumCost+=currCost[12]  
            level += threeDayUsage[i%24]
            levelList.append(level)

        st.subheader("Water Tank Level Over Time: Manual Pumping twice a Day")
        fig, ax = plt.subplots()
        ax.plot(np.arange(720), levelList, color='blue')
        ax.plot(np.linspace(0, 720, 100), np.zeros(100), color='red')

        ax.set_xlabel('Time [hr]')
        ax.set_ylabel('Water Level [L]')
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        st.write(f"Total cost incurred in 30 Days: Rs.{sumCost:.2f}")
    elif graph_type == "Twice a Day":
        levelList = []

        sumCost = 0

        for i in range(0, 720):
            
            if(i%24 == 6):
                level = refillTank()
                sumCost+=currCost[6]
            elif(i%24 == 16):
                level = refillTank()
                sumCost+=currCost[16]
            
            level += threeDayUsage[i%24]
            levelList.append(level)

        st.subheader("Water Tank Level Over Time: Manual Pumping twice a Day")
        fig, ax = plt.subplots()
        ax.plot(np.arange(720), levelList, color='blue')

        ax.set_xlabel('Time [hr]')
        ax.set_ylabel('Water Level [L]')
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        st.write(f"Total cost incurred in 30 Days: Rs.{sumCost:.2f}")
    elif graph_type == "Optimised Model":
        levelList = []

        sumCost = 0

        for i in range(0, 720):
            tempNextFive = predictWaterLevel(level, i%24)
            print(f"Hour: {i} :: {tempNextFive}")
            
            for j in range(0, 5):
                minCost = sys.maxsize
                print(f"{currCost[(i+j)%24]}")
                if(tempNextFive[j]<=20):
                    for k in range(i%24, (i+j+1)%24):
                        if(currCost[k]<minCost):
                            minCost = currCost[k]
                            refillHour = k
                    level = refillTank()
                    # print(f"Tank Refilled!!, {refillHour}")
                    sumCost += minCost
                    break
    
            level += threeDayUsage[i%24]
            levelList.append(level)

        st.subheader("Water Tank Level Over Time: Intelligent Pumping")
        fig, ax = plt.subplots()
        ax.plot(np.arange(720), levelList, color='blue')

        ax.set_xlabel('Time [hr]')
        ax.set_ylabel('Water Level [L]')
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        st.write(f"Total cost incurred in 30 Days: Rs.{sumCost:.2f}")
