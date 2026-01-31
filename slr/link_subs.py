# attach slr sub to correct place.....
import os
import glob
import  re
from pathlib import Path
import shutil as sh
# get all teh .mp4 files path


root = Path('/Volumes/my_files/porn')
sub_dir = Path('/Volumes/my_files/porn/subs/slr')


#############################################################################################
#map sub_id to sub_path
sub_id_to_path = {}
sub_paths = glob.glob(os.path.join(sub_dir.as_posix(), '*.srt'))
for sub_path in sub_paths:
    filename = os.path.basename(sub_path)
    sub_id = re.sub(r'\.srt$', '', filename)
    sub_id_to_path[sub_id] = sub_path
# print(sub_id_to_path)
# exit(1)

############################################################################################################
vid_paths = glob.glob(os.path.join(root.as_posix(), '**/*.mp4'), recursive=True)
print(len(vid_paths))
# exit(1)

###### check all the names, and filter out which are slr videos #######################
pattern = r"\d+_"
# vid_paths = [s for s in vid_paths if re.search(pattern, s)]
# print(vid_paths)
# print(len(vid_paths))

paths = []
for vid_path in vid_paths:
   #lowercase and check if slr/ sexlikereal is there
    if 'sexlikereal' in vid_path.lower() or 'slr' in vid_path.lower():
        paths.append(vid_path)

    pattern = r"^[0-9]+_[0-9]+\.mp4$"
    filename = os.path.basename(vid_path)
    if re.match(pattern, filename):
        paths.append(vid_path)

    pattern = r"^\d+_\d+p?\.mp4$"
    filename = os.path.basename(vid_path)
    if re.match(pattern, filename):
        paths.append(vid_path)
    # print(vid_path)



########## extract 5 digit slr scene id from video name################
matched = 0
for done, vid_path in enumerate(paths):
    print(f"Processing video {done + 1} of {len(paths)}")

    filename = os.path.basename(vid_path)
    parts = filename.split('_')
    numbers = [p for p in parts if re.sub(r'\..*$', '', p).isdigit()]
    id = numbers[0]
    # print(f"Extracted Numbers: {numbers}")
    if id in sub_id_to_path:
        # print("found..")
        # print(vid_path)
        matched+=1
        src_sub_path = sub_id_to_path[id]

        #dest_sub_path is path last name swapped with filename.srt
        dest_sub_path = os.path.join(os.path.dirname(vid_path), filename.split('.')[0] + '.srt')
        #copy src_sub_path to dest_sub_path
        sh.copy2(src_sub_path, dest_sub_path)
        print(src_sub_path, dest_sub_path,vid_path)
        # exit(1)
    else:
        print("not matched", vid_path)
# exit(1)
    # if numbers==[]:
    #     print(vid_path)
print(len(paths), matched)

##############################################
