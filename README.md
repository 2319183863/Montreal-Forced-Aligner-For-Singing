# Montreal Forced Aligner For Singing


### Conda environment installation

#### step 1

```
conda env create -n mfa -f environment.yml
```

#### step 2

MFA can be installed in develop mode via:

```
pip install -e .[dev]
```

### Prepare data

#### step 1
prepare data

数据准备为以下格式
其中 .lab 里存放的是音频对于的文本

```
.
.
|-- 100000081.lab
|-- 100000081.wav
|-- 100000198.lab
`-- 100000198.wav
```

#### step 2
将文本转换为拼音格式

```
python preprocess.py
```
将会生成下面格式的文件，其中.txt是原始的文本，.lab是拼音格式的文本

```
.
|-- 100000081.lab
|-- 100000081.txt
|-- 100000081.wav
|-- 100000198.lab
|-- 100000198.txt
`-- 100000198.wav
```

### Train

#### step 2

```

mfa train [数据路径] \
[字典路径] \
[模型保存路径] \
-t [训练过程中的临时文件保存路径] -j [训练使用的核] --single_speaker --clean --beam 100 


mfa train /datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner-For-Singing/zz_test/wav_preprocessed \
dictionary.txt \
/datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner-For-Singing/zz_logs/wav_preprocessed/acoustic_model.zip \
-t /datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner-For-Singing/zz_temp -j 50 --single_speaker --clean --beam 100 

```

### inference

```

mfa align [需要推理的数据集路径] \
[训练完模型生成的字典路径] \
[声学模型路径] \
[输出的TextGrid文件保存路径]

mfa align /datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner-For-Singing/zz_test/wav_preprocessed \
/datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner-For-Singing/zz_logs/wav_preprocessed/dictionary.dict \
/datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner-For-Singing/zz_logs/wav_preprocessed/acoustic_model.zip \
/datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner-For-Singing/zz_test/wav_preprocessed

```
