# coding: utf-8
import numpy as np
import datetime
import cartopy.util as cutil
import xarray as xr
import pandas as pd
"""

"""
class read3D:
    """
    read gtool format data 
    to generate this instance pass filename

    Constant value
    ---------------
    head,tail,head2,tail2 :4byte binary
             size info of fortran binary header
    Method
    --------------
    __init__(self,data,count,x,y,z)
    getarr(self,timestep)
    getheader()
    getDate 
    """
    head = ("head",">i4")
    tail = ("tail",">i4")
    head2 = ("head2",">i4")
    tail2 = ("tail2",">i4") 
    def __init__(self,file,count=1,x=128,y=64,z=36):
        """
        Parameter
        ----------------
        file  : string 
                filename of datafile
        count : int  
                num of data ex) daily=365,monthly=12
        x,y,z :int (lon,lat,alt)
        summ : int 
            total gird number
        """
        data = open(file,'br')
        self.x=x
        self.y=y
        self.z=z
        self.count=count
        if z == None:
            self.summ=str(int(x*y))
        else:
            self.summ=str(int(x*y*z))
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+self.summ+"f")
                       ,self.tail2])     #big endian
        chunk=np.fromfile(data,dtype=dt,count=count)
        self.chunk = chunk
        data.close()
    def getarr(self,timestep=0,cyclic=False,na_values=-999,miss=False):
        """
        get ndarray(z=36,y=64,x=128)
        
        Parameters
        -------------
        timestep  :  int (default=0)
                  1 origin and converted to 0 origin
        cyclic    : boolean (default = False)
        na_values : float (default=-999)
        miss      : boolean (default=False)
        Return
        ----------------
        arr    : numpy.ndarray((z=36,y=64,z=128))
        """
        arr = self.chunk[timestep]['arr']
        arr = arr.reshape((self.z,self.y,self.x),order='C')
        if miss:
            arr[arr <= na_values] = np.nan

        if cyclic:
            arr = cutil.add_cyclic_point(arr)
        return arr
    def getheader(self,timestep=0):
#        print(self.chunk[timestep]['header'])
        return  self.chunk[timestep]['header']
    def getDate(self,timestep=0,timespec='auto',timeinfo=True):
        """
        return datetime string as isoformat
        parameter
        ------------
        timstep  : int (default=0)
        timespec : string(default='auto')
        timeinfo  : boolean(default=True)
        
        return
        ---------
        label    :string isoformat
        
        """
        day=self.chunk[timestep]['header'][26].decode()
        label= datetime.datetime.strptime(day, '%Y%m%d %H%M%S ').isoformat(timespec='auto')
        if (not timeinfo):
            label=label[0:10]
        return label
    def getFortranheader_footer(self,timestep=0):
        head1=self.chunk[timestep]['head']
        head2=self.chunk[timestep]['head2']
        tail1=self.chunk[timestep]['tail']
        tail2=self.chunk[timestep]['tail2']
        return head1,head2,tail1,tail2   
    def getDatetimeIndex(self,timestep=0,freq='MS'):
        """
        get pd.DatetimeIndex
 
        Parameters
        ---------------
        timestep : int (default 0)
        freq     : string default 'MS' (follow pandas format cord)
        
        Return
        ---------------
        datetime :pd.DatetimeIndex (default return monthly)
        """
        sday=self.getDate(timestep=0)
        eday=self.getDate(timestep=self.count-1)
        datetime=pd.date_range(sday,eday,freq=freq)
        return datetime
    def to_dataarray(self,end=1,cyclic=False):
        if cyclic:
            x = self.x+1
        else:
            x = self.x
        if self.z == None:
            dataarray=np.zeros((end,self.y,x))
            for i in range(end):
                dataarray[i,:,:]=self.getarr(timestep=i,cyclic=cyclic)
        else:
            dataarray=np.zeros((end,self.z,self.y,x))
            for i in range(end):
                dataarray[i,:,:,:]=self.getarr(timestep=i,cyclic=cyclic) 
        return dataarray
    def to_dataset(self):
        ds = 'Null'
        
        return ds
    


class readlon():
    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,x=128):
        self.x=x
        file='/home/onishi/GTAXDIR/GTAXLOC.GLON'+str(self.x)
        data=open(file,'br')
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+str(self.x)+"f")
                       ,self.tail2])     #big endian
        chunk=np.fromfile(data,dtype=dt)
        self.chunk = chunk
        data.close()
    def getlon(self,cyclic=False):
        lon = self.chunk[0]['arr']
        if cyclic:
            lon = np.append(lon,[360.0])
        return lon        
    
class readlat():
    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,y=64):
        self.y=y
        file='/home/onishi/GTAXDIR/GTAXLOC.GGLA'+str(self.y)
        data=open(file,'br')
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+str(self.y)+"f")
                       ,self.tail2])     #big endian
        chunk=np.fromfile(data,dtype=dt)
        self.chunk = chunk
        data.close()
    def getlat(self):
        lat = self.chunk[0]['arr']
        return lat
