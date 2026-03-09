import numpy as np
import matplotlib.pyplot as plt

labels_obliq = ['S(9m 33sol)', 'E(1m 1sol)', 'N(3m 41sol)', 'F(6m 17sol)'] #황도경사
labels_ecc = [' P(9m 1sol)', '', 'A(3m 13sol)'] #이심률

def add_eot_labels(t0, delay1, delay2_shifted, total_delay):
    zero_crossings_obliq = np.where(np.diff(np.sign(delay2_shifted)))[0]
    zero_crossings_ecc = np.where(np.diff(np.sign(delay1)))[0]

    # 1. 황도경사 (Obliquity) 점 및 라벨
    plt.scatter(t0[zero_crossings_obliq], 
                total_delay[zero_crossings_obliq], 
                color='crimson', 
                s=30, 
                zorder=4)

    seen = set()
    for x, y, label in zip(t0[zero_crossings_obliq], total_delay[zero_crossings_obliq], labels_obliq):
        if (x, y) not in seen:
            seen.add((x, y))
            plt.text(x, y, label, fontsize=10, zorder=4, color='crimson', verticalalignment='bottom')

    
    # 2. 이심률 (Eccentricity) 점 및 라벨
    plt.scatter(t0[zero_crossings_ecc], 
                total_delay[zero_crossings_ecc], 
                color='blue', 
                s=30, 
                zorder=4)

    seen = set()
    for x, y, label in zip(t0[zero_crossings_ecc], total_delay[zero_crossings_ecc], labels_ecc):
        if (x, y) not in seen:
            seen.add((x, y))
            plt.text(x, y, label, fontsize=10, zorder=4, color='blue', verticalalignment='bottom')


    
def add_analemma_labels(delay1, delay2_shifted, total_delay, alt):
    zero_crossings_obliq = np.where(np.diff(np.sign(delay2_shifted)))[0]
    zero_crossings_ecc = np.where(np.diff(np.sign(delay1)))[0]

    # 1. 황도경사 (Obliquity) 점 및 라벨
    plt.scatter(total_delay[zero_crossings_obliq], 
                alt[zero_crossings_obliq], 
                color='crimson', 
                s=30, 
                zorder=4)

    x_obliq_zeros = total_delay[zero_crossings_obliq]
    y_obliq_zeros = alt[zero_crossings_obliq]

    # 2. 이심률 (Eccentricity) 점 및 라벨
    plt.scatter(total_delay[zero_crossings_ecc], 
                alt[zero_crossings_ecc], 
                color='blue', 
                s=30, 
                zorder=4)

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