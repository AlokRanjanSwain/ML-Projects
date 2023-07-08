import argparse
import ast
import cv2
import imageio
from tqdm import tqdm

class VideoError(Exception):
    pass

def convert_to_sec_str(time_str):
    """convert string to seconds

    Args:
        time_str (str): sting in min.sec format

    Returns:
        int: seconds
    """
    min_pt, dec_pt = time_str.split(".")
    
    secs_from_mins = int(min_pt)*60
    secs = int(dec_pt)
    
    return secs_from_mins +secs



def merge_ranges(ranges):
    """merge_range of the skip_range

    Args:
        ranges (string): list of strings consisting skip ranges

    Returns:
        _type_: return sorted list
    """
    merged_ranges = []

    # Sort the ranges based on the start value
    sorted_ranges = sorted(ranges, key=lambda x: float(x.split('-')[0]))

    for range_str in sorted_ranges:
        start, end = map(float, range_str.split('-'))
        
        # if list is empty or non-coincidenctial range
        if not merged_ranges or start > merged_ranges[-1][1]:
            merged_ranges.append((start, end))
        else:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))

    # Convert merged ranges back to string format
    merged_ranges_str = [f"{start}-{end}" for start, end in merged_ranges]

    return merged_ranges_str



def frame_skipped(skip_ranges, fps):
    """return set of frames to be skipped

    Args:
        skip_ranges (list): list of string with time range to be skipped
        fps (int): fps of the video

    Returns:
        set: frame index/number to be skipped
    """
    
    # Merge and sort common ranges
    skip_ranges=merge_ranges(skip_ranges)

    # Convert skip ranges to frame indices
    skip_frames = set()

    for skip_range in skip_ranges:

        start_time, end_time = skip_range.split('-')

        start_frame = int(convert_to_sec_str(start_time) *fps)
        end_frame = int(convert_to_sec_str(end_time) *fps)

        skip_frames.update(range(start_frame, end_frame + 1))
            
    print("Number of frames skipped: ", len(skip_frames)) 
    
    return skip_frames
    

def convert_to_gif(video_path, output_gif_path, size_w, size_h, footer_h,
                   skip_ranges=None, footer_path=None):
    """convert video to gif

    Args:
        video_path (_type_): path of video file
        output_gif_path (_type_): path of gif file
        size_w (int, optional): gif output widht. Defaults to 320.
        size_h (int, optional): gif output height. Defaults to 240.
        skip_ranges (_type_, optional): time ranges to skip. Defaults to None.
        footer_path (_type_, optional): footer image if required. Defaults to None.
        footer_h (int, optional): footer image output height. Defaults to 30.
    """
    
    video = cv2.VideoCapture(video_path)

      # Check if the video is empty or unable to open
    if not video.isOpened():
        raise VideoError(f"Unable to open video: {video_path}")


    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create a list to store frames
    frames = []
    
    #create a frame number sets to skip
    skip_frames = set()
    if skip_ranges:
        skip_frames = frame_skipped(skip_ranges,fps)
    
    
    #Add footer
    if footer_path:
        
        foot_img = cv2.imread(footer_path)
        foot_img = cv2.resize(foot_img,(size_w, footer_h))
        foot_img = cv2.cvtColor(foot_img, cv2.COLOR_BGR2RGB)
        
    
    # storing the frames for gif
    with tqdm(total=total_frames, desc='Converting to GIF') as pbar:
        frame_index = 0
        while True:
            ret, frame = video.read()

            if not ret:
                break
                       
            # skipping frames
            if skip_ranges and frame_index in skip_frames:
                frame_index += 1
                continue

            # Convert the frame to RGB for compatibility with imageio
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # resize
            frame_rgb = cv2.resize(frame_rgb,(size_w,size_h))
            
            if footer_path:
                # Concatenate the frame and the footer image vertically
                frame_rgb = cv2.vconcat([frame_rgb, foot_img])

            frames.append(frame_rgb)
            pbar.update(1)
            frame_index += 1
    
    duration = 1000/fps
    # Save frames as a GIF using imageio
    imageio.mimsave(output_gif_path, frames, format='GIF', duration=duration)

    # Release resources
    video.release()
    
    return 


def main():
    """Main Funtion
    """ 
    parser = argparse.ArgumentParser(description="Convert video to gif, can skip part of video as well")

    # Add command-line options
    parser.add_argument('-v', '--video_path', help='location of video file')
    parser.add_argument('-f', '--footer_path', help='location of footer image file')
    parser.add_argument('-o', '--output', help='Specify the output gif file location. Provide in .gif format')
    parser.add_argument('-ih', '--image_h', type=int, help='height of out gif')
    parser.add_argument('-iw', '--image_w', type= int, help='width of out gif')
    parser.add_argument('-fh', '--footer_h', type= int,help='footer height for the output')
    parser.add_argument('-s','--skip_range', help='skip ranges for the skipping the video')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Set the variable
    
    # get and validate the video path
    video_path = args.video_path
    if video_path is None:
        parser.error('Video path is missing.')

    # get and validate gif path
    out_path = args.output
    if out_path is None: 
        parser.error('Output gif path is missing')

    footer_path = args.footer_path

    # set image dimension and footer height
    image_w = args.image_w
    if image_w is None:
        image_w = 320
    
    image_h = args.image_h
    if image_h is None:
        image_h = 240

    foot_h = args.footer_h
    if foot_h is None: 
        foot_h = 50

    # set skip ranges 
    skip_range_str = args.skip_range
    skip_ranges = None
    if skip_range_str is not None:
        skip_ranges = ast.literal_eval(skip_range_str)

    try: 
        
        convert_to_gif(video_path=video_path, output_gif_path=out_path, footer_path=footer_path,
        size_w=image_w, size_h=image_h, footer_h= foot_h,skip_ranges=skip_ranges)

        print("Video converted to GIF")

    except VideoError as e:
        print(str(e))

if __name__ == "__main__":
    print("Starting Video Editing Application ")
    main()