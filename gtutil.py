import numpy as np
import sys
sys.path.append('/home/onishi/Pylib')

month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
season=['JJA','SON','DJF','MAM']
mdays=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def weighted_mean(arr,area):
    """
    Parameter
    --------------
    arr   :array_like
    area  :array_like
    Return
    --------------
    weighted_mean :np.ndarray
    """
    
    weighted_mean=(arr*area).sum()/area.sum()
    return weighted_mean


 
def corre_coef(x,y):
    """
    args  type
    -------------------------
    x     np.ndarray((time,y,x))
    y     np.ndarray((time,y,x))
    
    return  type
    -------------------------
    correlation  np.ndarray((y,x))
    """
    xmean=x.mean(axis=0)
    ymean=y.mean(axis=0)
    xyarr=x*y
    xymean=xyarr.mean(axis=0)
    x2mean=(x**2).mean(axis=0)
    y2mean=(y**2).mean(axis=0)
    xystd=xymean-(x.mean(axis=0)*y.mean(axis=0))
    correlation=(xymean-xmean*ymean)/np.sqrt((x2mean-xmean**2)*(y2mean-ymean**2))
    return correlation

def zscore(x,axis=None,ddof=0):
    """ 
    return zscore standalization
           x =(x - x.mean)/x.std
    average=0 std=1

    Parameters
    -------------------
    x : numpy.ndarray(x,y)
    axis :int 0 #caliculate each col
              1 #           each row
    ddof :int 0 #when caliculate std, devide by n
              1 #                   , devide by n-1
    Returns
    --------------------
    zcore : np.ndarray(x,y)
    """
    xmean=x.mean(axis=axis,keepdims=True)
    xstd=np.std(x,axis=axis,keepdims=True,ddof=ddof)
    zscore  =(x-xmean)/xstd
    return zscore

def min_max(x,axis=None):
    """
    return min_max standalization
           x = (x-x.min)/(x.max-x.min)
    min=0 max=1

    Parameters
    -------------------
    x : numpy.ndarray(x,y)
    axis :int 0 #caliculate each col
              1 #           each row

    Returns
    --------------------
    result : np.ndarray(x,y)
    """
    xmin =x.min(axis=axis,keepdims=True)
    xmax =x.max(axis=axis,keepdims=True)
    result = (x-xmin)/(xmax-xmin)
    return result
