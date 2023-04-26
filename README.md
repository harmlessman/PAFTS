# PAFTS

### Library That Preprocessing Audio For TTS.

PAFTS is a library for making Text-to-Speech dataset.
TTS data basically requires clean audio files and a text file with text corresponding to each audio file. 
This library makes audio files clean and creates text file with text corresponding to each audio file.


## Description 

PAFTS consist of three main operations.
1. Transform 
2. Delete BGM
3. STT

Transform operation changes the sampling rate(sr), channel, and format of the audio files.

Delete BGM operation removes background music from audio files.

STT operation generates text corresponding to the audio files.


```
# before run()

      path
        ├── 1_001.wav
        ├── 1_002.wav
        ├── 1_003.wav
        ├── 1_004.wav
        └── abc.wav


# after run()
    
      path
        ├── 1_001.wav # Background music removed 
        ├── 1_002.wav # sr, channel, format unified
        ├── 1_003.wav
        ├── 1_004.wav
        ├── abc.wav
        └── text.json
        
        # text.json
        {
              '1_001.wav' : "I have a note.", 
              '1_002.wav' : "I want to eat chicken.",
              '1_003.wav' : "...",
              '1_004.wav' : "...",
              'abc.wav' : "...",   
        }
```


### Supported Audio Formats

* **wav, mp3, ogg, flac**
* **Recommend using wav format** because it is much faster in Transform operation and Delete BGM operation.
* STT operation support **wav, flac** formats.


### Note

* Audio files are not provided. Please prepare your own audio files.
* Audio files are appropriate to say one or two sentences for 3 to 10 seconds.
* If the background music is music with lyrics, the background music cannot be removed clearly.
* Google Web Speech is free, but the quality is low, so if you want high quality, use Google Cloud Speech API or Azure STT API


## Features

* Use the [spleeter](https://github.com/deezer/spleeter) to remove background music.
* In STT, you can use [Google Web Speech](https://wicg.github.io/speech-api/), [Google Cloud Speech](https://cloud.google.com/speech-to-text) and [Azure STT](https://azure.microsoft.com/products/cognitive-services/speech-to-text/).
* If you use Google Cloud Speech API or Azure STT API, you need API key.
* **❗ The audio files may be modified or changed during the Transform process and Delete BGM process, so please back up the original audio files.**
* **❗ Google Cloud Speech API and Azure STT API will be charged if they exceed the free usage, so please check the price options carefully.**
* **❗❗ We are not responsible for the transformation of audio files due to the use of PAFTS or the payment of fees due to the use of STT API.**

## Requirements

* python >= 3.8
* spleeter
* pydub
* SpeechRecognition
* tqdm



## Installation

```
pip install pafts
```


## Usage

* Quick start:
    ```
    from pafts import PAFTS
    pafts = PAFTS(dataset_path="your dataset path", language='language')
    pafts.run()
    
  
    # Example
  
    pafts = PAFTS(
        dataset_path='C:\\Users\\82109\\Desktop\\dataset',
        language='en-us',
    )
    pafts.run()
  
  
  
  
    >> Run...
  | > Dataset name : dataset
  | > Path : C:\Users\82109\Desktop\dataset
  | > language : en-us
  | > Number of files : 5
  | > Total duration : 0:00:14.760000
  
  > Transform items...
  | > format : wav
  | > sr : 22050
  | > channel : 1
  change_format: 100%|██████████| 5/5 [00:00<00:00, 337.68it/s]
  change_sr: 100%|██████████| 5/5 [00:00<00:00, 141.79it/s]
  change_channel: 100%|██████████| 5/5 [00:00<00:00, 166.22it/s]
          
  > Delete BGM...
  | > Number of items : 5
  | > Path : C:\Users\82109\Desktop\dataset
  abc.wav: 100%|██████████| 5/5 [00:08<00:00,  1.65s/it]
  | > Number of Success items : 5
  | > Number of failure items : 0
  
  > Preparing STT API...
  | > STT API : google web speech
  | > Dataset name : dataset
  | > Path : C:\Users\82109\Desktop\dataset
  | > language : en-us
  | > Number of files : 5
  | > Total duration : 0:00:14.760000
  
  abc.wav: 100%|██████████| 5/5 [00:10<00:00,  2.02s/it]
  
  | > Numbers of deleted files : 0
  Saved at C:\Users\82109\Desktop\dataset\text.json
  Successfully Completed.

    ```
  
    'dataset_path' is your audio files path.
    'language' is BCP 47 tag.
    You can add a detailed option to the argument of run(). Please refer to the document of the run() for more information.


* If you want to task step by step:
    ```
    from pafts import PAFTS
    pafts = PAFTS(dataset_path="your dataset path", language='language', dataset_name='dataset name', key_path='api key path')
    pafts.transform_items(formats='audio format', sr=22050, channel=1)
    pafts.delete_bgm()
    dic = pafts.stt(stt_api_name='stt api name')
    pafts.save(dic=dic, output_name='text.json')
    ```

* If you want to make key file:
    ```
    from pafts import make_key_file
    make_key_file()    # default path : ./key.json
    ```

    ```
    # key.json
    
    {
        "google_cloud_stt": "credentials_json file path",
        "azure_stt": {
            "key": "KEY",
            "location": "LOCATION"
        }
    }
    ```

* If you want to Flatten directory structure:
    ```
    from pafts import PAFTS
    pafts = PAFTS(dataset_path="your dataset path")
    pafts.flatten()
    ```

    ```
    before dataset structure
    
          path
            ├── a
            │   ├── 1.wav
            │   ├── 2.wav
            │   └── 3.wav
            ├── b
            │   ├── 1.wav
            │   └── 2.wav
            ├── 1.wav
            ├── 2.wav
            └── c
                └── d
                    └── 1.wav
    
    
    after dataset structure
    
          path
            ├── a_1.wav
            ├── a_2.wav
            ├── a_3.wav
            ├── b_1.wav
            ├── b_2.wav
            ├── 1.wav
            ├── 2.wav
            └── c_d_1.wav
    ```

## License

The code of **PAFTS** is [MIT-licensed](LICENSE)


## Disclaimer

We are not responsible for the transformation of audio files due to the use of PAFTS or the payment of fees due to the use of STT API.

You agree that you use [PAFTS](https://github.com/harmlessman/PAFTS) at your own risk.

