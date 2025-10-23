from crawlers import Hjwzw


if __name__ == "__main__":
    # 全本爬取
    Hjwzw(
        novel_id=40949, 
        novel_name="我師兄實在太穩健了"
    ).main()

    # 斷點續爬
    # Hjwzw(
    #     novel_id=35543, 
    #     novel_name="重啟末世", 
    #     after_chapter_id=11822905,  # 包含此章節
    #     is_continue=True
    # ).main()
