from crawlers import Hjwzw


if __name__ == "__main__":
    # 全本爬取
    # Hjwzw(
    #     novel_id=37018, 
    #     novel_name="瘋狂升級系統"
    # ).main()

    # 斷點續爬
    Hjwzw(
        novel_id=37018, 
        novel_name="瘋狂升級系統", 
        after_chapter_id=15775160,  # 包含此章節
        is_continue=True
    ).main()
