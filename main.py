import ffmpeg
import json
import argparse
import pandas as pd

def getVideoInfo(url):
    try:
        probe = ffmpeg.probe(url)['streams']
        index = 0
        while probe[index]['codec_type'] != 'video':
            index+=1

        fps_aux = probe[index]['r_frame_rate'].split('/')
        fps =  round(int(fps_aux[0])/int(fps_aux[1]))

        if fps > 50:
            return ('Not found',0,0)
        codec = probe[index]['codec_name']
        width = probe[index]['width']
        height = probe[index]['height']
        resolution = str(width)+'x'+ str(height)

        return (codec,fps,resolution)
    except:
        return ('unauthorized',0,0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Jiro')
    parser.add_argument('-f', '--fileName', type=str, required=True, help='name of file configuration')
    args = parser.parse_args()

    with open(args.fileName) as jsonFile:
        jsonCamInfo = json.load(jsonFile)
        jsonFile.close()

    listTuples = []
    for index, rtsp in enumerate(jsonCamInfo['sources']):
        listTuples.append((jsonCamInfo['mall_id'],rtsp)+getVideoInfo(rtsp))
        print(str(round((index+1)*100/len(jsonCamInfo['sources'])))+'%')

    df = pd.DataFrame(listTuples, columns=['mallId','rtsp','codec','fps','resolution'])
    df.to_csv(jsonCamInfo['mall_id']+'_'+jsonCamInfo['analytics']+'_RTSPstatus.csv',index=True,sep=';')
