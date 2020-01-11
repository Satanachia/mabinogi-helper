
# Mabinogi-Helper

[![LICENSE](https://img.shields.io/badge/license-BSD%203%20Clause-blue.svg "LICENSE")](https://github.com/fadhiilrachman/line-py/blob/master/LICENSE) [![Supported python versions: 3.8](https://img.shields.io/badge/python-3.8-green.svg "Supported python versions: 3.8")](https://www.python.org/downloads/)  
這個是新瑪奇的遊戲輔助程式，基本上全部都不違反遊戲相關規定。  
跟遊戲相關的部分我有稍微區分開來，不過絕大部分都不是適合一般玩家使用的，所以並不會提供詳細說明與安裝教學。  

## 帳號
>打開 [accountsInfo.json.example](https://github.com/NNSound/mabinogi-helper/blob/master/common/config/accountsInfo.json.example) 填入你的分身帳號密碼
並把.example後綴刪掉。  
這部分請務必小心使用，本人不負責各種被盜之類的問題責任。 

## 爬蟲 & Selenium
>Selenium Driver 請自行解壓縮對應的os，因為考慮到Linux 的crontab 真的很好用，所以我兩種OS的版本都有寫過，目前正在研究 WSL 如果有時間會嘗試把這部分全部放到 Linux 上處理

## Discord Bot
[![Chat on Discord](https://discordapp.com/api/guilds/632783197968662528/widget.png "Chat on Discord")](https://discord.gg/PfuguUb)
>這算是目前正在頻繁維護更新的部分，詳細情況請至該[頁面](https://github.com/NNSound/mabinogi-helper/tree/master/common/tool/discord)查看詳細情況

## Line Bot
>算是Discord bot 的前身，有官方Bot & Line Notify 兩種，前者因為免費推送訊息限制放棄，後者因為Line 畢竟是比較私人性質的東西，所以後來轉到 Discord 的平台上。  
詳細的部分可以看[這裡](https://github.com/NNSound/mabinogi-helper/tree/master/common/tool/line)

## 其他
>這裡通常是比較獨立的小工具，有些東西暫時是沒有進去版控的，詳細部分就請自己慢慢摸索囉~

## 套件安裝
```
pip install -r requirements.txt
```
