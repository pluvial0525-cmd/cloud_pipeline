from app.imageRag.service import (
    BASE_DIR,
    create_embedding,
    create_table,
    describe_file_image,
    embedding_exists,
    get_image_files,
    save_embedding,
)


def build_embeddings():

    print()
    print("==============================")
    print("Image RAG 임베딩 생성 시작")
    print("==============================")
    print()


    create_table()


    image_files = get_image_files()


    print(
        f"전체 이미지 수: "
        f"{len(image_files)}"
    )

    print()


    success_count = 0

    skip_count = 0

    fail_count = 0


    for index, image_path in enumerate(
        image_files,
        start=1,
    ):

        relative_path = str(
            image_path.relative_to(
                BASE_DIR
            )
        )


        print(
            f"[{index}/{len(image_files)}] "
            f"{relative_path}"
        )


        # -------------------------------------
        # 이미 처리한 이미지는 건너뜀
        # -------------------------------------

        if embedding_exists(
            relative_path
        ):

            print(
                "  → 이미 저장되어 있음 "
                "(건너뜀)"
            )

            skip_count += 1

            continue


        try:

            food_name = (
                image_path.parent.name
            )


            print(
                "  → 이미지 분석 중..."
            )

            description = (
                describe_file_image(
                    image_path
                )
            )


            print(
                "  → 임베딩 생성 중..."
            )

            embedding = (
                create_embedding(
                    description
                )
            )


            save_embedding(
                food_name=food_name,
                image_path=relative_path,
                description=description,
                embedding=embedding,
            )


            success_count += 1


            print(
                f"  → 저장 완료: "
                f"{food_name}"
            )


        except Exception as e:

            fail_count += 1

            print(
                "  → 처리 실패"
            )

            print(
                f"  → {e}"
            )


        print()


    print()
    print("==============================")
    print("Image RAG 임베딩 생성 완료")
    print("==============================")

    print(
        f"신규 저장: "
        f"{success_count}"
    )

    print(
        f"기존 데이터: "
        f"{skip_count}"
    )

    print(
        f"실패: "
        f"{fail_count}"
    )


if __name__ == "__main__":

    build_embeddings()