class readgrid():
    def __init__(self,x=128,y=64):
        self.x=x
        self.y=y
    def getlonlat(self,cyclic=False):
        lat=readlat(self.y).getlat()
        lon=readlon(self.x).getlon(cyclic=cyclic)
        return lon,lat
    def getmesh(self,cyclic=False):
        x,y=self.getlonlat(cyclic=cyclic)
        xx,yy=np.meshgrid(x,y)
        return xx,yy
class readalt(read3D):
    """
    read sigma
    if you need sigma,pa,beta, set count=3
    """
    def __init__(self,file,count=1,x=1,y=1,z=36):
        super().__init__(file,count,x,y,z)
        pass
    def getalt(self):
        """
        Parameter
        --------------
        None
        Return
        --------------
        lonarray  :numpy.ndarray(36)
        """
        sig = self.chunk[0]['arr']
        return sig
    def getsigma(self):
        """
        Parameter
        ----------------
        None

        Return
        ------------------
        pa   :np.ndarray(z)
        beta :np.ndarray(z)
        """
        sigma = self.chunk[0]['arr']
        pa = self.chunk[1]['arr']
        beta = self.chunk[2]['arr']
        return pa,beta
class read2D(read3D):
    """
    read surface
    Parameter
    -----------------
    file  :  string filename
    count :  totaldata number
    """
    def __init__(self,file,count=1,x=128,y=64,z=None):
        super().__init__(file,count,x,y,z)
        pass
    def getarr(self,timestep=0,cyclic=False,na_values=-999,miss=False):
        """
        get ndarray((y=64,x=128))
        
        Parameters
        ----------------
        timestep  : int (default 0)
        cyclic    : bool
                default = True
                if True ,add cyclic point on 2Darray
        Return
        ----------------
        arr    : numpy.ndarray((y=64,x=128))
        """
        arr = self.chunk[timestep]['arr']
#succeed when order='C' not 'F'
        arr = arr.reshape((self.y,self.x),order='C')
        if miss:
            arr[arr <= na_values] = np.nan
        if cyclic:
            arr = cutil.add_cyclic_point(arr)
        return arr

def to_netcdf(lon,lat,datetime,arr
            ,filename='test.nc'
            ,arrname='undefined'
            ,attrs={'None':'None'}):

    ds = xr.Dataset(
        {
            arrname:(['time','lat','lon'],arr)
        },
        coords={
                'time':datetime,
                'lat':('lat',lat,{'units':'degrees_north'}),
                'lon':('lon',lon,{'units':'degrees_east'})
        }
        ,attrs=attrs
         
    )
    return ds

######################################################################
def weighted_mean(data,grid=(128,64),dim='2d',xr=[0,None],yr=[0,None],cyclic=False):
    """
    return weighted regional average
    passed argument are only data
    this function return global weighted average 
   
    args     type       default
    -------------------------------
    data    : np.ndarray (128,64) only to dim data now
    grid    : int,tuple : (128,64)
    dim     : string    : '2d'
    xr      : int,list  : [0,None]
    yr      : int,list  : [0,None]
    cyclic  : bool      : False
    
    return
    -------------------------------
    weighteddata :real
  
    """
    sx,ex=xr[0],xr[1]
    sy,ey=yr[0],yr[1]
    if ex == None:
        ex=data.shape[-1]
    if ey == None:
        ey=data.shape[0]
    print(sx,ex)
    gridfile='/home/onishi/GRID/harea'+str(grid[0])+'x'+str(grid[1])+'_'+dim
    if dim =='2d':
        harea=read2D(gridfile,x=grid[0],y=grid[1]).getarr(cyclic=cyclic)
    else:
        raise NameError(dim+'is Invalid dimension')
    harea = harea*(data/data)  #consider NaN value
    data = data *harea
    weighteddata = np.nansum(data[sy:ey,sx:ex],axis=(0,1))\
                   /np.nansum(harea[sy:ey,sx:ex]) 
    return weighteddata
def weighted(arr,x=128,y=64,cyclic=False):
    """
    Parameter
    --------------
    arr  :np.ndarray((64,128))
    x,y  :int  grid
    cyclic :boolean
    Return
    --------------
    weighted_arr :np.ndarray((2,64,128))
    """
    gridfile='/home/onishi/GRID/harea'+str(x)+'x'+str(y)+'_2d'
    harea=read2D(gridfile,x=x,y=y).getarr(cyclic=cyclic)
    weighted_arr=np.concatenate([arr*harea,harea]).reshape((2,64,128))
    return weighted_arr

def weighted_mean2(weighted_arr,axis=(1,2)):
    """
    Parameter
    ---------------
    weighted_arr :np.ndarray((2,64,128))
    Return
    ---------------
    zonal_mean
    """
    temp=weighted_arr.mean(axis=axis)
    numer=temp[0]
    denomi=temp[1]
    zonal_mean=numer/denomi
    return zonal_mean
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
