import styled from "styled-components";

import ImageUpload
    from "../components/ImageUpload";

import ImageResult
    from "../components/ImageResult";

import {
    useImageRagMutation,
} from "../query/imageRagQuery";


function ImageRagPage() {
    const imageRagMutation =
        useImageRagMutation();


    const handleSearch = (
        file,
    ) => {
        imageRagMutation.mutate({
            file,
            topK: 5,
        });
    };


    return (
        <Page>
            <Container>
                <Header>
                    <Badge>
                        IMAGE RAG
                    </Badge>

                    <Title>
                        Korean Food
                        Image Search
                    </Title>

                    <Subtitle>
                        음식 이미지를
                        업로드하면
                        OpenAI Vision과
                        임베딩을 이용해
                        가장 유사한 음식
                        이미지를 검색합니다.
                    </Subtitle>
                </Header>


                <Content>
                    <ImageUpload
                        onSearch={
                            handleSearch
                        }
                        isPending={
                            imageRagMutation
                                .isPending
                        }
                    />

                    <ImageResult
                        data={
                            imageRagMutation
                                .data
                        }
                    />
                </Content>


                {imageRagMutation
                    .isError && (
                    <ErrorBox>
                        검색 중 오류가
                        발생했습니다.

                        <br />

                        {
                            imageRagMutation
                                .error
                                ?.response
                                ?.data
                                ?.detail
                            ||
                            imageRagMutation
                                .error
                                ?.message
                        }
                    </ErrorBox>
                )}
            </Container>
        </Page>
    );
}


export default ImageRagPage;


const Page = styled.div`
    min-height: 100vh;

    background:
        radial-gradient(
            circle at top,
            #1b2035 0%,
            #0d1017 42%,
            #080a0f 100%
        );

    color: white;
`;


const Container = styled.div`
    width: min(
        1180px,
        calc(
            100% - 40px
        )
    );

    margin: 0 auto;

    padding: 70px 0;
`;


const Header = styled.div`
    margin-bottom: 45px;
`;


const Badge = styled.div`
    display: inline-block;

    margin-bottom: 12px;

    padding: 7px 12px;

    border-radius: 100px;

    background:
        rgba(
            124,
            92,
            255,
            0.15
        );

    border: 1px solid
        rgba(
            124,
            92,
            255,
            0.3
        );

    color: #9587ff;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.5px;
`;


const Title = styled.h1`
    margin: 0;

    font-size:
        clamp(
            38px,
            5vw,
            66px
        );

    letter-spacing: -2px;
`;


const Subtitle = styled.p`
    width: min(
        650px,
        100%
    );

    margin-top: 16px;

    color: #929baa;

    font-size: 16px;

    line-height: 1.7;
`;


const Content = styled.div`
    display: grid;

    grid-template-columns:
        minmax(
            0,
            0.9fr
        )
        minmax(
            0,
            1.1fr
        );

    gap: 25px;

    align-items: start;

    @media (
        max-width: 950px
    ) {
        grid-template-columns:
            1fr;
    }
`;


const ErrorBox = styled.div`
    margin-top: 20px;

    padding: 18px;

    border-radius: 14px;

    border: 1px solid
        rgba(
            255,
            90,
            90,
            0.3
        );

    background:
        rgba(
            255,
            90,
            90,
            0.08
        );

    color: #ff9b9b;

    line-height: 1.6;
`;