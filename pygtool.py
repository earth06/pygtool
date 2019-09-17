import numpy as np
import datetime
import cartopy.util as cutil
import carto_kit as ckit
import xarray as xr
import pandas as pd
import gtutil
import gtplot
import pathlib
"""
"""

thisdir=str(pathlib.Path(__file__).resolve().parent)
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
#        print(self.getDate(timestep=timestep))
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
    def getDatetimeIndex(self,start=0,end=None,timestep=0,freq='MS'):
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
        if ( end == None ):
            end = self.count-1
        sday=self.getDate(timestep=start)
        eday=self.getDate(timestep=end)
        datetime=pd.date_range(sday,eday,freq=freq)
        return datetime
    def to_dataarray(self,start=0,end=None,cyclic=False):
        if end== None:
            end=self.count
        if cyclic:
            x = self.x+1
        else:
            x = self.x
        if self.z == None:
            dataarray=np.zeros((end-start,self.y,x))
            for i in range(end-start):
                dataarray[i,:,:]=self.getarr(timestep=start+i,cyclic=cyclic)
        else:
            dataarray=np.zeros((end-start,self.z,self.y,x))
            for i in range(end-start):
                dataarray[i,:,:,:]=self.getarr(timestep=start+i,cyclic=cyclic) 
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
        file=thisdir+'/GTAXDIR/GTAXLOC.GLON'+str(self.x)
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
    def showlon(self,cyclic=False):
        lon=self.getlon(cyclic=cyclic)
        for i in range(len(lon)):
            print(i,':',lon[i])
class readlat():
    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,y=64):
        self.y=y
        file=thisdir+'/GTAXDIR/GTAXLOC.GGLA'+str(self.y)
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
    def showlat(self):
        lat = self.getlat()
        for i in range(len(lat)):
            print(i,':',lat[i])
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
    def getmesh2(self):
        y=readlat(self.y).getlat()
        x=np.arange(1.40625,360.1,2.8125)
        xx,yy=np.meshgrid(x,y)
        return xx,yy


class readalt():
    """
    read sigma
    if you need sigma,pa,beta, set count=3
    """

    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,z=36):
        self.z=z
        file=thisdir+'/GTAXDIR/GTAXLOC.HETA'+str(self.z)
        data=open(file,'br')
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+str(self.z)+"f")
                       ,self.tail2])     #big endian
        chunk=np.fromfile(data,dtype=dt,count=3)
        self.chunk = chunk
        data.close()
    def getsig(self):
        sig=self.chunk[0]['arr']
        return sig
    def getsig_pa_beta(self):
        """
        Parameter
        ----------------
        None

        Return
        ------------------
        sig  :np.ndarray(z)
        pa   :np.ndarray(z)
        beta :np.ndarray(z)
        """
        sig=self.chunk[0]['arr']
        pa=self.chunk[1]['arr']
        beta=self.chunk[2]['arr']
        return sig,pa,beta
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
#        print(self.getDate(timestep=timestep))
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
if __name__ == '__main__':
    print(str(thisdir))
    
