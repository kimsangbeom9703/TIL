# [PHP/Ci4] FFMpeg 사용하여 동영상 재생시간 구하기

## 사용이유
```
    업로드 된 동영상 재생 시간을 구하고 싶어 FFMpeg를 사용하게 되었다.
```

## 설치
```
    root계정 실행

    cd /usr/local/bin
    
    mkdir ffmpeg && cd ffmpeg
    
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
    
    tar -xf ffmpeg-release-amd64-static.tar.xz

    cp -a /usr/local/bin/ffmpeg/ffmpeg-4.2.1-amd64-static/ . /usr/local/bin/ffmpeg/

    ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg

    ln -s /usr/local/bin/ffmpeg/ffprobe /usr/bin/ffprobe
```

## ci4 사용
```
    $ composer require php-ffmpeg/php-ffmpeg

    
    use FFMpeg\FFMpeg;
    use FFMpeg\FFProbe;
    
    public function fileDuration($filepath)
    {
        $ffmpeg = FFMpeg::create([
            'ffmpeg.binaries'  => '/usr/bin/ffmpeg', // 실제 FFmpeg 실행 파일의 경로
            'ffprobe.binaries' => '/usr/bin/ffprode', // 실제 FFProbe 실행 파일의 경로
        ]);
        $video = $ffmpeg->open($filepath);
        $streams = $video->getStreams();
        $duration = null;
        
        foreach ($streams as $stream) {
            // 비디오 스트림인 경우 (codec_type이 'video'인 경우) 재생시간(duration) 추출
            if ($stream->get('codec_type') === 'video') {
                $duration = $stream->get('duration');
                break; // 첫 번째 비디오 스트림에서 재생시간을 찾으면 루프 종료
            }
        }
       return $duration;
    }

```