from scipy.stats import norm
import matplotlib.pyplot as plt

class StatDist:

    def __init__(self, data):
        self.pdf = norm.pdf(data)

class StatPlot(plt.boxplot):

    def __init__(self, name, data):
        self.plot = super(data, labels = [name])