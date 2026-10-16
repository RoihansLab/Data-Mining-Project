from youtube_comment_downloader import YoutubeCommentDownloader
import csv

# Daftar video AI/otomasi vs pekerjaan - 6 video final (ID + EN, berita + opini + cerita personal + edukasi)

VIDEO_URLS = [
    "https://www.youtube.com/watch?v=t2WmNcToB3I",  # (ID) Pekerja Latih Robot Untuk Gantikan Mereka! KIAMAT KERJA AI DIMULAI! (899 komentar)
    "https://www.youtube.com/watch?v=F8pz5wIO6gA",  # (ID) Manusia Belum Tergantikan AI Karena Satu Hambatan Ini (912 komentar)
    "https://www.youtube.com/watch?v=7Pq-S557XQU",  # (EN) Humans Need Not Apply - CGP Grey (47.937 komentar)
    "https://www.youtube.com/watch?v=SDich6serU0",  # (EN) The EXACT moment AI took my job... (261 komentar)
    "https://www.youtube.com/watch?v=s1c4Ji6tNdw",  # (EN) UK unemployment soars: is AI already taking our jobs? (951 komentar)
    "https://www.youtube.com/watch?v=0LOHWGQwKtM",  # (EN) AI is taking their jobs. But they're fighting back. (163 komentar)
]

# Dibatasi biar video #3 (yang komentarnya 47rb) nggak mendominasi dataset secara nggak proporsional.
# Video dengan komentar < limit ini akan terambil semuanya (habis).
MAX_COMMENTS_PER_VIDEO = 1500
OUTPUT_FILE = "youtube_comments.csv"

downloader = YoutubeCommentDownloader()
all_comments = []

for url in VIDEO_URLS:
    print(f"Scraping: {url}")
    count = 0
    try:
        for comment in downloader.get_comments_from_url(url, sort_by=0):  # 0 = popular, 1 = recent
            all_comments.append({
                "video_url": url,
                "author": comment.get("author"),
                "comment": comment.get("text"),
                "likes": comment.get("votes"),
                "time": comment.get("time"),
            })
            count += 1
            if count >= MAX_COMMENTS_PER_VIDEO:
                break
    except Exception as e:
        print(f"Gagal scraping {url}: {e}")
    print(f"  -> {count} komentar diambil")

# Simpan ke CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["video_url", "author", "comment", "likes", "time"])
    writer.writeheader()
    writer.writerows(all_comments)

print(f"\nTotal komentar: {len(all_comments)}")
print(f"Tersimpan di: {OUTPUT_FILE}")