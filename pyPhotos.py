#!/usr/bin/env python3
'''
Photos organizer

Sources:
- original sourced from https://github.com/gabrielfroes/photo-organizer/blob/master/photo-organizer.py

'''

import os
from pathlib import Path
import shutil
from datetime import datetime
from PIL import Image

from pyImgDiff import imgDiff


class photos(object):
    '''
    Manage photos on local filesystem
    '''
    DATETIME_EXIF_INFO_ID = 36867
    

    def __init__(self, **kwargs):
        self.DIR = kwargs.get('DIR', '.')
        if self.DIR[-1] == '/' : self.DIR[0:-1]
        self.extList = ['jpg', 'jpeg', 'png']
        self.phDict = self.walk(**kwargs)

    def FN(self, phName): return os.path.join(self.DIR, phName)
        
    def pwd(self, fn):
        '''
        Return 'YYYY/YYmmdd'
        '''
        date = self.photoDate(fn)
        return date.strftime('%Y') + '/' + date.strftime('%Y-%m-%d')

    def photoDate(self, fn):
        '''
        
        Return datetime of photo image
        - use image info, if exists
        - otherwise: use last modified time of image file
        '''
        if Path(fn).suffix.lower() in ['.pdf', '.mp4']:
            return datetime.fromtimestamp(os.path.getmtime(fn))
        
        date = None
        try: photo = Image.open(fn)
        except Exception as err:
            print(f"Warning, can not open image:",err)
            return datetime.fromtimestamp(os.path.getmtime(fn))
            
        if hasattr(photo, '_getexif'):
            infoDict = photo._getexif()
            if infoDict:
                if self.DATETIME_EXIF_INFO_ID in infoDict:
                    date = infoDict[self.DATETIME_EXIF_INFO_ID]
                    date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        if date is None:
            date = datetime.fromtimestamp(os.path.getmtime(fn))
        return date

    def mv(self, fn, newDIR):
        '''
        FIXME: TBD
        move fn to newDIR
        '''
        if self.DIR in newDIR :
            print("ERROR, mv NewDir contains photo top dir.", newDIR)
            return
            
        if not os.path.exists(newDIR):
            os.makedirs(newDIR)
        shutil.move(fn, newDIR + '/' + file)

    def walk(self, **kwargs):
        """
        Recursive walk thru photo director

        os.stat_result(st_mode=33152, st_ino=738824, 
        st_dev=16777220, 
        st_nlink=1, 
        st_uid=501, 
        st_gid=20, 
        st_size=2540722, 
        st_atime=1705757178, 
        st_mtime=1705753503, 
        st_ctime=1722888808)
        """
        self.dupPhotoDict = {}
        
        phDict = {}
        bnDict = {}

        dirRoot = kwargs.get('DIR',self.DIR)
        for dir, dList, bList in os.walk(dirRoot):
            #print("72 walk", dir, self.DIR)
            
            dir = dir.replace(self.DIR, '.')
            for bn in bList:
                # relative path
                fn = os.path.join(dir, bn)

                # Full path
                FN = os.path.join(self.DIR, fn)
                st = os.stat(FN)

                # Add new extensions
                ext = Path(bn).suffix
                if ext not in self.extList:
                    self.extList.append(ext)

                #phDt = self.photoDate(FN)

                if bn in bnDict.keys():
                    print("dup", bn, bnDict[bn],fn)
                    self.dupPhotoDict[bn] = (bnDict[bn],fn)
                bnDict[bn] = fn

                phDict[fn] = dict(uid = st.st_uid,
                                  fn = fn,
                                  bn = bn,
                                  dt = st.st_mtime,  # FIXME: check dt inside photo
                                  dtC = st.st_ctime,
                                  desc = '',
                                  kw = '',
                                  album = dir,
                                  persons = '',
                                  size = st.st_size,
                                  ext = ext
                                 )
        return phDict

    def organize(self, **kwargs):
        '''
        create inventory of photo directory
        '''
        self.dirList, self.bnList, self.fnList = self.walk(**kwargs)

    def __repr__(self):
        try: sdNum = len(list(set([d['album'] for d in self.phDict.values()])))
        except: sdNum = 0
                
        d = dict(DIR = self.DIR.replace(str(Path.home()),'~'),
                 dirs = sdNum,
                 photos = len(self.phDict.keys()),
                 exts = self.extList,
                 dups = len(self.dupPhotoDict.keys())
                )
        return str(d)

