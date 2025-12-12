import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def read_signal(filepath):
    indices = []
    values = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[3:]
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            indices.append(int(parts[0]))
            values.append(float(parts[1]))
    return indices,values

def Compare_Signals(file_name,Your_indices,Your_samples):      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:

            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Correlation Test case failed, your signal have different values from the expected one") 
            return
    print("Correlation Test case passed successfully")
    return True


def computeNormalizer(val1,val2):
    
    X = np.array(val1)
    Y = np.array(val2)
    n = len(X)

    normalizer= (1/n) * np.sqrt(np.sum(X**2) * np.sum(Y**2))

    return normalizer

def correlation(ind1,val1,ind2,val2):

    indices=[]
    signal=[]

    N = len(val1)
    d1 = dict(zip(ind1, val1))
    d2 = dict(zip(ind2, val2))
    start = N
    for i, v in enumerate(val2):
        d2[start + i] = v

    y_start = min(d1.keys())
    y_end = max(d1.keys())

    normalizer= computeNormalizer(val1,val2)

    for n in range(y_start,y_end+1):

        value=0
        for k in range (y_start,y_end+1):
            value+=d1[k]*d2[k+n]
        
        value=(1/N * value) / normalizer
        value = round(value, 8)

        signal.append(value)
        indices.append(n)
    
    return indices,signal



def max_index(values):

    n=len(values)
    maxVal=values[0]
    maxIdx=0
    for i in range(1,n):
        
        if(values[i]>maxVal):
            maxVal=values[i]
            maxIdx=i
    
    return maxIdx


def indices_arr():

    indices=[]

    for i in range(0,251):
        indices.append(i)
    
    return indices


def display_task6():

    st.subheader("Correlation")
    path1="Task 6\Correlation Task Files\Point1 Correlation\Corr_input signal1.txt"
    path2="Task 6\Correlation Task Files\Point1 Correlation\Corr_input signal2.txt"
    path3="Task 6\Correlation Task Files\Point1 Correlation\CorrOutput.txt"

    indicies1,value1=read_signal(path1)
    indicies2,value2=read_signal(path2)

    actual_ind,actual_val = correlation(indicies1,value1,indicies2,value2)
    exp_ind,exp_val= read_signal(path3)

    if st.button("Run Correlation Test Case"):

        col1, col2,col3 = st.columns(3) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(actual_ind, actual_val, marker='o', color='blue')
            ax1.set_title("Actual Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 
        
        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(exp_ind, exp_val, marker='o', color='green')
            ax2.set_title("Expected Signal", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)
        
        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(exp_val) - np.array(actual_val))
            ax3.plot(exp_ind, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)
        
        if Compare_Signals(path3,actual_ind,actual_val):
            st.write("Correlation Test case passed successfully")
    
    st.subheader("Time analysis")
    if st.button("Run Time Analysis Test Case"):

        path1="Task 6\Correlation Task Files\Point2 Time analysis\TD_input signal1.txt"
        path2="Task 6\Correlation Task Files\Point2 Time analysis\TD_input signal2.txt"

        indicies1,value1=read_signal(path1)
        indicies2,value2=read_signal(path2)

        actual_ind,actual_val = correlation(indicies1,value1,indicies2,value2)

        maxIndex=max_index(actual_val)
        Fs=100
        Ts=1/Fs

        result=Ts*maxIndex
        st.write("Time delay =", result)

    st.subheader("Classification")
    if st.button("Run Classification Test Case 1"):
        
        test_values=np.loadtxt("Task 6\Correlation Task Files\point3 Files\Test Signals\Test1.txt")
        indices=indices_arr()

        max_Up=0
        max_down=0
        for i in range (1,6):

            valuesUp=np.loadtxt(f"Task 6\Correlation Task Files\point3 Files\Class 2\_up{i}.txt")
            valuesDown=np.loadtxt(f"Task 6\Correlation Task Files\point3 Files\Class 1\down{i}.txt")

            _,valUp=correlation(indices,test_values,indices,valuesUp)
            _,valDown=correlation(indices,test_values,indices,valuesDown)

            max_Up=max_Up+max(valUp)
            max_down=max_down+max(valDown)


        avg_max_up=max_Up/5
        avg_max_down=max_down/5

        if(avg_max_up> avg_max_down):
            st.write("Signal is classified to Class 2 (Up)") 
        else:
            st.write("Signal is classified to Class 1 (Down)")
        
    

    if st.button("Run Classification Test Case 2"):

        test_values=np.loadtxt("Task 6\Correlation Task Files\point3 Files\Test Signals\Test2.txt")
        indices=indices_arr()

        max_Up=0
        max_down=0

        for i in range (1,6):

            valuesUp=np.loadtxt(f"Task 6\Correlation Task Files\point3 Files\Class 2\_up{i}.txt")
            valuesDown=np.loadtxt(f"Task 6\Correlation Task Files\point3 Files\Class 1\down{i}.txt")

            _,valUp=correlation(indices,test_values,indices,valuesUp)
            _,valDown=correlation(indices,test_values,indices,valuesDown)

            max_Up=max_Up+max(valUp)
            max_down=max_down+max(valDown)


        avg_max_up=max_Up/5
        avg_max_down=max_down/5

        if(avg_max_up> avg_max_down):
            st.write("Signal is classified to Class 2 (Up)") 
        else:
            st.write("Signal is classified to Class 1 (Down)")


