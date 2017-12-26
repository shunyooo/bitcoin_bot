import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('ggplot')
# font = {'family': 'meiryo'}
# matplotlib.rc('font', **font)
mpl.rc('figure', figsize=(16, 8))


def plot(*args, **kwargs):
    plt.plot(*args, **kwargs)
