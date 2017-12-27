import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('ggplot')
# font = {'family': 'meiryo'}
# matplotlib.rc('font', **font)


def set_figure(figsize=(16, 8)):
    mpl.rc('figure', figsize=figsize)


def plot(*args, **kwargs):
    plt.plot(*args, **kwargs)

set_figure()
