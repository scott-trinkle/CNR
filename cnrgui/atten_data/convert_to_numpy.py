import numpy as np


def read_and_save_atten_data(fn):
    '''
    Reads .txt filename for u/p data and saves as numpy array
    '''

    data = np.loadtxt(fn, dtype=np.float64)
    data = data.reshape((data.size // 2, 2))

    new_fn = fn.strip('.txt')
    np.save(new_fn, data)


mats = ['H2O', 'Os', 'Pb', 'U']

for mat in mats:
    fn = 'u_p_' + mat + '.txt'
    read_and_save_atten_data(fn)
