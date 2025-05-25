'''
Photo services for Mac Photo App (osx)

'''
import os.path
from pathlib import Path
import sys

from pathvalidate import is_valid_filepath, sanitize_filepath

import osxphotos

# ph _info fields
osxKwDict = {'_uuid':'uid',
        'filename':'fn',
        'originalFilename':'bn',
        'imageDate':'dt',
        'extendedDescription':'desc',
        'keywords':'kw',
        'albums':'album',
        'persons':'person'}


class photosOSX(object):
    '''
    osxphotos services for photo organizer

    - the photosOSX db.photos is treated as the top dir of osx photo

    - access photoes within mac photo app 
    - access albums

    '''
    
    def __init__(self, **kwargs):
        self.DIR = 'osxPhotos:'
        self.extList = ['jpg', 'jpeg', 'png']
        
        self.db = osxphotos.PhotosDB()
        self.phDict = self.walk(**kwargs)

    def findFN(self, fn):
        return [ph for ph in self.db.photos() if ph.filename == fn]
    def findBN(self, bn):
        return [ph for ph in self.db.photos() if ph.original_filename == bn]


    def walk(self, **kwargs):
        self.dupPhotoDict = {}
        phDict = {}
        p2aDict = self.ph2AlbumDict()
        for ph in self.db.photos():
            d = self._statDict(ph)
            
            try: d['album'] = p2aDict[fn]
            except: d['album'] = '.'

            fn = f"{d['album']}/{self._bn(ph)}"
            if fn in phDict.keys():
                self.dupPhotoDict[fn] = f"{phDict[fn]['fn']}:{d['fn']}"
            phDict[fn] = d
        return phDict

    def List(self, **kwargs):
        return [d for d in self.db.photos(**kwargs)]

    def ph2AlbumDict(self):
        '''
        build photo.filename to album dict
        Dup's get the last 
        '''
        aDict = {}
        for a in self.db.albums:
            for ph in self.db.photos(albums=[a]):
                fn = ph.filename
                if fn in aDict.keys():
                    print("dup Album", fn, a, aDict[fn])
                aDict[fn] = a
        return aDict


    def albumDict(self):
        aDict = {a:[] for a in self.db.albums}
        for bn,stDict in self.phDict.items(): 
            aDict[stDict['album']].append(stDict)
        return aDict

    def albumCount(self, aDict=None):
        if aDict is None : aDict = self.albumDict()
        return {a:len(phList) for a,phList in aDict.items()}

    def _bn(self, p): return p._info['originalFilename']

    def _statDict(self, p):
        '''
        Build stat dict per photo
        '''
        stDict = {}
        for kw,kNew in osxKwDict.items():
            stDict[kNew] = p._info[kw]
        bn = stDict['bn']
        ext = Path(bn).suffix
        if ext not in self.extList:
            self.extList.append(ext)
        stDict['ext'] = ext
        return stDict
        
    def __repr__(self):
        '''
        Return str representing info about OSX photos
        '''
        osxDict = dict(photos = len(self.List()),
                       dupPhotos = len(self.dupPhotoDict.keys()),
             kw = self.db.keywords,
             persons = self.db.persons,
             albums = self.db.albums,
             dict_kw = self.db.keywords_as_dict,
             dict_persons = self.db.persons_as_dict,
             #dict_album = self.db.albums_as_dict
            )
        d = dict(DIR = self.DIR,
                 dirs = len(self.db.albums),
                 photos = len(self.phDict.keys()),
                 exts = self.extList,
                 osx = osxDict)
        return str(d)
        
        
        return str(d)

    def export(self, p, dir):
        '''
        Export a single photo into a dir
        '''
        if not p.ismissing:
            if p.hasadjustments:
                exported = p.export(dir, edited=True)
            else:
                exported = p.export(dir)
            print(f"Exported {p.filename} to {dir}")
        else:
            print(f"Skipping missing photo: {p.filename}")

        
    def exportAlbum(self, album, dirTop):
        '''
        source: https://pypi.org/project/osxphotos/

        Export all photos of an album into dirTop/<album>        
        '''
        # create destination dir if needed
        dirAlbum  = os.path.join(dirTop, album)
        if not os.path.isdir(dirAlbum):
            os.makedirs(dirAlbum)

        for p in self.db.photos(albums=[album]):
            
            # verify path is a valid path
            #if not is_valid_filepath(dest_dir, platform="auto"):
            #   sys.exit(f"Invalid filepath {dest_dir}")
            self.export(p, dirAlbum)

    
            
                        

