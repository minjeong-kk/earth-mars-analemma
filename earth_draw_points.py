import numpy as np
import matplotlib.pyplot as plt

labels_obliq = ['E(3/20)', 'N(6/21)',  'F(9/22)', 'S(12/22)'] #황도경사
labels_ecc = ['P(1/4)', '', 'A(7/4)'] #이심률

def add_eot_labels(t0, delay1, delay2_shifted, total_delay):
    zero_crossings_obliq = np.where(np.diff(np.sign(delay2_shifted)))[0]
    zero_crossings_ecc = np.where(np.diff(np.sign(delay1)))[0]

    # 점 찍기
    plt.scatter(t0[zero_crossings_obliq], 
                total_delay[zero_crossings_obliq], 
                color='crimson', 
                s=30, 
                zorder=4)
    
    plt.scatter(t0[zero_crossings_ecc], 
                total_delay[zero_crossings_ecc], 
                color='blue', 
                s=30, 
                zorder=4)

    # 황도경사
    
    seen = set()
    for x, y, label in zip(t0[zero_crossings_obliq], total_delay[zero_crossings_obliq], labels_obliq):
        if (x, y) not in seen:
            seen.add((x, y))
            plt.text(x, y, label, fontsize=10, zorder=4, color='crimson', verticalalignment='bottom')

    # 이심률
    
    seen = set()
    for x, y, label in zip(t0[zero_crossings_ecc], total_delay[zero_crossings_ecc], labels_ecc):
        if (x, y) not in seen:
            seen.add((x, y))
            plt.text(x, y, label, fontsize=10, zorder=4, color='blue', verticalalignment='bottom')


def add_analemma_labels(delay1, delay2_shifted, total_delay, alt):
    zero_crossings_obliq = np.where(np.diff(np.sign(delay2_shifted)))[0]
    zero_crossings_ecc = np.where(np.diff(np.sign(delay1)))[0]

    # 황도경사
    plt.scatter(total_delay[zero_crossings_obliq], 
                alt[zero_crossings_obliq], 
                color='crimson', 
                s=30, 
                zorder=4)

    # 이심룰
    plt.scatter(total_delay[zero_crossings_ecc], 
                alt[zero_crossings_ecc], 
                color='blue', 
                s=30, 
                zorder=4)

    x_obliq_zeros = total_delay[zero_crossings_obliq]
    y_obliq_zeros = alt[zero_crossings_obliq]
    x_ecc_zeros = total_delay[zero_crossings_ecc]
    y_ecc_zeros = alt[zero_crossings_ecc]

    seen = set()
    for x, y, label in zip(x_obliq_zeros, y_obliq_zeros, labels_obliq):
        if (x, y) not in seen:
            seen.add((x, y))
            plt.text(x, y, label, fontsize=10, zorder=4, color='crimson', verticalalignment='bottom')

    seen = set()
    for x, y, label in zip(x_ecc_zeros, y_ecc_zeros, labels_ecc):
        if (x, y) not in seen:
            seen.add((x+2, y))
            plt.text(x-3, y, label, fontsize=10, color='blue', verticalalignment='bottom', zorder=4)