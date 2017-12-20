
from scipy.stats import multivariate_normal

mvn = multivariate_normal(mean=[1,1], cov=[1,1])

print mvn.pdf([[2,3], [1-2,1-2]])
