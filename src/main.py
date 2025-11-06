# import flet as ft

# def main(page: ft.Page):

#     def login_page(e):
#         page.launch_url("https://flet.dev/")


#     page.floating_action_button = ft.FloatingActionButton(
#         icon=ft.Icons.ADD, on_click=login_page,
#         text="Login Now"
#     )

#     page.add(
#         ft.SafeArea(
#             ft.Container(
#                 ft.Text("Ini app saya", selectable=True),
#                 alignment=ft.alignment.center,
#             ),
#             expand=True,
#         )
#     )


# ft.app(main)

# import flet as ft
# import yt_dlp

# def main(page: ft.Page):
#     page.title = "YouTube Downloader"

#     def download_video(e):
#         url = url_input.value
#         ydl_opts = {"outtmpl": "storage/data/%(title)s.mp4"}
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=True)
#             page.snack_bar = ft.SnackBar(ft.Text(f"Downloaded: {info['title']}"))
#             page.snack_bar.open = True
#             page.update()

#     url_input = ft.TextField(label="YouTube URL")
#     download_button = ft.ElevatedButton("Download", on_click=download_video)

#     page.add(url_input, download_button)

# ft.app(target=main)

#################################

import flet as ft
import yt_dlp


def main(page: ft.Page):
    ph = ft.PermissionHandler()
    
    page.title = "YouTube Downloader"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.overlay.append(ph)

    status_text = ft.Text("Masukkan URL YouTube untuk mulai.")
    progress_bar = ft.ProgressBar(width=300, value=0)
    url_input = ft.TextField(label="YouTube URL", width=300)

    def my_hook(d):
        """Dipanggil setiap ada update dari yt_dlp."""
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes", 1)
            downloaded = d.get("downloaded_bytes", 0)
            progress = downloaded / total_bytes
            progress_bar.value = progress
            status_text.value = f"Mengunduh... {progress * 100:.1f}%"
            page.update()

        elif d["status"] == "finished":
            status_text.value = "Download selesai! Menyimpan file..."
            progress_bar.value = 1
            page.update()

    def download_video(e):
        url = url_input.value.strip()
        if not url:
            page.snack_bar = ft.SnackBar(ft.Text("Masukkan URL dulu!"))
            page.snack_bar.open = True
            page.update()
            return

        status_text.value = "Menyiapkan download..."
        progress_bar.value = 0
        page.update()

        ydl_opts = {
            "outtmpl": "/storage/emulated/0/DCIM/ytdlp/%(title)s.mp4",
            "progress_hooks": [my_hook],
            "quiet": True,  # biar gak spam log di terminal
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
            status_text.value = f"Selesai: {info['title']}"
            page.snack_bar = ft.SnackBar(ft.Text("Berhasil diunduh!"))
            page.snack_bar.open = True
        except Exception as ex:
            status_text.value = f"Error: {ex}"
            page.snack_bar = ft.SnackBar(ft.Text("Gagal mengunduh video."))
            page.snack_bar.open = True

        progress_bar.value = None
        page.update()

    result_text = ft.Text()

    def request_storage_permission(e):
        res = ph.request_permission(ft.PermissionType.MANAGE_EXTERNAL_STORAGE)
        result_text.value = f"Hasil: {res}"
        page.update()

    def open_settings(e):
        ph.open_app_settings()

    download_button = ft.ElevatedButton("Download", on_click=download_video)
    request_storage = ft.ElevatedButton("Request permission", on_click=request_storage_permission)
    setting = ft.ElevatedButton("Open Settings", on_click=open_settings)

    page.add(
        ft.Column(
            [
                url_input,
                ft.Row(
                    [
                        download_button,
                        request_storage,
                        setting,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                progress_bar,
                status_text,
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(main)

#################################

# import flet as ft

# def main(page: ft.Page):
#     page.title = "Permission Test"
#     ph = ft.PermissionHandler()
#     page.overlay.append(ph)

#     result_text = ft.Text("Belum ada aksi")

#     def request_storage_permission(e):
#         result_text.value = "Meminta izin penyimpanan..."
#         page.update()
#         res = ph.request_permission(ft.PermissionType.MICROPHONE)
#         result_text.value = f"Hasil: {res}"
#         page.update()

#     def check_storage_permission(e):
#         res = ph.check_permission(ft.PermissionType.MICROPHONE)
#         result_text.value = f"Status izin: {res}"
#         page.update()

#     def open_settings(e):
#         ph.open_app_settings()

#     page.add(
#         ft.SafeArea(
#             ft.Column([
#                 ft.OutlinedButton("Check Permission", on_click=check_storage_permission),
#                 ft.OutlinedButton("Request Permission", on_click=request_storage_permission),
#                 ft.OutlinedButton("Open App Settings", on_click=open_settings),
#                 result_text,
#             ])
#         ),
#     )

# ft.app(target=main)

#################################

# import flet as ft
# import flet_permission_handler as fph

# def main(page: ft.Page):
#     # 1. Inisialisasi PermissionHandler dan tambahkan ke overlay
#     ph = fph.PermissionHandler()
#     page.overlay.append(ph)
#     page.update()

#     def request_storage_permission(e):
#         # Meminta izin penyimpanan (Permission.STORAGE atau Permission.PHOTOS)
#         # Catatan: Di Android modern, izin penyimpanan telah diperketat.
#         # Anda mungkin perlu izin spesifik seperti MEDIA_IMAGES/VIDEO.
#         # Coba gunakan PHOTOS atau MEDIA_IMAGES di Android/iOS untuk akses galeri.
#         status = ph.request_permission(fph.PermissionType.STORAGE) 
        
#         page.add(ft.Text(f"Status Izin Penyimpanan: {status.name}"))
        
#         # Contoh status: GRANTED (diizinkan), DENIED (ditolak), PERMANENTLY_DENIED (ditolak permanen)
#         if status == fph.PermissionStatus.PERMANENTLY_DENIED:
#             # Arahkan pengguna ke Pengaturan Aplikasi jika ditolak permanen
#             ph.open_app_settings()

#     page.add(
#         ft.SafeArea(
#             ft.OutlinedButton(
#             "Minta Izin Penyimpanan (Storage)", 
#             on_click=request_storage_permission
#             )
#         )
#     )

# ft.app(target=main)