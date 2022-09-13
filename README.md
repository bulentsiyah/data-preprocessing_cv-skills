# Data Preprocessing and CV Skills

## What is it?
Bu repo Bilgisayarlı Görü (Computer Vision) yetenekleri geliştirmek için yaratılmıştır.

Hope this might be useful to someone! :-)

## Who am I?
>Hi 👋

## What to do next:
- [x] readme yaratılacak
- [x] requirements yaratılacak(pipreqs) – her kütüphane ihtiyacında güncellenecek
- [x] output ve data şeklinde klasor yapısı olacak
- [x] main başlayacak
- [x] config dosyası olacak ilk veriler oradan alınacak
- [x] video operasyonu var ise bağımsız class olacak
- [x] tool sınıfı olacak ıse yarar hesaplamalar orda duracak
- [x] drawing sınıfı olacak o sayede tüm çizimler yapılacak
- [ ] Her yeni CV yeteneği çıktısını readme ekle

## How does it work?
requirements.txt yükle: pip install -r requirements.txt

reponun bir adım gerisine:
git clone https://github.com/nwojke/deep_sort.git
git clone https://github.com/ultralytics/yolov5.git



## Overview

### Projects

#### Yarı otomatik etiketleme

- **Summary:** Video üzerinden seçili objeyi takip edip etiketleme. Önce ilk sınıftan toplam sınıfa kadar döngü şeklinde etıketleme yapılır. 
- **Keywords:** 
<table style="width:100%">
  <tr>
    <th>
      <p align="center">
           <img src="./_images_must/readme/semi_labeling.png" alt="Overview" width="90%" height="90%">
           <br><a href="./semi_labeling.py" >(semi_labeling.py)</a>
      </p>
    </th>
  </tr>
</table>

#### Yarı otomatik etiketleme

- **Summary:** Daha önce eğitilmiş bir model video üzerinde tahminleme yaptırılıp, etiketlemeye yardımcı olması sağlanır. 
- **Keywords:** 
<table style="width:100%">
  <tr>
    <th>
      <p align="center">
           <img src="./_images_must/readme/pretrain_model_for_labeling.png" alt="Overview" width="90%" height="90%">
           <br><a href="./pretrain_model_for_labeling.py" >(pretrain_model_for_labeling.py)</a>
      </p>
    </th>
  </tr>
</table>

#### Split Sataset

- **Summary:** Etiketleme veya pretrained ile hazırlanmış veriyi configkteki oranlara göre ayırır. 
- [] splitte hem yolov3 hemde yolov5 için dosyalar rastgele seçilmeli
- **Keywords:** 
<table style="width:100%">
  <tr>
    <th>
      <p align="center">
           <img src="./_images_must/readme/splitdataset.png" alt="Overview" width="90%" height="90%">
           <br><a href="./splitdataset.py" >(splitdataset.py)</a>
      </p>
    </th>
  </tr>
</table>

#### Data Analysis

- **Summary:** veri ile ilgili csv dosyası yaratılır. Bu dosyada width height bulunduğu region alan gibi özellikler bulunur ve bu dosya dataanalysis_visualization.ipynb dosyasında grafiklerle incelenir.

- **Keywords:** 
<table style="width:100%">
  <tr>
    <th>
      <p align="center">
           <img src="./_images_must/readme/dataanalysis.png" alt="Overview" width="90%" height="90%">
           <br><a href="./dataanalysis.py" >(dataanalysis.py)</a>
      </p>
    </th>
  </tr>
</table>


#### DeepSort

- **Summary:** detectiondan gelen bounding box larla sonraki framelerde aynı id almasını sağlyan kod bloğu.
- **Keywords:** 
<table style="width:100%">
  <tr>
    <th>
      <p align="center">
           <img src="./_images_must/readme/deepsort.png" alt="Overview" width="90%" height="90%">
           <br><a href="./deepsort.py" >(deepsort.py)</a>
      </p>
    </th>
  </tr>
</table>

#### Image Stabilization Via Gaussian Filters In Opencv

- **Summary:** 
- **Keywords:** 
<table style="width:100%">
  <tr>
    <th>
      <p align="center">
           <img src="./_images_must/readme/video_stabilization.gif" alt="Overview" width="90%" height="90%">
           <br><a href="./video_stabilization/main.py" >(video_stabilization.py)</a>
      </p>
    </th>
  </tr>
</table>