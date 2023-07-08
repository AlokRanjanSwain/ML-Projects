# Common Python Utils

## Video to Gif Convertor with footer

### Python package requirements 
- opencv
- imageio
- tqdm

If required 

```sh
pip install requirements.txt
```

#### Application Details
```sh
python video_to_gif.py -v ./data/test.mp4 -o ./data/out_gif.gif -f ./data/footer.png -ih 340 -iw 480 -fh 30 -s "['0.1-0.4', '0.5-0.6', '0.2-0.3']"
```
##### Skip Ranges
- It could be the string of time ranges needs to be skipped.
- Currently supported in format of `min.sec`. E.g. '0.1' means 0 min and 1 sec and '0.10' means 0 min 10 sec.
- The code automatically sort and merge the time ranges, so no need to sort it by Users, just add the time ranges in the list as mentioned in usage

##### Output

The output will be like this:


<img src = "./data/out_gif.gif" width="320">
