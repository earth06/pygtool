import numpy as np
import pandas as pd
month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
season=['DJF','MAM','JJA','SON']
mdays=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
reg=[   'AMN', 'AMM', 'AMS', 'AFN', 'AFS',\
        'EUR', 'CEU', 'SBR', 'IND', 'CHN',\
        'JPN', 'IDN', 'AUS', 'TLD']
head = ("head",">i4")
tail = ("tail",">i4")
head2 = ("head2",">i4")
tail2 = ("tail2",">i4") 
gthead = ("header",">64S16")

ffmt=(head,tail,head2,tail2)
mid_lon=np.arange(1.40625,360.1,2.8125)
#def lonlabel(left=):

#def latlabel(left=-90,right=90,dlat=30):
#    latlist=[]
#    for i in range(lfet,right,dlat)

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

def get_area(dlon=2.5e0,dlat=2.5e0):
    """
    """
    er=6370e3
    xxtmp,yytmp=np.meshgrid(np.arange(0,360,dlon),np.arange(90,-90.1,-dlat))
    area=(er**2)*(np.deg2rad(dlon)*(np.sin(np.deg2rad(yytmp[0:-1,:]))\
                                  -np.sin(np.deg2rad(yytmp[1:,:])))\
)
    return area
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
def read_nas(filename,header=False,na_values=-999):
    """
    reading nas file with skipping data
    return pd.Dataframe

    Parameter
    ---------
    filename :string
    header   :boolean

    Return
    ---------
    df             :pd.Dataframe
    head(optional) :list
    """
    with open(filename,'tr') as data:
        line1=data.readline()
        row=int(line1.split(',')[0])
        head=data.readlines()
    df=pd.read_csv(filename,skiprows=row-1,na_values=na_values)
    if header:
        return df,head
    else:
        return df

def normdate_to_datetime():
    """
    converting floating date into datetimeindex
    """
    
    return
def cmass_column(C,ps,T,timestep=0,zmax=36,fact=1.0e0,cyclic=False):
    """
    conduct vertical integration
    This function should be weritten class
    __init__() set sigma scaler.
    """
    P=aeta+beta*ps.getarr(timestep=timestep,cyclic=cyclic)*1e2
    PM=aeta_M+beta_M*ps.getarr(timestep=timestep,cyclic=cyclic)*1e2
    dp=PM[1:,:,:]-PM[:-1,:,:]
    grav=9.8e0
    rho=(P/287.0*T.getarr(timestep=timestep,cyclic=cyclic))
    dz=dp/(rho*grav)
    col3D=C.getarr(timestep=timestep,cyclic=cyclic)*dz
    column=col3D[0:zmax,:,:].sum(axis=0)*fact
    return colflux
