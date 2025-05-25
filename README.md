# photoOrganizer
Organize photos on local filesystem;  
- inventory all photos : done, see obj.phDict
- compare photos
- cleanup duplicates
- organize into albums 

## Repository

Types of repositories
- local files: root directory containing subtree of images
- osxphoto DB: images stored in Mac DB
- Windows???
- Other photo apps

### Features Desired
a) within respository
    - identify dups
    - classify pictures
        - people
        - time
        - geo location
        - organize into albums  (preference varies by individual)
b) merge respositories
    - identify dups
    - preserve subdirs

## Manage Duplicates
    - same basename  bn.ext, bn.ext2...
    - same time : create, modify time
    - same content
    - visually compare w/ quick manual classification
    - AI smart content comparison

## Future:
- handle multiple Photo directories
    - merge photos of 2 repositories
    - compare common photos (filename, date of photo, mtime)
    - smarte merge (save deleted files in temp dir)
- Create Albums
    - family
    - timeline
