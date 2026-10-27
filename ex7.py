from pathlib import Path
import requests 
import time
import csv
from datetime import datetime

urls = ["https://example.com",
        "https://www.google.com"]


server_log = Path("server_log.csv")

first_run = not server_log.exists()

slow_threshold = 2.0  
timeout_seconds = 5.0

def judge_status(code,elapsed,slow_threshold):
    if  200<= code < 300:
        if elapsed >= slow_threshold:
            return "遅い"
        else:
            return "正常"

    elif 300 <= code < 400:
        return "リダイレクト"
            
    elif 400<= code <500:
        if code == 404:
            return "ページが見つかりません"
        else:
            return "クライアントエラー"
                            
    elif 500 <= code < 600:
       return "サーバーエラー"
            
    else:
        return "その他のHTTP応答"
    


            
        
with server_log.open("a",newline = "",encoding = "utf-8-sig") as file:
    writer = csv.writer(file)
    
    if first_run:
        writer.writerow(["日時","URL","HTTPコード","状態","応答時間"])#実際に書き込む
    
    for url in urls:
        now = datetime.now()
        time_text = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            start = time.perf_counter()
            response = requests.get(url, timeout=timeout_seconds)
            elapsed = time.perf_counter() - start
            code = response.status_code 
            status = judge_status(code,elapsed,slow_threshold)
            print(url)
            print(f"状態: {status}")
            print(f"応答時間: {elapsed:.2f}秒")
            print(f"HTTPコード: {response.status_code}")
        
        except requests.RequestException:
            elapsed = time.perf_counter() - start
            print(url)
            print("状態:リクエスト失敗")
            print(f"応答時間: {elapsed:.2f}秒")
            print("HTTPコード取得できません")
            code = ""
            status = "リクエスト失敗"
        
        writer.writerow([time_text,url,code,status,f"{elapsed:.2f}"])
        
        